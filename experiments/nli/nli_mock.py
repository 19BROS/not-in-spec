# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers>=4.40", "sentencepiece", "protobuf"]
# ///
"""Mock of the chunk -> claim -> NLI-window path (SPEC 6.1, 6.4). Experiment only, not core.

Everything for one section lives in sections/<slug>/:
  section.json              simulated Sphinx parse (input, hand-written)
  build -> chunk.{json,md}, prompt.md (paste into a model), windows-<N>.json
  claims/<model>.json       paste the model's answer here
  pair  -> pairs/<model>.windows-<N>.jsonl (citation check + NLI premise/hypothesis)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
SECTIONS = HERE / "sections"
DEFAULT_TOKENIZER = "cross-encoder/nli-deberta-v3-base"
ABBREVIATIONS = ("etc.", "e.g.", "i.e.", "vs.", "approx.")
PROSE_BLOCKS = ("paragraph", "list_item", "admonition")  # each item / box is its own block


def norm(text: str) -> str:
    """Form used for citation matching and NLI input: no backticks, single spaces."""
    return " ".join(text.replace("`", "").split())


def render_markdown(section: dict[str, Any]) -> str:
    crumbs = section["breadcrumb"]
    parts = [f"{'#' * len(crumbs)} {crumbs[-1]}"]
    for block in section["blocks"]:
        if block["type"] == "code":
            parts.append(f"```{block['language'] or ''}\n{block['text']}\n```")
        elif block["type"] == "list_item":  # extra paragraphs indented under the bullet
            parts.append("- " + block["text"].replace("\n\n", "\n\n  "))
        elif block["type"] == "admonition":
            body = block["text"].replace("\n\n", "\n>\n> ")
            parts.append(f"> **{block['kind'].capitalize()}:** {body}")
        else:
            parts.append(block["text"])
    return "\n\n".join(parts) + "\n"


def chunk_id(breadcrumb: list[str], markdown: str) -> str:
    """Stable ID = hash of heading path + content (SPEC 4)."""
    return hashlib.sha256((" > ".join(breadcrumb) + "\n" + markdown).encode()).hexdigest()[:16]


def split_sentences(paragraph: str) -> list[str]:
    """Deterministic splitter: break after . ! ? + space when the next char starts a sentence."""
    out, start = [], 0
    for m in re.finditer(r"(?<=[.!?])\s+(?=[A-Z`\"(])", paragraph):
        before = paragraph[start : m.start()]
        if before.endswith(ABBREVIATIONS):
            continue
        out.append(before.strip())
        start = m.end()
    out.append(paragraph[start:].strip())
    return [s for s in out if s]


def prose_sentences(section: dict[str, Any]) -> list[dict[str, Any]]:
    """Prose-only stream: code blocks and tables are left out (SPEC 6.1)."""
    sents: list[dict[str, Any]] = []
    for b_idx, block in enumerate(section["blocks"]):
        if block["type"] not in PROSE_BLOCKS:
            continue
        for s in split_sentences(block["text"]):
            sents.append({"i": len(sents), "block": b_idx, "text": norm(s)})
    return sents


def join_sentences(sents: list[dict[str, Any]]) -> str:
    text = ""
    for k, s in enumerate(sents):
        if k:
            text += " " if s["block"] == sents[k - 1]["block"] else "\n\n"
        text += s["text"]
    return text


def make_windows(
    sents: list[dict[str, Any]], count: Callable[[str], int], max_tokens: int, overlap: int
) -> list[tuple[int, int]]:
    """Greedy pack of whole sentences up to max_tokens; next window repeats `overlap` sentences."""
    windows: list[tuple[int, int]] = []
    i = 0
    while i < len(sents):
        j = i
        while j < len(sents) and count(join_sentences(sents[i : j + 1])) <= max_tokens:
            j += 1
        j = max(j, i + 1)  # a single sentence over the limit still gets its own window
        windows.append((i, j))
        if j >= len(sents):
            break
        i = max(j - overlap, i + 1)
    return windows


def load_tokenizer(name: str) -> tuple[Callable[[str], int], int]:
    from transformers import AutoTokenizer  # heavy import, only when needed

    tok = AutoTokenizer.from_pretrained(name)

    def count(text: str) -> int:
        return len(tok(text, add_special_tokens=False, verbose=False)["input_ids"])

    return count, int(tok.model_max_length)


def cmd_build(args: argparse.Namespace) -> None:
    count, model_max = load_tokenizer(args.tokenizer)
    templates = {
        name: (HERE / name).read_text(encoding="utf-8")
        for name in ("prompt.md", "prompt-outside.md")
    }
    for d in section_dirs(args.slugs):
        slug = d.name
        section = json.loads((d / "section.json").read_text(encoding="utf-8"))
        md = render_markdown(section)
        cid = chunk_id(section["breadcrumb"], md)
        chunk = {
            "chunk_id": cid,
            "slug": slug,
            "breadcrumb": section["breadcrumb"],
            "source": section["source"],
            "components": sorted({"C" if b["type"] == "code" else "D" for b in section["blocks"]}),
            "tokens": count(md),
            "markdown": md,
        }
        (d / "chunk.json").write_text(json.dumps(chunk, indent=2), encoding="utf-8")
        (d / "chunk.md").write_text(md, encoding="utf-8")
        for name, template in templates.items():
            prompt = (
                template.replace("{{PROJECT}}", section["source"]["project"])
                .replace("{{BREADCRUMB}}", " > ".join(section["breadcrumb"]))
                .replace("{{CHUNK}}", md.strip())
            )
            (d / name).write_text(prompt, encoding="utf-8")
        (d / "claims").mkdir(exist_ok=True)

        sents = prose_sentences(section)
        spans = make_windows(sents, count, args.max_tokens, args.overlap)
        windows = []
        for i, j in spans:
            text = join_sentences(sents[i:j])
            windows.append(
                {
                    "id": f"{cid}:s{i}-s{j - 1}",
                    "sentences": [i, j - 1],
                    "tokens": count(text),
                    "text": text,
                }
            )
        doc = {
            "chunk_id": cid,
            "slug": slug,
            "tokenizer": args.tokenizer,
            "max_tokens": args.max_tokens,
            "overlap_sentences": args.overlap,
            "pair_limit": model_max,
            "sentences": sents,
            "windows": windows,
        }
        (d / f"windows-{args.max_tokens}.json").write_text(json.dumps(doc, indent=2), "utf-8")
        sizes = ", ".join(str(w["tokens"]) for w in windows)
        print(
            f"{slug}: chunk {cid}, {chunk['tokens']} tok, {len(sents)} prose sentences, "
            f"{len(windows)} windows @ {args.max_tokens} [{sizes}]"
        )


def parse_claims(raw: str) -> list[dict[str, Any]]:
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw.strip())
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:  # chat UIs sometimes turn quotes into typographic ones
        data = json.loads(raw.translate(str.maketrans("“”‘’", "\"\"''")))
    claims = data["claims"] if isinstance(data, dict) else data
    return [c for c in claims if isinstance(c, dict)]


def section_dirs(slugs: list[str]) -> list[Path]:
    dirs = [SECTIONS / s for s in slugs] if slugs else sorted(SECTIONS.iterdir())
    return [d for d in dirs if (d / "section.json").is_file()]


def cmd_pair(args: argparse.Namespace) -> None:
    counters: dict[str, Callable[[str], int]] = {}
    for d in section_dirs(args.slugs):
        chunk = json.loads((d / "chunk.json").read_text(encoding="utf-8"))
        extractors = {}
        for cpath in sorted((d / "claims").glob("*.json")):
            raw = cpath.read_text(encoding="utf-8")
            if raw.strip():
                extractors[cpath.stem] = parse_claims(raw)
            else:
                print(f"{d.name}/claims/{cpath.name}: empty, skipped")
        for wpath in sorted(d.glob("windows-*.json")):
            wdoc = json.loads(wpath.read_text(encoding="utf-8"))
            if wdoc["tokenizer"] not in counters:
                counters[wdoc["tokenizer"]] = load_tokenizer(wdoc["tokenizer"])[0]
            for name, claims in extractors.items():
                pair_one(d, chunk, wdoc, name, claims, counters[wdoc["tokenizer"]])


def pair_one(
    d: Path,
    chunk: dict[str, Any],
    wdoc: dict[str, Any],
    extractor: str,
    claims: list[dict[str, Any]],
    count: Callable[[str], int],
) -> None:
    sents, windows = wdoc["sentences"], wdoc["windows"]
    chunk_norm = norm(chunk["markdown"])
    prose, offsets = "", []  # sentence i covers prose[offsets[i][0]:offsets[i][1]]
    for s in sents:
        if prose:
            prose += " "
        offsets.append((len(prose), len(prose) + len(s["text"])))
        prose += s["text"]

    rows, stats = [], {"ok": 0}
    for n, c in enumerate(claims, 1):
        cit = norm(str(c.get("citation", "")))
        row: dict[str, Any] = {
            "chunk_id": wdoc["chunk_id"],
            "extractor": extractor,
            "claim_id": c.get("id", f"c{n}"),
            "type": c.get("type"),
            "citation": c.get("citation"),
            "hypothesis": c.get("claim"),
        }
        if c.get("kind"):  # outside / beyond (prompt-outside.md)
            row["kind"] = c["kind"]
        pos = prose.find(cit) if cit else -1
        if not cit or cit not in chunk_norm:
            row["status"] = "dropped:citation_not_in_chunk"  # SPEC 6.4 step 1
        elif pos < 0:
            row["status"] = "dropped:citation_not_in_prose"  # only in code / spans a code block
        else:
            end = pos + len(cit)
            hit = [i for i, (a, b) in enumerate(offsets) if a < end and b > pos]
            lo, hi = hit[0], hit[-1]
            inside = [w for w in windows if w["sentences"][0] <= lo and hi <= w["sentences"][1]]
            if inside:
                used = [inside[0]]
                row["status"] = "ok"
            else:  # citation crosses a window boundary -> join the neighbouring windows
                used = [w for w in windows if w["sentences"][1] >= lo and w["sentences"][0] <= hi]
                row["status"] = "ok:joined_windows"
            first, last = used[0]["sentences"][0], used[-1]["sentences"][1]
            row["window_ids"] = [w["id"] for w in used]
            row["cited_sentences"] = [lo, hi]
            row["premise"] = join_sentences(sents[first : last + 1])
            row["premise_tokens"] = count(row["premise"])
            pair_tokens = row["premise_tokens"] + count(str(row["hypothesis"])) + 3
            if pair_tokens > wdoc["pair_limit"]:
                row["warning"] = f"pair is {pair_tokens} tokens > {wdoc['pair_limit']}, truncated"
        key = row["status"] if not row["status"].startswith("ok") else "ok"
        stats[key] = stats.get(key, 0) + 1
        rows.append(row)

    (d / "pairs").mkdir(exist_ok=True)
    out = d / "pairs" / f"{extractor}.windows-{wdoc['max_tokens']}.jsonl"
    out.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    print(f"{out.relative_to(SECTIONS).as_posix()}: {len(rows)} claims {stats}")
    for r in rows:
        if not r["status"].startswith("ok"):
            print(f"  {r['claim_id']}: {r['status']}: {r['citation']!r}")


# Sections whose claims are cross-paired: each claim is scored against the OTHER section's
# prose (gold: must not be kept, since grounding must find a claim in its own section).
CROSS_GROUPS = [
    ("retrying-requests", "configuring-exponential-backoff"),  # same page, related topic
    ("using-timeouts", "httpx-timeouts-fine-tuning"),  # same topic, different library
    ("changelog-2-8-0-security", "changelog-2-8-0-bugfixes"),  # same release, overlapping fix
]
STOPWORDS = {"the", "and", "for", "with", "that", "this", "are", "can", "not", "when", "from"}


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9_]+", text.lower()) if len(w) >= 3} - STOPWORDS


def cmd_cross(args: argparse.Namespace) -> None:
    """Pair each real claim of section A with the most word-similar sentence of section B.

    Written to B/pairs/x-<A>~<extractor>.windows-N.jsonl, so the premise and its breadcrumb
    belong to B. The best-matching sentence is the 'citation' (hardest wrong premise).
    """
    for a, b in [*CROSS_GROUPS, *[(y, x) for x, y in CROSS_GROUPS]]:
        da, db = SECTIONS / a, SECTIONS / b
        if not (da / "claims").is_dir() or not (db / "chunk.json").exists():
            continue
        chunk_b = json.loads((db / "chunk.json").read_text(encoding="utf-8"))
        for cpath in sorted((da / "claims").glob("*.json")):
            name = cpath.stem
            raw = cpath.read_text(encoding="utf-8")
            if not raw.strip() or name.startswith("negatives") or name.endswith("-outside"):
                continue
            claims = parse_claims(raw)
            for wpath in sorted(db.glob("windows-*.json")):
                wdoc = json.loads(wpath.read_text(encoding="utf-8"))
                sents = wdoc["sentences"]
                rows = []
                for n, c in enumerate(claims, 1):
                    cw = words(str(c.get("claim", "")))
                    best = max(range(len(sents)), key=lambda i: len(cw & words(sents[i]["text"])))
                    win = next(
                        w for w in wdoc["windows"] if w["sentences"][0] <= best <= w["sentences"][1]
                    )
                    rows.append(
                        {
                            "chunk_id": chunk_b["chunk_id"],
                            "extractor": f"x-{a}~{name}",
                            "claim_id": c.get("id", f"c{n}"),
                            "type": c.get("type"),
                            "citation": sents[best]["text"],
                            "hypothesis": c.get("claim"),
                            "cross_from": a,
                            "status": "ok",
                            "window_ids": [win["id"]],
                            "cited_sentences": [best, best],
                            "premise": win["text"],
                            "premise_tokens": win["tokens"],
                        }
                    )
                (db / "pairs").mkdir(exist_ok=True)
                out = db / "pairs" / f"x-{a}~{name}.windows-{wdoc['max_tokens']}.jsonl"
                out.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
                print(f"{out.relative_to(SECTIONS).as_posix()}: {len(rows)} cross pairs")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="sections -> chunks, prompts, NLI windows")
    b.add_argument("--max-tokens", type=int, default=400, help="window size (SPEC candidate 400)")
    b.add_argument("--overlap", type=int, default=1, help="sentences repeated between windows")
    b.add_argument("--tokenizer", default=DEFAULT_TOKENIZER)
    b.set_defaults(func=cmd_build)
    q = sub.add_parser("pair", help="all claims/*.json x windows-*.json -> pairs/*.jsonl")
    q.set_defaults(func=cmd_pair)
    x = sub.add_parser("cross", help="claims of section A x prose of related section B")
    x.set_defaults(func=cmd_cross)
    for sp in (b, q):
        sp.add_argument("slugs", nargs="*", help="section folder names (default: all)")
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
