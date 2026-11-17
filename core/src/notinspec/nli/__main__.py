"""python -m notinspec.nli fetch | bench  (in the worker: docker compose run --rm worker ...)"""

import argparse
import json
import os
import platform
import sys

from notinspec.nli.bench import bench, fetch, torch_threads
from notinspec.nli.local import MODEL_ID, REVISION, NliUnavailable, TransformersNli


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m notinspec.nli")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch", help="download the pinned NLI model into HF_HOME (once)")
    b = commands.add_parser("bench", help="time the NLI model on sample pairs")
    b.add_argument("--pairs", type=int, default=64)
    b.add_argument("--threads", type=int, help="torch CPU threads (default: torch's)")
    b.add_argument("--batch", type=int, default=8)
    args = parser.parse_args(argv)
    try:
        if args.command == "fetch":
            print(fetch())
            return 0
        model = TransformersNli(threads=args.threads, batch_size=args.batch)
        result = bench(model, args.pairs)
    except NliUnavailable as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    report = {
        "model": MODEL_ID,
        "revision": REVISION,
        "machine": platform.machine(),
        "cpus": os.cpu_count(),
        "threads": torch_threads(),
        "batch": args.batch,
        "pairs": result.pairs,
        "load_s": round(result.load_seconds, 1),
        "score_s": round(result.seconds, 1),
        "pairs_per_s": round(result.pairs_per_second, 2),
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
