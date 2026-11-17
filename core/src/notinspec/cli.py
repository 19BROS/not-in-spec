import argparse
import statistics
import sys
from pathlib import Path

from notinspec import __version__
from notinspec.adapters.canonical import canonical_json
from notinspec.chunking import (
    DEFAULT_SOFT_LIMIT,
    DEFAULT_WINDOW_TOKENS,
    chunk_documents,
    load_documents,
    nli_windows,
)
from notinspec.config import load_config
from notinspec.ingestion import ingest, plan_ingestion
from notinspec.report import build_results, write_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notinspec")
    parser.add_argument("--version", action="version", version=f"notinspec {__version__}")
    commands = parser.add_subparsers(dest="command")

    chunk = commands.add_parser("chunk", help="split Markdown docs into chunks and NLI windows")
    chunk.add_argument("root", type=Path, help="docs root; chunk sources are relative to it")
    chunk.add_argument(
        "-g", "--glob", action="append", help="file pattern under root (default: **/*.md)"
    )
    chunk.add_argument("--soft-limit", type=_positive_int, default=DEFAULT_SOFT_LIMIT)
    chunk.add_argument("--window-tokens", type=_positive_int, default=DEFAULT_WINDOW_TOKENS)
    chunk.add_argument(
        "--overlap-tokens", type=int, help="window overlap (default: 1/5 of --window-tokens)"
    )
    output = chunk.add_mutually_exclusive_group()
    output.add_argument("--list", action="store_true", help="one line per chunk")
    output.add_argument("--json", action="store_true", help="chunks and windows as JSON")

    ci = commands.add_parser(
        "ci",
        aliases=["ingest"],
        help="process configured docs and write artifacts (ingestion only; no LLM evaluation)",
        description="Ingestion prototype: Markdown chunking and OpenAPI normalization. "
        "Processes all inputs; does not call LLMs or evaluate L0-L4.",
    )
    ci.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    ci.add_argument("--out", type=Path, default=Path("notinspec-out"))
    ci.add_argument("--soft-limit", type=_positive_int, default=DEFAULT_SOFT_LIMIT)
    ci.add_argument(
        "--dry-run",
        action="store_true",
        help="check config and list inputs without parsing or writing",
    )

    args = parser.parse_args(argv)
    # A crash must return 2, never 1 (reserved for an evaluated documentation regression).
    try:
        if args.command == "chunk":
            return _chunk(args)
        if args.command in ("ci", "ingest"):
            return _ingest(args)
    except Exception as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    parser.print_help()
    return 0


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _ingest(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if args.dry_run:
        plan, warnings = plan_ingestion(config, output=args.out)
        print(f"Dry run: {len(plan)} input files selected.")
        for item in plan:
            print(f"  {item.kind}: {item.source}")
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        print("No documents parsed, no files written, no LLM evaluation.")
        return 0
    print("Processing documentation (ingestion only; no LLM calls).")
    ingestion = ingest(config, output=args.out, soft_limit=args.soft_limit)
    results = build_results(ingestion, config.root)
    write_artifacts(args.out, ingestion, results)
    counts = results["ingestion"]
    print(
        f"Processed {counts['files']} files: {counts['chunks']} chunks, "
        f"{counts['operations']} OpenAPI operations."
    )
    for warning in ingestion.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    print(f"Artifacts: {args.out.resolve()}")
    print("LLM evaluation: not run (no pass/fail verdict).")
    return 0


def _chunk(args: argparse.Namespace) -> int:
    if not args.root.is_dir():
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2
    documents = load_documents(args.root, args.glob or ["**/*.md"])
    chunks = chunk_documents(documents, soft_limit=args.soft_limit)
    overlap = args.window_tokens // 5 if args.overlap_tokens is None else args.overlap_tokens
    windows = {
        c.id: nli_windows(c, max_tokens=args.window_tokens, overlap_tokens=overlap) for c in chunks
    }

    if args.json:
        sys.stdout.buffer.write(canonical_json({"chunks": chunks, "windows": windows}, pretty=True))
        return 0
    if args.list:
        print("tokens  part  windows  breadcrumb")
        for c in chunks:
            flag = "  OVERSIZED" if c.oversized else ""
            part = f"{c.part}/{c.parts}"
            print(f"{c.tokens:>6}  {part:>4}  {len(windows[c.id]):>7}  {c.breadcrumb}{flag}")
        return 0

    sizes = [c.tokens for c in chunks] or [0]
    counts = [len(w) for w in windows.values()] or [0]
    all_windows = [w for ws in windows.values() for w in ws]
    split = {c.section_id for c in chunks if c.parts > 1}
    print(
        f"{len(documents)} files, {len(chunks)} chunks from {len({c.section_id for c in chunks})}"
        f" sections ({len(split)} split into parts, "
        f"{sum(c.oversized for c in chunks)} oversized)"
    )
    print(f"chunk tokens: median {statistics.median(sizes):.0f}, max {max(sizes)}")
    print(
        f"NLI windows: {len(all_windows)}, per chunk median {statistics.median(counts):.0f}, "
        f"max {max(counts)}, {sum(not w for w in windows.values())} chunks without prose, "
        f"{sum(w.oversized for w in all_windows)} oversized sentences"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
