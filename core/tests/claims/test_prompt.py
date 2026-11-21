from dataclasses import replace

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import (
    CLAIMS_SCHEMA,
    DEFAULT_EXTRACTORS,
    GROQ_EXTRACTORS,
    ExtractorSpec,
    build_request,
    extractor_for,
    render_prompt,
)


def test_prompt_has_project_location_and_the_whole_chunk(guide_chunks: list[Chunk]) -> None:
    chunk = next(c for c in guide_chunks if c.breadcrumb.endswith("Timeouts"))
    prompt = render_prompt(chunk)
    assert "Project: fixturelib\n" in prompt
    assert "Location in the docs: fixturelib > User Guide > Timeouts\n" in prompt
    assert f"<section>\n{chunk.text.strip()}\n</section>" in prompt
    assert "{{" not in prompt


def test_placeholders_inside_the_chunk_stay(guide_chunks: list[Chunk]) -> None:
    chunk = replace(guide_chunks[0], text="Use {{PROJECT}} and {{BREADCRUMB}} here.")
    assert "Use {{PROJECT}} and {{BREADCRUMB}} here." in render_prompt(chunk)


def test_request(guide_chunks: list[Chunk]) -> None:
    spec = ExtractorSpec("a", "acme/model", max_tokens=100)
    request = build_request(guide_chunks[0], spec)
    assert request.model == "acme/model"
    assert request.temperature == 0.0
    assert request.max_tokens == 100
    assert request.response_schema == CLAIMS_SCHEMA
    assert [m.role for m in request.messages] == ["user"]
    assert request.prompt_hash() == build_request(guide_chunks[0], spec).prompt_hash()


def test_unknown_prompt_version(guide_chunks: list[Chunk]) -> None:
    with pytest.raises(ValueError, match="prompt version 99"):
        build_request(guide_chunks[0], ExtractorSpec("a", "m", prompt_version=99))


def test_extractors_from_model_ids() -> None:
    assert extractor_for("qwen3.8-flash-next") == DEFAULT_EXTRACTORS[0]
    assert extractor_for("gemma4-26b-a4b-hpc") == DEFAULT_EXTRACTORS[1]
    assert all(s.thinking is False and s.max_tokens == 16384 for s in DEFAULT_EXTRACTORS)
    assert extractor_for("openai/gpt-oss-20b") == GROQ_EXTRACTORS[1]
    assert extractor_for("qwen/qwen3.8-27b") == GROQ_EXTRACTORS[0]
    assert extractor_for("acme/other") == ExtractorSpec("acme/other", "acme/other")
