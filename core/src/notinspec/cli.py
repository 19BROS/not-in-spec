import argparse
import fnmatch
import json
import statistics
import sys
import uuid
from collections.abc import Callable
from dataclasses import asdict
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
from notinspec.claims import (
    DEFAULT_EXTRACTORS,
    PROMPT_VERSION,
    JsonlCallLog,
    JsonlClaimStore,
    extract_claims,
    extractor_for,
)
from notinspec.config import load_config
from notinspec.ingestion import ingest, plan_ingestion
from notinspec.report import build_results, write_artifacts
from notinspec.runner import (
    GROQ,
    PROVIDERS,
    ChatRequest,
    Completion,
    Message,
    ModelClient,
    ModelUnavailable,
    OpenAICompatProvider,
    Provider,
    ProviderError,
    QuotaExhausted,
    RecordingProvider,
    TransientError,
)
from notinspec.verify import ANSWER_SCHEMA, parse_answer

# bump when the shape of claims.json changes
CLAIMS_SCHEMA_VERSION = 1

# ad-hoc instruction for trying a model by hand; real prompts come from the generator's templates
_ASK_SYSTEM = (
    "Answer with only a JSON object describing the HTTP request to send, "
    "matching this JSON Schema:\n"
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
    chunk.add_argument("--project", help="root of every breadcrumb (default: name of root)")
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
        description="Ingestion prototype: Sphinx XML and Markdown chunking, OpenAPI "
        "normalization. "
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

    ask = commands.add_parser("ask", help="ask one model one question (Groq: needs GROQ_API_KEY)")
    ask.add_argument("prompt")
    ask.add_argument("--model", help=f"provider's model ID (default on Groq: {GROQ.default_model})")
    ask.add_argument(
        "--no-schema", action="store_true", help="don't send the answer schema as response_format"
    )
    ask.add_argument("--record", type=Path, help="save the raw response as a fake-provider fixture")
    _provider_option(ask)

    models = commands.add_parser("models", help="list the provider's active models")
    models.add_argument(
        "--structured", action="store_true", help="only models known to take a JSON schema"
    )
    models.add_argument(
        "--probe",
        action="store_true",
        help="ask each listed model one question with the answer schema (one request per model)",
    )
    _provider_option(models)

    claims = commands.add_parser("claims", help="claims from prose (SPEC §6.4)")
    claims_commands = claims.add_subparsers(dest="claims_command")
    extract = claims_commands.add_parser(
        "extract",
        help="extract claims with the LLM extractors (Groq: needs GROQ_API_KEY); no grounding",
        description="Reads the configured docs, sends every prose chunk to each extractor and "
        "writes claims.json. Every request is appended to llm-calls.jsonl; claims of unchanged "
        "chunks are reused from claims-store.jsonl in the output folder.",
    )
    extract.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    extract.add_argument("--out", type=Path, default=Path("notinspec-out"))
    extract.add_argument(
        "--source",
        action="append",
        help="only chunks whose source (Sphinx docname or file path) matches this glob; "
        "repeatable (default: claims.sources in the config, else every chunk)",
    )
    extract.add_argument(
        "--extractor",
        action="append",
        metavar="MODEL",
        help="extractor model ID; repeatable (default: claims.extractors in the config, else "
        + ", ".join(s.model for s in DEFAULT_EXTRACTORS)
        + ")",
    )
    extract.add_argument("--soft-limit", type=_positive_int, default=DEFAULT_SOFT_LIMIT)
    extract.add_argument("--no-reuse", action="store_true", help="ask again for every chunk")
    extract.add_argument("--run-id", help="run ID for the response cache (default: random)")
    extract.add_argument(
        "--record", type=Path, help="also save the raw responses as a fake-provider fixture"
    )
    _provider_option(extract)

    args = parser.parse_args(argv)
    # A crash must return 2, never 1 (reserved for an evaluated documentation regression).
    try:
        if args.command == "claims":
            if args.claims_command == "extract":
                return _extract_claims(args)
            claims.print_help()
            return 0
        if args.command == "chunk":
            return _chunk(args)
        if args.command in ("ci", "ingest"):
            return _ingest(args)
        if args.command == "ask":
            config = PROVIDERS[args.provider]
            model = args.model or config.default_model
            if model is None:
                raise ValueError(f"--model is required for {config.name}")
            provider = OpenAICompatProvider.from_env(config)
            return _ask(provider, model, args.prompt, schema=not args.no_schema, record=args.record)
        if args.command == "models":
            provider = OpenAICompatProvider.from_env(PROVIDERS[args.provider])
            return _models(provider, structured_only=args.structured, probe=args.probe)
    except Exception as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    parser.print_help()
    return 0


def _provider_option(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "--provider", choices=sorted(PROVIDERS), default=GROQ.name, help="default: %(default)s"
    )


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _ingest(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if args.dry_run:
        plan, warnings = plan_ingestion(config, output=args.out)
        print(f"Dry run: {len(plan)} inputs selected.")
        for item in plan:
            if item.kind == "sphinx":
                print(
                    f"  sphinx: {item.source}/ ({item.xml_files} XML files, "
                    f"Sphinx {item.sphinx_version})"
                )
            else:
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
    print(
        f"Inventory: {counts['symbols']} symbols, {counts['changes']} changes, "
        f"{counts['conflicts']} conflicts between sources."
    )
    for warning in ingestion.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    print(f"Artifacts: {args.out.resolve()}")
    print("LLM evaluation: not run (no pass/fail verdict).")
    return 0


class _LazyProvider:
    """Builds the live provider on the first request, so a fully reused run needs no API key.

    A provider that cannot be built (no key) stops the whole command instead of failing every
    chunk: it is not a per-chunk provider error.
    """

    def __init__(self, factory: Callable[[], Provider]) -> None:
        self._factory = factory
        self._provider: Provider | None = None

    def complete(self, request: ChatRequest) -> Completion:
        if self._provider is None:
            try:
                self._provider = self._factory()
            except ProviderError as e:
                raise RuntimeError(str(e)) from e
        return self._provider.complete(request)


def _live_provider(name: str) -> Provider:
    """Seam for tests: the CLI never calls a real provider in CI."""
    return OpenAICompatProvider.from_env(PROVIDERS[name])


def _extract_claims(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    models = args.extractor or list(config.claims.extractors)
    specs = tuple(extractor_for(m) for m in models) if models else DEFAULT_EXTRACTORS
    patterns = args.source or list(config.claims.sources)
    ingestion = ingest(config, output=args.out, soft_limit=args.soft_limit)
    chunks = [
        c
        for c in ingestion.chunks
        if not patterns or any(fnmatch.fnmatchcase(c.source, p) for p in patterns)
    ]
    if patterns and not chunks:
        raise ValueError(f"no chunk source matches {', '.join(patterns)}")
    args.out.mkdir(parents=True, exist_ok=True)
    calls = JsonlCallLog(args.out / "llm-calls.jsonl")
    store = None if args.no_reuse else JsonlClaimStore(args.out / "claims-store.jsonl")
    provider_name: str = args.provider
    live = RecordingProvider(_LazyProvider(lambda: _live_provider(provider_name)))
    client = ModelClient(live, limits=PROVIDERS[provider_name].limiters())
    run_id = args.run_id or uuid.uuid4().hex
    print(f"Extracting claims from {len(chunks)} chunks with {len(specs)} extractors.")
    results = []
    for spec in specs:
        result = extract_claims(chunks, spec, client, run_id, calls, store=store)
        results.append(result)
        print(
            f"  {spec.name}: {len(result.claims)} claims, {result.asked} chunks asked, "
            f"{result.reused} reused, {result.without_prose} without prose, "
            f"{len(result.failures)} failed, {len(result.problems)} claims skipped"
            + (f"; stopped: {result.stopped}" if result.stopped else "")
        )
    if args.record is not None:
        live.save(args.record)
    output = {
        "schema_version": CLAIMS_SCHEMA_VERSION,
        "project": ingestion.project,
        "input_hash": ingestion.input_hash,
        "prompt_version": PROMPT_VERSION,
        "sources": sorted(patterns),
        "chunks": len(chunks),
        "extractors": [r.extractor for r in results],
        "claims": [c for r in results for c in r.claims],
        "failures": [f for r in results for f in r.failures],
        "problems": [p for r in results for p in r.problems],
    }
    (args.out / "claims.json").write_bytes(canonical_json(output, pretty=True))
    print(f"Claims: {(args.out / 'claims.json').resolve()}")
    stopped = [r for r in results if r.stopped]
    for r in stopped:
        print(f"stopped: {r.extractor.name}: {r.stopped}; run again to continue", file=sys.stderr)
    return 2 if stopped else 0


def _chunk(args: argparse.Namespace) -> int:
    if not args.root.is_dir():
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2
    documents = load_documents(args.root, args.glob or ["**/*.md"])
    project = args.project or args.root.resolve().name
    chunks = chunk_documents(documents, project=project, soft_limit=args.soft_limit)
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


def _answer_request(model: str, prompt: str, *, schema: bool) -> ChatRequest:
    return ChatRequest(
        model=model,
        messages=(
            Message("system", _ASK_SYSTEM + json.dumps(ANSWER_SCHEMA)),
            Message("user", prompt),
        ),
        response_schema=ANSWER_SCHEMA if schema else None,
    )


def _ask(
    provider: OpenAICompatProvider, model: str, prompt: str, *, schema: bool, record: Path | None
) -> int:
    live = RecordingProvider(provider)
    # one retry at most: trying by hand shouldn't burn the daily budget
    completion = ModelClient(live, max_attempts=2).ask(
        "cli", _answer_request(model, prompt, schema=schema)
    )
    if record is not None:
        live.save(record)

    answer = parse_answer(completion.content, refusal=completion.refusal)
    print(f"model:   {completion.model}")
    print(f"finish:  {completion.finish_reason}")
    print(f"content: {completion.content}")
    if answer.request is not None:
        print(f"parsed:  {json.dumps(asdict(answer.request), ensure_ascii=False)}")
    else:
        print(f"parsed:  {answer.cause} ({answer.detail})")
    return 0


# a question every model can answer, so a failed probe means the schema, not the task
_PROBE_PROMPT = "Fetch the pet with ID 1 from the Petstore API: GET /pets/1."


def _models(provider: OpenAICompatProvider, *, structured_only: bool, probe: bool) -> int:
    client = ModelClient(provider, limits=provider.config.limiters(), max_attempts=1)
    listed = [m for m in provider.list_models() if m.structured_output or not structured_only]
    for done, m in enumerate(listed):
        structured = "structured-output" if m.structured_output else "-"
        line = f"{m.id:<50} {m.context_length or '?':>8}  {structured:<17}"
        if probe:
            try:
                line += f"  probe: {_probe(client, m.id)}"
            except QuotaExhausted as e:
                print(f"stopped: {e} ({done} of {len(listed)} models probed)", file=sys.stderr)
                return 2
        print(line, flush=True)
    return 0


def _probe(client: ModelClient, model: str) -> str:
    """`rejected` only when the provider refused the request itself, e.g. the schema."""
    try:
        completion = client.ask("probe", _answer_request(model, _PROBE_PROMPT, schema=True))
    except QuotaExhausted:
        raise
    except ModelUnavailable as e:
        return f"unavailable ({str(e)[:120]})"
    except TransientError as e:  # rate limits included: says nothing about the schema
        return f"unknown ({type(e).__name__}: {str(e)[:120]})"
    except ProviderError as e:
        return f"rejected ({type(e).__name__}: {str(e)[:120]})"
    answer = parse_answer(completion.content, refusal=completion.refusal)
    if answer.request is not None:
        return "ok"
    return f"answered, {answer.cause} (finish: {completion.finish_reason})"


if __name__ == "__main__":
    sys.exit(main())
