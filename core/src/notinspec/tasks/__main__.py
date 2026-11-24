"""Local entry point: built Sphinx XML → inventory → unapproved task candidates."""

import argparse
from pathlib import Path

from notinspec.adapters.canonical import content_hash
from notinspec.chunking import chunk_blocks
from notinspec.inventory import build_inventory
from notinspec.sphinx import read_sphinx_xml
from notinspec.tasks import (
    GenerationContext,
    GenerationResult,
    generate_l0,
    generate_l1,
    load,
    save,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sphinx_xml", type=Path)
    parser.add_argument("--project", required=True)
    parser.add_argument("--docs-version", required=True)
    parser.add_argument(
        "--api-version", help="PEP 440 version for Change evidence when label is main/latest"
    )
    parser.add_argument("--out", type=Path, required=True, help="new candidate JSON file")
    parser.add_argument("--reuse", type=Path, help="reuse frozen candidates from an earlier export")
    args = parser.parse_args(argv)
    xml = read_sphinx_xml(args.sphinx_xml)
    chunks = tuple(c for d in xml.documents for c in chunk_blocks(d, project=args.project))
    built = build_inventory(chunks)
    context = GenerationContext(
        args.project, args.docs_version, content_hash(dict(xml.files)), api_version=args.api_version
    )
    existing = load(args.reuse).items if args.reuse else ()
    results = [
        generate(
            built.inventory,
            context=context,
            chunks=chunks,
            conflicts=built.conflicts,
            existing=existing,
        )
        for generate in (generate_l0, generate_l1)
    ]
    result = GenerationResult(
        tuple(i for r in results for i in r.items), tuple(s for r in results for s in r.skipped)
    )
    save(args.out, result)
    print(f"{len(result.items)} candidates, {len(result.skipped)} skipped; {args.out}")
    for warning in (*xml.warnings, *built.warnings):
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
