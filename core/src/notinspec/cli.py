import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from notinspec import __version__
from notinspec.runner import (
    ChatRequest,
    Message,
    ModelClient,
    OpenRouterProvider,
    ProviderError,
    RecordingProvider,
)
from notinspec.verify import ANSWER_SCHEMA, parse_answer

# ad-hoc instruction for trying a model by hand; real prompts come from the generator's templates
_ASK_SYSTEM = (
    "Answer with only a JSON object describing the HTTP request to send, "
    "matching this JSON Schema:\n"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notinspec")
    parser.add_argument("--version", action="version", version=f"notinspec {__version__}")
    commands = parser.add_subparsers(dest="command")

    ask = commands.add_parser(
        "ask", help="ask one model one question via OpenRouter (needs OPENROUTER_API_KEY)"
    )
    ask.add_argument("prompt")
    ask.add_argument(
        "--model", required=True, help="OpenRouter model ID, e.g. <vendor>/<name>:free"
    )
    ask.add_argument(
        "--no-schema", action="store_true", help="don't send the answer schema as response_format"
    )
    ask.add_argument("--record", type=Path, help="save the raw response as a fake-provider fixture")

    models = commands.add_parser("models", help="list OpenRouter :free models")
    models.add_argument("--all", action="store_true", help="include paid models")

    args = parser.parse_args(argv)
    try:
        if args.command == "ask":
            return _ask(args.model, args.prompt, schema=not args.no_schema, record=args.record)
        if args.command == "models":
            return _models(free_only=not args.all)
    except ProviderError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    parser.print_help()
    return 0


def _ask(model: str, prompt: str, *, schema: bool, record: Path | None) -> int:
    live = RecordingProvider(OpenRouterProvider.from_env())
    request = ChatRequest(
        model=model,
        messages=(
            Message("system", _ASK_SYSTEM + json.dumps(ANSWER_SCHEMA)),
            Message("user", prompt),
        ),
        response_schema=ANSWER_SCHEMA if schema else None,
    )
    # one retry at most: trying by hand shouldn't burn the daily budget
    completion = ModelClient(live, max_attempts=2).ask("cli", request)
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


def _models(*, free_only: bool) -> int:
    for m in OpenRouterProvider.from_env().list_models():
        if free_only and not m.id.endswith(":free"):
            continue
        structured = "structured-output" if m.structured_output else "-"
        print(f"{m.id:<60} {m.context_length or '?':>8}  {structured}")
    return 0
