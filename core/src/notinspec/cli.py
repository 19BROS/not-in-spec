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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notinspec")
    parser.add_argument("--version", action="version", version=f"notinspec {__version__}")
    commands = parser.add_subparsers(dest="command")

    chunk = commands.add_parser("chunk", help="split Markdown docs into chunks and NLI windows")
    chunk.add_argument("root", type=Path, help="docs root; chunk sources are relative to it")
    chunk.add_argument(
        "-g", "--glob", action="append", help="file pattern under root (default: **/*.md)"
    )
    chunk.add_argument("--soft-limit", type=int, default=DEFAULT_SOFT_LIMIT)
    chunk.add_argument("--window-tokens", type=int, default=DEFAULT_WINDOW_TOKENS)
    chunk.add_argument(
        "--overlap-tokens", type=int, help="window overlap (default: 1/5 of --window-tokens)"
    )
    output = chunk.add_mutually_exclusive_group()
    output.add_argument("--list", action="store_true", help="one line per chunk")
    output.add_argument("--json", action="store_true", help="chunks and windows as JSON")

    args = parser.parse_args(argv)
    if args.command == "chunk":
        return _chunk(args)
    parser.print_help()
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
