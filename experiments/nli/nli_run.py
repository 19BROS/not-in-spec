# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.4", "transformers>=4.56", "sentencepiece", "protobuf"]
#
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
#
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
"""Score every sections/<slug>/pairs/*.jsonl with local NLI cross-encoders (CPU), as a tracked run.

Nothing is installed into the repo: uv builds a cached env for this script, and model
weights go to the Hugging Face cache (~/.cache/huggingface, override with HF_HOME).

Each invocation = one run in runs/NNN-<name>/:
  config.json   git commit, models, contexts, premises, versions, input hashes, timing
  results/      <model>__ctx-<context>__prem-<premise>.csv, one row per claim x window size
  summary.md    metrics vs labels.csv, threshold sweep, labels per extractor, wrong decisions
and one line in runs/INDEX.md.

Scores are cached in .cache/scores.jsonl (gitignored), keyed by model + revision + variant +
premise + hypothesis, so re-running only scores new pairs. --bench times a sample instead.
Model "<id>@int8" = dynamic int8 quantization of the Linear layers (faster, slightly different).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from nli_mock import join_sentences

HERE = Path(__file__).parent
SECTIONS, RUNS, LABELS_CSV = HERE / "sections", HERE / "runs", HERE / "labels.csv"
CACHE = HERE / ".cache" / "scores.jsonl"
LABELS = ("entailment", "neutral", "contradiction")
DEFAULT_MODELS = ["cross-encoder/nli-deberta-v3-base"]  # SPEC 6.4 candidate
SUGGESTED = [
    "cross-encoder/nli-deberta-v3-xsmall",  # fast, ~70M params
    "cross-encoder/nli-deberta-v3-base",  # SPEC candidate, ~185M
    "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",  # base size, more NLI training data
    "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",  # strong, ~435M
]
THRESHOLDS = (None, 0.3, 0.5, 0.7, 0.9)  # None = argmax label


def _crumbs(r: dict[str, Any]) -> str:
    return " > ".join(r["breadcrumb"])


# What is put in front of the premise. The window alone never names the project.
CONTEXTS: dict[str, Callable[[dict[str, Any]], str]] = {
    "none": lambda r: "",
    "breadcrumb": lambda r: f"{r['project']} > {_crumbs(r)}:\n\n",
    "sentence": lambda r: (
        f'This text is from the {r["project"]} documentation, section "{_crumbs(r)}".\n\n'
    ),
}
# Which text is the premise. "both" (derived, not scored): keep only if window AND local entail.
# "local-block" = like local, but the +-radius sentences stay inside the cited block(s); a cited
# list item also gets the lead-in sentence of the list ("... the following:"), if there is one.
PREMISES = ("window", "local", "local-block")
COLUMNS = [
    "section", "extractor", "window_size", "claim_id", "type", "status", "window_ids",
    "hypothesis", "citation", "gold", "borderline", "label", "keep_ok",
    "p_entailment", "p_neutral", "p_contradiction", "premise",
]  # fmt: skip

Key = tuple[str, str, str]  # (model spec, context, premise)


def parse_spec(spec: str) -> tuple[str, str]:
    model_id, _, variant = spec.partition("@")
    if variant not in ("", "int8"):
        raise SystemExit(f"unknown variant @{variant} (only @int8)")
    return model_id, variant or "fp32"


SOURCES = ("real", "negative", "outside", "beyond", "cross")


def source_of(extractor: str, r: dict[str, Any]) -> str:
    """Where a claim comes from: a real extractor, a hand-made negative, prompt-outside.md
    (outside = true but not in the section, beyond = overreaches the section), or a claim
    of another section (cross, see nli_mock.py cross)."""
    if extractor.startswith("x-"):
        return "cross"
    if extractor.startswith("negatives"):
        return "negative"
    return str(r.get("kind") or "real")


def load_rows(slugs: list[str], radius: int) -> list[dict[str, Any]]:
    gold = {}
    if LABELS_CSV.exists():
        with LABELS_CSV.open(encoding="utf-8") as f:
            for g in csv.DictReader(f):
                gold[(g["section"], g["extractor"], g["claim_id"])] = g
    dirs = [SECTIONS / s for s in slugs] if slugs else sorted(SECTIONS.iterdir())
    rows = []
    for d in dirs:
        chunk = json.loads((d / "chunk.json").read_text(encoding="utf-8"))
        blocks = json.loads((d / "section.json").read_text(encoding="utf-8"))["blocks"]
        sentences: dict[str, list[dict[str, Any]]] = {}
        for path in sorted((d / "pairs").glob("*.jsonl")):
            extractor, _, size = path.stem.rpartition(".windows-")
            if size not in sentences:
                wdoc = json.loads((d / f"windows-{size}.json").read_text(encoding="utf-8"))
                sentences[size] = wdoc["sentences"]
            for line in path.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                g = gold.get((d.name, extractor, r["claim_id"]), {})
                if r["status"].startswith("ok"):  # cited sentence(s) +- radius
                    lo, hi = r["cited_sentences"]
                    sents = sentences[size]
                    r["local_premise"] = join_sentences(
                        sents[max(lo - radius, 0) : hi + radius + 1]
                    )
                    r["local_block_premise"] = local_block(sents, blocks, lo, hi, radius)
                rows.append(
                    {
                        **r,
                        "section": d.name,
                        "extractor": extractor,
                        "window_size": size,
                        "project": chunk["source"]["project"],
                        "breadcrumb": chunk["breadcrumb"],
                        "gold": g.get("gold", "neutral" if extractor.startswith("x-") else ""),
                        "borderline": g.get("borderline", ""),
                        "source": source_of(extractor, r),
                    }
                )
    return rows


def local_block(
    sents: list[dict[str, Any]], blocks: list[dict[str, Any]], lo: int, hi: int, radius: int
) -> str:
    """Cited sentence(s) +- radius, without crossing into other blocks, plus a list's lead-in."""
    cited = {s["block"] for s in sents[lo : hi + 1]}
    picked = [s for s in sents[max(lo - radius, 0) : hi + radius + 1] if s["block"] in cited]
    first = min(cited)
    if blocks[first]["type"] == "list_item":
        start = first  # walk back over the bullets of the same list
        while start > 0 and blocks[start - 1]["type"] == "list_item":
            start -= 1
        lead = [s for s in sents if s["block"] == start - 1]
        if start > 0 and blocks[start - 1]["type"] == "paragraph" and lead:
            if lead[-1]["text"].rstrip().endswith(":") and lead[-1] not in picked:
                picked = [lead[-1], *picked]
    return join_sentences(picked)


def premise_text(r: dict[str, Any], ctx: str, prem: str) -> str:
    body = {"window": "premise", "local": "local_premise", "local-block": "local_block_premise"}
    return CONTEXTS[ctx](r) + r[body[prem]]


# ---------------------------------------------------------------- score cache


class ScoreCache:
    """Append-only JSONL: one line per (model, revision, variant, premise, hypothesis)."""

    def __init__(self, path: Path | None) -> None:
        self.path, self.data = path, {}  # path None = in memory only
        if path and path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                e = json.loads(line)
                self.data[e["key"]] = e

    @staticmethod
    def key(model_id: str, revision: str, variant: str, premise: str, hyp: str) -> str:
        raw = json.dumps([model_id, revision, variant, premise, hyp], ensure_ascii=False)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, k: str) -> dict[str, float] | None:
        e = self.data.get(k)
        return e["p"] if e else None

    def put(self, entries: list[dict[str, Any]]) -> None:
        if self.path is None:
            self.data.update({e["key"]: e for e in entries})
            return
        self.path.parent.mkdir(exist_ok=True)
        gi = self.path.parent / ".gitignore"
        if not gi.exists():
            gi.write_text("*\n", encoding="utf-8")
        with self.path.open("a", encoding="utf-8") as f:
            for e in entries:
                if e["key"] not in self.data:
                    self.data[e["key"]] = e
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")


# Binary fact-checking models (premise supports claim or not), mapped onto the 3 NLI labels as
# entailment = p_supported, neutral = 1 - p_supported, contradiction = 0.
MINICHECK = ("lytang/MiniCheck-DeBERTa-v3-Large", "lytang/MiniCheck-RoBERTa-Large")
HHEM = "vectara/hallucination_evaluation_model"
# HHEM needs trust_remote_code: pin the reviewed code revision instead of following main.
PINNED = {HHEM: "de9a5e6ba9ba49531a022dba17e35ffeb2a6fad8"}
# 2-label NLI models (entailment / not_entailment), mapped like the binary fact-checkers.
NLI2 = (
    "MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
    "MoritzLaurer/ModernBERT-large-zeroshot-v2.0",
)


def family(model_id: str) -> str:
    if model_id in MINICHECK:
        return "minicheck"
    return "hhem" if model_id == HHEM else "nli2" if model_id in NLI2 else "nli3"


def hub_sha(model_id: str) -> str:
    """Commit of the weights actually in the local HF cache (revision_of() is often empty)."""
    try:
        from huggingface_hub import scan_cache_dir

        for repo in scan_cache_dir().repos:
            if repo.repo_id == model_id:
                return ",".join(sorted(r.commit_hash for r in repo.revisions))
    except Exception:  # noqa: BLE001 - provenance only, never fail a run on it
        pass
    return ""


def revision_of(model_id: str) -> str:
    if model_id in PINNED:
        return PINNED[model_id]
    from transformers import AutoConfig

    return str(getattr(AutoConfig.from_pretrained(model_id), "_commit_hash", "") or "")


def checkpoint_dtype(model_id: str) -> str:
    from transformers import AutoConfig

    cfg = AutoConfig.from_pretrained(model_id)
    return str(getattr(cfg, "dtype", None) or getattr(cfg, "torch_dtype", None) or "float32")


def import_cache(run_dirs: list[str], cache: ScoreCache) -> None:
    """Seed the cache from runs 001/002 results/*.csv (same premise text).

    Those runs loaded each model in its checkpoint dtype (transformers 5 default), so the
    large model ran in fp16: its scores are cached as variant "fp16", not reused for fp32.
    """
    revisions: dict[str, str] = {}
    for rd in run_dirs:
        for path in sorted((Path(rd) / "results").glob("*.csv")):
            spec = path.stem.split("__ctx-")[0].replace("__", "/", 1)
            model_id, variant = parse_spec(spec)
            if model_id not in revisions:
                revisions[model_id] = revision_of(model_id)
            if variant == "fp32" and "float16" in checkpoint_dtype(model_id):
                variant = "fp16"
            entries = []
            with path.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    if not r["p_entailment"]:
                        continue
                    k = ScoreCache.key(
                        model_id, revisions[model_id], variant, r["premise"], r["hypothesis"]
                    )
                    p = {lbl: float(r[f"p_{lbl}"]) for lbl in LABELS}
                    entries.append({"key": k, "model": spec, "p": p, "source": str(path)})
            before = len(cache.data)
            cache.put(entries)
            print(f"{path}: {len(entries)} scores, {len(cache.data) - before} new")


# ---------------------------------------------------------------- scoring


class Scorer:
    """One loaded model; run() maps (premise, hypothesis) pairs to probabilities over LABELS."""

    def __init__(self, spec: str) -> None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self.model_id, variant = parse_spec(spec)
        self.family = family(self.model_id)
        self.truncated = 0
        # Always fp32: transformers 5 otherwise keeps the checkpoint dtype, and the large
        # model's checkpoint is fp16, which is ~10x slower on CPU (and breaks int8).
        if self.family == "hhem":
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_id, trust_remote_code=True, revision=PINNED[self.model_id],
                dtype=torch.float32,
            ).eval()  # fmt: skip
        else:
            self.tok = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_id, dtype=torch.float32
            ).eval()
        if self.family in ("nli3", "nli2"):
            cfg = self.model.config.id2label
            self.id2label = {i: str(lbl).lower() for i, lbl in cfg.items()}
            want = set(LABELS) if self.family == "nli3" else {"entailment", "not_entailment"}
            if set(self.id2label.values()) != want:
                raise SystemExit(f"{self.model_id}: unexpected labels {self.id2label}")
        if variant == "int8":
            self.model = torch.ao.quantization.quantize_dynamic(
                self.model, {torch.nn.Linear}, dtype=torch.qint8
            )

    @staticmethod
    def binary(p_supported: float) -> dict[str, float]:
        p = round(float(p_supported), 4)
        return {"entailment": p, "neutral": round(1 - p, 4), "contradiction": 0.0}

    def run(self, pairs: list[tuple[str, str]]) -> list[dict[str, float]]:
        import torch

        if self.family == "hhem":  # model.predict applies HHEM's own prompt template
            return [self.binary(x) for x in self.model.predict(pairs).tolist()]
        if self.family == "minicheck":  # MiniCheck input format: doc + eos + claim, one text
            texts = [f"{prem}{self.tok.eos_token}{hyp}" for prem, hyp in pairs]
            lengths = [len(self.tok(t)["input_ids"]) for t in texts]
            self.truncated += sum(n > 512 for n in lengths)
            enc = self.tok(
                texts, truncation=True, max_length=512, padding=True, return_tensors="pt"
            )
            probs = torch.softmax(self.model(**enc).logits, dim=-1)[:, 1].tolist()
            return [self.binary(x) for x in probs]
        enc = self.tok(
            [prem for prem, _ in pairs],
            [hyp for _, hyp in pairs],
            truncation="only_first",
            max_length=512,
            padding=True,
            return_tensors="pt",
        )
        probs = torch.softmax(self.model(**enc).logits, dim=-1).tolist()
        if self.family == "nli2":
            ent = next(i for i, lbl in self.id2label.items() if lbl == "entailment")
            return [self.binary(p[ent]) for p in probs]
        return [{self.id2label[k]: round(v, 4) for k, v in enumerate(p)} for p in probs]


def load_model(spec: str) -> Scorer:
    return Scorer(spec)


def predict(scorer: Scorer, pairs: list[tuple[str, str]], batch: int) -> list[dict[str, float]]:
    """Probabilities per (premise, hypothesis), in input order. Sorts by length to cut padding."""
    import torch

    order = sorted(range(len(pairs)), key=lambda i: len(pairs[i][0]) + len(pairs[i][1]))
    out: list[dict[str, float]] = [{} for _ in pairs]
    with torch.no_grad():
        for i in range(0, len(order), batch):
            idx = order[i : i + batch]
            for j, p in zip(idx, scorer.run([pairs[j] for j in idx]), strict=True):
                out[j] = p
    if scorer.truncated:
        print(f"WARNING {scorer.model_id}: {scorer.truncated} inputs truncated at 512 tokens")
    return out


def score(
    spec: str,
    rows: list[dict[str, Any]],
    contexts: list[str],
    premises: list[str],
    batch: int,
    cache: ScoreCache,
) -> dict[str, Any]:
    """Sets r['nli'][(spec, ctx, prem)] on scorable rows; only uncached pairs hit the model."""
    model_id, variant = parse_spec(spec)
    revision = revision_of(model_id)
    loaded = None
    timing: dict[str, Any] = {"revision": revision}
    todo = [r for r in rows if r["status"].startswith("ok")]
    for ctx in contexts:
        for prem in premises:
            texts = {id(r): premise_text(r, ctx, prem) for r in todo}
            keys = {
                id(r): ScoreCache.key(model_id, revision, variant, texts[id(r)], r["hypothesis"])
                for r in todo
            }
            missing = {keys[id(r)]: (texts[id(r)], r["hypothesis"]) for r in todo}
            missing = {k: v for k, v in missing.items() if cache.get(k) is None}
            start = time.perf_counter()
            if missing:
                loaded = loaded or load_model(spec)
                ks = list(missing)
                probs = predict(loaded, [missing[k] for k in ks], batch)
                cache.put(
                    [{"key": k, "model": spec, "p": p} for k, p in zip(ks, probs, strict=True)]
                )
            secs = round(time.perf_counter() - start, 1)
            for r in todo:
                p = cache.get(keys[id(r)])
                assert p is not None
                r.setdefault("nli", {})[(spec, ctx, prem)] = {
                    "label": max(p, key=p.__getitem__),
                    "premise": texts[id(r)],
                    **{f"p_{lbl}": p[lbl] for lbl in LABELS},
                }
            unique = len(set(keys.values()))
            timing[f"{ctx}/{prem}"] = {"seconds": secs, "scored": len(missing), "unique": unique}
            print(f"{spec} ctx={ctx} prem={prem}: {len(missing)}/{unique} new pairs in {secs}s")
    return timing


# ---------------------------------------------------------------- evaluation


def verdict(r: dict[str, Any], key: Key) -> dict[str, Any]:
    spec, ctx, prem = key
    nli = r.get("nli", {})
    if prem == "both":
        w, loc = nli.get((spec, ctx, "window")), nli.get((spec, ctx, "local"))
        if w is None or loc is None:
            v: dict[str, Any] = {"label": "dropped"}
        else:
            worst = min((w, loc), key=lambda x: x["p_entailment"])
            ent = w["label"] == loc["label"] == "entailment"
            bad = loc if loc["label"] != "entailment" else w
            v = {
                **worst,
                "label": "entailment" if ent else bad["label"],
                "premise": w["premise"] + "\n\n---\n\n" + loc["premise"],
            }
    else:
        v = {**nli.get(key, {"label": "dropped"})}
    if r["gold"]:
        v["keep_ok"] = (v["label"] == "entailment") == (r["gold"] == "entailment")
    return v


def kept(v: dict[str, Any], thr: float | None) -> bool:
    if thr is None:
        return v["label"] == "entailment"
    if v["label"] == "dropped":
        return False
    return float(v["p_entailment"]) >= thr


def metrics(
    rows: list[dict[str, Any]], key: Key, size: str, nb: bool, thr: float | None = None
) -> dict[str, Any]:
    g = [r for r in rows if r["window_size"] == size and r["gold"] and r["source"] != "cross"]
    if nb:
        g = [r for r in g if not r["borderline"]]
    pred = []
    for r in g:
        v = verdict(r, key)
        pred.append((r["gold"], v["label"], kept(v, thr)))
    tp = sum(gl == "entailment" and k for gl, _, k in pred)
    gold_e = sum(gl == "entailment" for gl, _, _ in pred)
    pred_e = sum(k for _, _, k in pred)
    gold_c = sum(gl == "contradiction" for gl, _, _ in pred)

    def pct(a: int, b: int) -> str:
        return f"{100 * a / b:.0f}%" if b else "-"

    return {
        "n": len(pred),
        "keep_acc": pct(sum((gl == "entailment") == k for gl, _, k in pred), len(pred)),
        "keep_recall": pct(tp, gold_e),
        "keep_precision": pct(tp, pred_e),
        "false_keeps": pred_e - tp,
        "contra_recall": pct(sum(gl == p == "contradiction" for gl, p, _ in pred), gold_c),
    }


def git_info() -> dict[str, Any]:
    def run(*cmd: str) -> str:
        try:
            return subprocess.run(cmd, cwd=HERE, capture_output=True, text=True).stdout.strip()
        except OSError:
            return ""

    return {
        "commit": run("git", "rev-parse", "HEAD"),
        "branch": run("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_experiment_files": bool(run("git", "status", "--porcelain", ".")),
    }


def inputs_hash(slugs: list[str]) -> dict[str, str]:
    h = hashlib.sha256()
    dirs = [SECTIONS / s for s in slugs] if slugs else sorted(SECTIONS.iterdir())
    for d in dirs:
        for p in sorted([*(d / "pairs").glob("*.jsonl"), *d.glob("windows-*.json")]):
            h.update(p.read_bytes())
    labels = hashlib.sha256(LABELS_CSV.read_bytes()).hexdigest()[:12] if LABELS_CSV.exists() else ""
    return {"pairs_windows_sha256": h.hexdigest()[:12], "labels_sha256": labels}


def new_run_dir(name: str) -> Path:
    RUNS.mkdir(exist_ok=True)
    nums = [int(p.name[:3]) for p in RUNS.iterdir() if p.is_dir() and p.name[:3].isdigit()]
    run_dir = RUNS / f"{max(nums, default=0) + 1:03d}-{name}"
    run_dir.mkdir(parents=True)
    return run_dir


def append_index(run_dir: Path, doc: str, config: dict[str, Any], what: str, note: str) -> None:
    index = RUNS / "INDEX.md"
    if not index.exists():
        index.write_text(
            "# NLI runs\n\nOne line per run; details in each run's summary.md. "
            "Findings across runs: ../FINDINGS.md\n\n| run | date | models | contexts | note |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    with index.open("a", encoding="utf-8") as f:
        models = ", ".join(m.split("/")[-1] for m in config["models"])
        f.write(
            f"| [{run_dir.name}]({run_dir.name}/{doc}) | {config['started'][:16]} "
            f"| {models} | {what} | {note} |\n"
        )


def short(spec: str) -> str:
    return spec.split("/")[-1]


def write_run(args: argparse.Namespace, rows: list[dict[str, Any]], config: dict[str, Any]) -> Path:
    run_dir = new_run_dir(args.name)
    (run_dir / "results").mkdir()
    both = {"window", "local"} <= set(config["premises"])
    prems = [*config["premises"], *(["both"] if both else [])]
    keys: list[Key] = [
        (m, c, p) for m in config["models"] for c in config["contexts"] for p in prems
    ]
    sizes = sorted({r["window_size"] for r in rows}, key=int)

    for key in keys:
        name = f"{key[0].replace('/', '__')}__ctx-{key[1]}__prem-{key[2]}.csv"
        with (run_dir / "results" / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, COLUMNS, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                v = verdict(r, key)
                w.writerow({**r, **v, "window_ids": " ".join(r.get("window_ids", []))})

    md = [f"# Run {run_dir.name}", "", f"- note: {args.note or '-'}"]
    md += [f"- {k}: `{v}`" for k, v in config.items() if k not in ("note",)]
    labelled = sum(1 for r in rows if r["gold"]) // max(len(sizes), 1)
    annot = "claude-draft" if "claude-draft" in LABELS_CSV.read_text(encoding="utf-8") else "human"
    md += ["", f"## Metrics vs labels.csv ({labelled} labelled claims, annotator: {annot})", ""]
    table = [
        "| model | context | premise | win | n | keep acc | keep recall | keep precision "
        "| false keeps | contra recall | keep acc nb |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    md += [
        "Keep = NLI says entailment (claim survives grounding). Dropped by the citation check "
        "= not kept. `nb` = without borderline labels. Premise `window` = NLI window, `local` = "
        f"cited sentence(s) +-{args.radius}, `local-block` = the same but within the cited "
        "block (+ the list's lead-in), `both` = kept only if window and local say entailment.",
        "",
        *table,
    ]
    for m, c, p in keys:
        for s in sizes:
            a, b = metrics(rows, (m, c, p), s, False), metrics(rows, (m, c, p), s, True)
            line = (
                f"| {short(m)} | {c} | {p} | {s} | {a['n']} | {a['keep_acc']} "
                f"| {a['keep_recall']} | {a['keep_precision']} | {a['false_keeps']} "
                f"| {a['contra_recall'] if family(parse_spec(m)[0]) == 'nli3' else 'n/a'} "
                f"| {b['keep_acc']} |"
            )
            md.append(line)
            table.append(line)

    md += ["", "## Should-drop claims kept, by source (argmax)", ""]
    md += [
        "Claims whose gold label is not entailment, split by where they come from. Cell = kept "
        "/ total (lower is better). `cross` = a claim scored against a related section's prose "
        "(gold neutral by default, not part of the metrics above; some may truly be entailed, "
        "review the list at the end).",
        "",
        "| model | context | premise | win | " + " | ".join(SOURCES) + " |",
        "|---|---|---|---|" + "---|" * len(SOURCES),
    ]
    for m, c, p in keys:
        for s in sizes:
            cells = []
            for src in SOURCES:
                g = [
                    r
                    for r in rows
                    if r["window_size"] == s
                    and r["source"] == src
                    and r["gold"]
                    and r["gold"] != "entailment"
                ]
                k = sum(kept(verdict(r, (m, c, p)), None) for r in g)
                cells.append(f"{k}/{len(g)}" if g else "-")
            md.append(f"| {short(m)} | {c} | {p} | {s} | " + " | ".join(cells) + " |")

    md += ["", "## Threshold sweep", ""]
    md += [
        "Keep if p_entailment >= threshold (argmax = keep if entailment is the top label). "
        "Cell = keep recall / false keeps.",
        "",
    ]
    heads = ["argmax" if t is None else f">= {t}" for t in THRESHOLDS]
    md += ["| model | context | premise | win | " + " | ".join(heads) + " |"]
    md += ["|---|---|---|---|" + "---|" * len(heads)]
    for m, c, p in keys:
        for s in sizes:
            cells = []
            for t in THRESHOLDS:
                x = metrics(rows, (m, c, p), s, False, t)
                cells.append(f"{x['keep_recall']} / {x['false_keeps']}")
            md.append(f"| {short(m)} | {c} | {p} | {s} | " + " | ".join(cells) + " |")

    md += ["", "## Labels per extractor", ""]
    md += ["| model | context | premise | win | section | extractor | ent | neu | con | dropped |"]
    md += ["|---|---|---|---|---|---|---|---|---|---|"]
    groups = sorted({(r["window_size"], r["section"], r["extractor"]) for r in rows})
    for m, c, p in keys:
        for s, sec, ext in groups:
            g = [
                verdict(r, (m, c, p))["label"]
                for r in rows
                if (r["window_size"], r["section"], r["extractor"]) == (s, sec, ext)
            ]
            n = {lbl: g.count(lbl) for lbl in (*LABELS, "dropped")}
            md.append(
                f"| {short(m)} | {c} | {p} | {s} | {sec} | {ext} | {n['entailment']} "
                f"| {n['neutral']} | {n['contradiction']} | {n['dropped']} |"
            )

    md += ["", "## Wrong keep / drop decisions (argmax)", ""]
    md += [
        "| model | context | premise | win | section | extractor | id | gold | NLI | p_ent "
        "| claim |"
    ]
    md += ["|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, c, p in keys:
        for r in rows:
            v = verdict(r, (m, c, p))
            if v.get("keep_ok") is False and r["source"] != "cross":
                gold = r["gold"] + (" (borderline)" if r["borderline"] else "")
                md.append(
                    f"| {short(m)} | {c} | {p} | {r['window_size']} | {r['section']} "
                    f"| {r['extractor']} | {r['claim_id']} | {gold} | {v['label']} "
                    f"| {v.get('p_entailment', '')} | {r['hypothesis']} |"
                )
    md += ["", "## Cross-section pairs kept (argmax)", ""]
    md += [
        "| model | context | premise | win | premise section | claim from | id | p_ent | claim |"
    ]
    md += ["|---|---|---|---|---|---|---|---|---|"]
    for m, c, p in keys:
        for r in rows:
            if r["source"] == "cross" and kept(verdict(r, (m, c, p)), None):
                md.append(
                    f"| {short(m)} | {c} | {p} | {r['window_size']} | {r['section']} "
                    f"| {r['extractor'][2:]} | {r['claim_id']} "
                    f"| {verdict(r, (m, c, p)).get('p_entailment', '')} | {r['hypothesis']} |"
                )
    (run_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (run_dir / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    what = ", ".join(config["contexts"]) + " / " + ", ".join(prems)
    append_index(run_dir, "summary.md", config, what, args.note)
    print("\n" + "\n".join(table))
    return run_dir


# ---------------------------------------------------------------- benchmark


def bench(args: argparse.Namespace, rows: list[dict[str, Any]], config: dict[str, Any]) -> Path:
    """Time a fixed sample of the longest-premise pairs per model spec x thread count. No cache."""
    import torch

    ctx, prem = args.context[0], args.premise[0]
    biggest = max((r["window_size"] for r in rows), key=int)
    pool = {
        (premise_text(r, ctx, prem), r["hypothesis"])
        for r in rows
        if r["status"].startswith("ok") and r["window_size"] == biggest
    }
    ordered = sorted(pool, key=lambda x: len(x[0]) + len(x[1]))
    step = max(len(ordered) // args.bench, 1)
    sample = ordered[::step][: args.bench]
    default_threads = torch.get_num_threads()
    threads = [t or default_threads for t in args.threads]
    config["bench"] = {"pairs": len(sample), "default_threads": default_threads, "results": []}

    lines = [
        "| model | threads | batch | seconds | pairs/s | vs first row | max abs dp_ent vs fp32 "
        "| label agreement vs fp32 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    fp32: dict[str, list[dict[str, float]]] = {}
    for spec in args.model or DEFAULT_MODELS:
        loaded = load_model(spec)
        model_id, variant = parse_spec(spec)
        for t in threads:
            torch.set_num_threads(t)
            predict(loaded, sample[: args.batch], args.batch)  # warm-up
            start = time.perf_counter()
            probs = predict(loaded, sample, args.batch)
            secs = time.perf_counter() - start
            if variant == "fp32":
                fp32.setdefault(model_id, probs)
            base = config["bench"]["results"]
            first = next((b["seconds"] for b in base if b["model"].split("@")[0] == model_id), secs)
            ref = fp32.get(model_id)
            dp = agree = "-"
            if ref is not None and variant != "fp32":
                pairs = list(zip(ref, probs, strict=True))
                dp = f"{max(abs(a['entailment'] - b['entailment']) for a, b in pairs):.3f}"
                same = sum(
                    max(a, key=a.__getitem__) == max(b, key=b.__getitem__)
                    for a, b in zip(ref, probs, strict=True)
                )
                agree = f"{same}/{len(probs)}"
            base.append({"model": spec, "threads": t, "seconds": round(secs, 1)})
            line = (
                f"| {short(spec)} | {t} | {args.batch} | {secs:.1f} | {len(sample) / secs:.2f} "
                f"| {first / secs:.2f}x | {dp} | {agree} |"
            )
            lines.append(line)
            print(line, flush=True)
    config["finished"] = datetime.now().isoformat(timespec="seconds")

    run_dir = new_run_dir(args.name)
    md = [
        f"# Bench {run_dir.name}",
        "",
        f"- note: {args.note or '-'}",
        f"- sample: {len(sample)} pairs, evenly spread by length over the largest window size, "
        f"context `{ctx}`, premise `{prem}`; one warm-up batch before timing",
        f"- torch default threads: {default_threads}",
        *[f"- {k}: `{v}`" for k, v in config.items() if k not in ("note", "bench")],
        "",
        *lines,
    ]
    (run_dir / "bench.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (run_dir / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    append_index(run_dir, "bench.md", config, "bench", args.note)
    return run_dir


# ---------------------------------------------------------------- CLI


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("slugs", nargs="*", help="section folder names (default: all)")
    p.add_argument(
        "--model",
        action="append",
        help=f"HF model id, repeatable, '@int8' suffix = quantized (default: {DEFAULT_MODELS[0]})"
        "\nsuggested:\n  " + "\n  ".join(SUGGESTED),
    )
    p.add_argument(
        "--context", nargs="+", choices=list(CONTEXTS), default=["none"],
        help="what to put in front of the premise (several = compare them)",
    )  # fmt: skip
    p.add_argument(
        "--premise", nargs="+", choices=PREMISES, default=["window"],
        help="window = NLI window, local = cited sentence(s) +- radius, local-block = local "
        "within the cited block (+ list lead-in); window and local given = also 'both'",
    )  # fmt: skip
    p.add_argument("--radius", type=int, default=1, help="sentences around the citation (local)")
    p.add_argument("--name", default="run", help="short run name, used in the folder name")
    p.add_argument("--note", default="", help="one line: why this run exists")
    p.add_argument("--batch", type=int, default=8)
    p.add_argument(
        "--threads", type=int, nargs="+", default=[0],
        help="torch CPU threads (0 = torch default); several only with --bench",
    )  # fmt: skip
    p.add_argument("--bench", type=int, metavar="N", help="time N sample pairs, no scoring run")
    p.add_argument("--no-cache", action="store_true", help="ignore and don't write the score cache")
    p.add_argument(
        "--import-cache", nargs="+", metavar="RUN_DIR",
        help="seed the score cache from older runs' results/*.csv and exit",
    )  # fmt: skip
    args = p.parse_args()

    cache = ScoreCache(None if args.no_cache else CACHE)
    if args.import_cache:
        import_cache(args.import_cache, cache)
        return

    rows = load_rows(args.slugs, args.radius)
    if not rows:
        raise SystemExit("no pairs found, run `nli_mock.py pair` first")

    import torch
    import transformers

    models = args.model or DEFAULT_MODELS
    config: dict[str, Any] = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "models": models,
        "contexts": args.context,
        "premises": args.premise,
        "radius": args.radius,
        "sections": args.slugs or "all",
        "batch": args.batch,
        "git": git_info(),
        "inputs": inputs_hash(args.slugs),
        "versions": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
        },
    }
    if args.bench:
        run_dir = bench(args, rows, config)
        print(f"\n-> {run_dir.relative_to(HERE).as_posix()}/bench.md")
        return

    if args.threads[0]:
        torch.set_num_threads(args.threads[0])
    config["threads"] = torch.get_num_threads()
    config["seconds"] = {}
    for spec in models:
        config["seconds"][spec] = score(spec, rows, args.context, args.premise, args.batch, cache)
    config["hub_sha"] = {spec: hub_sha(parse_spec(spec)[0]) for spec in models}
    config["finished"] = datetime.now().isoformat(timespec="seconds")
    run_dir = write_run(args, rows, config)
    print(f"\n-> {run_dir.relative_to(HERE).as_posix()}/summary.md")


if __name__ == "__main__":
    main()
