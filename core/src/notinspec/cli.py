import argparse
import fnmatch
import json
import os
import shutil
import statistics
import sys
import uuid
from collections.abc import Callable, Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

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
    ClaimsRun,
    ExtractionResult,
    JsonlCallLog,
    JsonlClaimStore,
    extract_claims,
    extractor_for,
    run_claims,
)
from notinspec.config import load_config
from notinspec.demo import build_demo_run, new_run_id
from notinspec.ingestion import ingest, plan_ingestion
from notinspec.nli import NliModel, RecordingNli, TransformersNli
from notinspec.pack import pack_inputs
from notinspec.report import build_results, claim_counts, render_claims, write_artifacts
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

# bump when the shape of extracted-claims.json changes
CLAIMS_SCHEMA_VERSION = 1
# bump when the shape of claims.json (grounded claims) changes
GROUNDED_SCHEMA_VERSION = 1

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
        "writes extracted-claims.json (not grounded yet). Every request is appended to "
        "llm-calls.jsonl; claims of unchanged chunks are reused from claims-store.jsonl in the "
        "output folder.",
    )
    _claims_options(extract)
    run = claims_commands.add_parser(
        "run",
        help="extract and ground claims (Groq: needs GROQ_API_KEY; NLI: needs notinspec[nli])",
        description="Extracts claims like `claims extract`, then grounds each one: citation "
        "check, NLI premise, NLI with the local model, identifier check. Writes claims.json "
        "(every claim with its status, dropped ones too) and claims.html.",
    )
    _claims_options(run)
    run.add_argument(
        "--record-nli", type=Path, help="also save the NLI scores as a recorded-NLI fixture"
    )

    pack = commands.add_parser(
        "pack",
        help="pack the configured inputs into the upload archive (SPEC 11.1)",
        description="Writes the tar.gz the GitHub Action uploads to our service. Selects "
        "inputs like `ci --dry-run`; the same inputs always give the same bytes.",
    )
    pack.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    pack.add_argument("--out", type=Path, default=Path("inputs.tar.gz"))

    demo = commands.add_parser(
        "demo",
        help="ingest and (optionally) run claims into one run folder for the web demo",
        description="Runs `ci` and `claims run` into <runs-dir>/<run id>/ and writes run.json "
        "last (the API lists only folders with it). Claims need GROQ_API_KEY for chunks not "
        "in the claims store and notinspec[nli].",
    )
    demo.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    demo.add_argument("--runs-dir", type=Path, default=Path("tmp/runs"))
    demo.add_argument(
        "--source", action="append", help="claims only from chunks matching this glob; repeatable"
    )
    demo.add_argument("--extractor", action="append", metavar="MODEL", help="repeatable")
    demo.add_argument("--no-claims", action="store_true", help="ingestion only, no LLM or NLI")
    demo.add_argument(
        "--claims-store",
        type=Path,
        help="claims-store.jsonl copied into the run first, so stored answers are reused",
    )
    _provider_option(demo)

    args = parser.parse_args(argv)
    # A crash must return 2, never 1 (reserved for an evaluated documentation regression).
    try:
        if args.command == "claims":
            if args.claims_command == "extract":
                return _extract_claims(args)
            if args.claims_command == "run":
                return _run_claims(args)
            claims.print_help()
            return 0
        if args.command == "chunk":
            return _chunk(args)
        if args.command == "demo":
            return _demo(args)
        if args.command in ("ci", "ingest"):
            return _ingest(args)
        if args.command == "pack":
            names = pack_inputs(args.config, args.out)
            print("\n".join(names))
            print(f"Packed {len(names)} files, {args.out.stat().st_size} bytes: {args.out}")
            return 0
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


def _claims_options(command: argparse.ArgumentParser) -> None:
    command.add_argument("--config", type=Path, default=Path("notinspec.yaml"))
    command.add_argument("--out", type=Path, default=Path("notinspec-out"))
    command.add_argument(
        "--source",
        action="append",
        help="only chunks whose source (Sphinx docname or file path) matches this glob; "
        "repeatable (default: every chunk)",
    )
    command.add_argument(
        "--extractor",
        action="append",
        metavar="MODEL",
        help="extractor model ID; repeatable (default: "
        + ", ".join(s.model for s in DEFAULT_EXTRACTORS)
        + ")",
    )
    command.add_argument("--soft-limit", type=_positive_int, default=DEFAULT_SOFT_LIMIT)
    command.add_argument(
        "--no-reuse",
        action="store_true",
        help="ask again for every chunk and replace its stored claims",
    )
    command.add_argument("--run-id", help="run ID for the response cache (default: random)")
    command.add_argument(
        "--record", type=Path, help="also save the raw responses as a fake-provider fixture"
    )
    _provider_option(command)


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


def _nli_model() -> NliModel:
    """The NLI model, already loaded, so a missing extra or model stops a run before any LLM
    call. Seam for tests: CI replays recorded NLI scores and never loads the real model."""
    model = TransformersNli()
    model.load()
    return model


class _ClaimsInput:
    """What both claims commands read: the docs, the chosen chunks, extractors and logs."""

    def __init__(self, args: argparse.Namespace) -> None:
        config = load_config(args.config)
        self.specs = (
            tuple(extractor_for(m) for m in args.extractor)
            if args.extractor
            else DEFAULT_EXTRACTORS
        )
        self.patterns: list[str] = args.source or []
        self.ingestion = ingest(config, output=args.out, soft_limit=args.soft_limit)
        self.chunks = [
            c
            for c in self.ingestion.chunks
            if not self.patterns or any(fnmatch.fnmatchcase(c.source, p) for p in self.patterns)
        ]
        if self.patterns and not self.chunks:
            raise ValueError(f"no chunk source matches {', '.join(self.patterns)}")
        args.out.mkdir(parents=True, exist_ok=True)
        self.calls = JsonlCallLog(args.out / "llm-calls.jsonl")
        self.store = JsonlClaimStore(args.out / "claims-store.jsonl")
        for warning in self.store.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        provider_name: str = args.provider
        self.live = RecordingProvider(_LazyProvider(lambda: _live_provider(provider_name)))
        self.client = ModelClient(self.live, limits=PROVIDERS[provider_name].limiters())
        self.run_id: str = args.run_id or uuid.uuid4().hex
        self.reuse = not args.no_reuse
        self.record: Path | None = args.record

    def header(self) -> dict[str, Any]:
        return {
            "project": self.ingestion.project,
            "input_hash": self.ingestion.input_hash,
            "prompt_version": PROMPT_VERSION,
            "sources": sorted(self.patterns),
            "chunks": len(self.chunks),
        }


def _print_extraction(result: ExtractionResult) -> None:
    print(
        f"  {result.extractor.name}: {len(result.claims)} claims, {result.asked} chunks asked, "
        f"{result.reused} reused, {result.without_prose} without prose, "
        f"{len(result.failures)} failed, {len(result.problems)} claims skipped"
        + (f"; stopped: {result.stopped}" if result.stopped else ""),
        flush=True,
    )


def _stopped(results: Sequence[ExtractionResult]) -> int:
    stopped = [r for r in results if r.stopped]
    for r in stopped:
        print(f"stopped: {r.extractor.name}: {r.stopped}; run again to continue", file=sys.stderr)
    return 2 if stopped else 0


def _extract_claims(args: argparse.Namespace) -> int:
    run = _ClaimsInput(args)
    print(f"Extracting claims from {len(run.chunks)} chunks with {len(run.specs)} extractors.")
    results = []
    try:
        for spec in run.specs:
            result = extract_claims(
                run.chunks, spec, run.client, run.run_id, run.calls, store=run.store,
                reuse=run.reuse,
            )  # fmt: skip
            results.append(result)
            _print_extraction(result)
    finally:  # a recording of the answers so far is worth keeping when a later step fails
        if run.record is not None:
            run.live.save(run.record)
    output = {
        "schema_version": CLAIMS_SCHEMA_VERSION,
        **run.header(),
        "extractors": [r.extractor for r in results],
        "claims": [c for r in results for c in r.claims],
        "failures": [f for r in results for f in r.failures],
        "problems": [p for r in results for p in r.problems],
    }
    path = args.out / "extracted-claims.json"
    path.write_bytes(canonical_json(output, pretty=True))
    print(f"Extracted claims: {path.resolve()}")
    return _stopped(results)


def _run_claims(args: argparse.Namespace) -> int:
    return _stopped(_claims_run(args).results)


def _claims_run(args: argparse.Namespace) -> ClaimsRun:
    """`claims run` without its exit code: writes claims.json and claims.html."""
    run = _ClaimsInput(args)
    nli = _nli_model()
    recording = RecordingNli(nli) if args.record_nli is not None else None
    print(f"Claims from {len(run.chunks)} chunks with {len(run.specs)} extractors.", flush=True)
    try:
        result = run_claims(
            run.chunks,
            run.specs,
            run.client,
            recording or nli,
            run.run_id,
            run.calls,
            sections=run.ingestion.chunks,
            inventory=run.ingestion.inventory,
            project=run.ingestion.project,
            store=run.store,
            reuse=run.reuse,
            on_extracted=_print_extraction,
        )
    finally:  # recordings of the answers and scores so far are worth keeping on a failure
        if run.record is not None:
            run.live.save(run.record)
        if recording is not None:
            recording.save(args.record_nli)
    counts = claim_counts(result)
    output = {
        "schema_version": GROUNDED_SCHEMA_VERSION,
        **run.header(),
        "extractors": [r.extractor for r in result.results],
        "versions": result.versions,
        "counts": counts,
        "claims": result.claims,
        "failures": [f for r in result.results for f in r.failures],
        "problems": [p for r in result.results for p in r.problems],
    }
    path = args.out / "claims.json"
    path.write_bytes(canonical_json(output, pretty=True))
    page = args.out / "claims.html"
    page.write_bytes(render_claims(run.ingestion, run.chunks, result).encode("utf-8"))
    for name, by_status in counts.items():
        print(f"  {name}: " + ", ".join(f"{n} {status}" for status, n in by_status.items()))
    print(f"Claims: {path.resolve()}")
    print(f"Report: {page.resolve()}")
    return result


def _demo(args: argparse.Namespace) -> int:
    """`ci` + `claims run` into one fresh run folder, then run.json (docs/plans/demo-cli-web.md).

    shortcut: a folder on disk instead of Postgres; the API only reads run.json.
    """
    config = load_config(args.config)
    run_id = new_run_id(config.project)
    out = args.runs_dir / run_id
    out.mkdir(parents=True)
    common = {"config": args.config, "out": out, "soft_limit": DEFAULT_SOFT_LIMIT}
    code = _ingest(argparse.Namespace(**common, dry_run=False))
    if code:
        return code
    stopped: list[str] = []
    if not args.no_claims:
        if args.claims_store is not None:
            shutil.copyfile(args.claims_store, out / "claims-store.jsonl")
        result = _claims_run(
            argparse.Namespace(
                **common,
                source=args.source,
                extractor=args.extractor,
                no_reuse=False,
                run_id=run_id,
                record=None,
                record_nli=None,
                provider=args.provider,
            )
        )
        code = _stopped(result.results)
        stopped = [f"{r.extractor.name}: {r.stopped}" for r in result.results if r.stopped]
    claims = None if args.no_claims else json.loads((out / "claims.json").read_bytes())
    run = build_demo_run(
        json.loads((out / "ingestion.json").read_bytes()),
        json.loads((out / "results.json").read_bytes()),
        claims,
        run_id,
        stopped=stopped,
    )
    # last, and atomic: a run.json that exists is complete (the API lists only those)
    partial = out / "run.json.tmp"
    partial.write_bytes(canonical_json(run, pretty=True))
    os.replace(partial, out / "run.json")
    print(f"Run: {out.resolve()}")
    print(f"Web: http://localhost:5173/#/runs/{run_id}")
    return code


def _chunk(args: argparse.Namespace) -> int:
    if not args.root.is_dir():
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2
    try:
        documents = load_documents(args.root, args.glob or ["**/*.md"])
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
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
