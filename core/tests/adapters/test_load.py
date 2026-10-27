from pathlib import Path

import orjson
import pytest
import yaml

from notinspec.adapters.openapi import SpecLoadError, load_spec, load_spec_bytes
from notinspec.adapters.openapi.load import parse_spec, validate_spec


def test_yaml_and_json_give_the_same_document(tmp_path: Path, fixtures: Path) -> None:
    from_yaml = load_spec(fixtures / "acme.yaml")
    json_file = tmp_path / "acme.json"
    json_file.write_bytes(orjson.dumps(from_yaml.document))
    assert load_spec(json_file).document == from_yaml.document


def test_json_is_sniffed_without_a_suffix() -> None:
    assert parse_spec(b'  {"openapi": "3.1.0"}') == {"openapi": "3.1.0"}


def test_yaml_1_1_scalars_are_read_like_json() -> None:
    doc = parse_spec(
        b"date: 2024-01-01\nflags: [on, off, yes, no, true, False]\n200: ok\nnull: x\ntrue: y\n",
        "x.yaml",
    )
    assert doc["date"] == "2024-01-01"
    assert doc["flags"] == ["on", "off", "yes", "no", True, False]
    assert doc["200"] == "ok"  # int keys (response codes) become strings
    assert doc["null"] == "x"
    assert doc["true"] == "y"


def test_libyaml_is_used() -> None:
    assert yaml.__with_libyaml__, "PyYAML without libyaml is far too slow for GitHub's spec"


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (b"- just\n- a list\n", "not a mapping"),
        (b"{not json", "cannot parse"),
        (b"a: [unclosed\n", "cannot parse"),
        (b"swagger: '2.0'\n", "Swagger 2.0"),
        (b"openapi: 2.5.0\n", "unsupported openapi version"),
        (b"info: {}\n", "unsupported openapi version"),
    ],
)
def test_unusable_input_raises(data: bytes, message: str) -> None:
    with pytest.raises(SpecLoadError, match=message):
        load_spec_bytes(data, "spec.json" if data.startswith(b"{") else "spec.yaml")


def test_validation_problems_are_collected_not_raised(fixtures: Path) -> None:
    spec = load_spec(fixtures / "acme.yaml")
    assert spec.openapi_version == "3.1.0"
    assert spec.problem_count == 1
    assert spec.problems == (
        "#/paths/~1v1~1charges~1{id}/get/parameters/0: 'required' is a required property",
    )


def test_validator_crash_is_a_problem_not_an_error(fixtures: Path) -> None:
    spec = load_spec(fixtures / "composition.yaml")
    assert any("validator stopped" in p for p in spec.problems)


def test_validation_can_be_skipped(fixtures: Path) -> None:
    spec = load_spec(fixtures / "composition.yaml", validate=False)
    assert spec.problems == ()
    assert spec.problem_count == 0


def test_valid_spec_has_no_problems() -> None:
    doc = {"openapi": "3.0.3", "info": {"title": "t", "version": "1"}, "paths": {}}
    assert validate_spec(doc, "3.0.3") == []


def test_problem_list_is_capped_but_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("notinspec.adapters.openapi.load.MAX_PROBLEMS", 2)
    # OpenAPI 3.0 requires `responses` on every operation: one problem per path
    paths = {f"/p{i}": {"get": {}} for i in range(5)}
    doc = {"openapi": "3.0.3", "info": {"title": "t", "version": "1"}, "paths": paths}
    spec = load_spec_bytes(orjson.dumps(doc), "s.json")
    assert spec.problem_count == 5
    assert len(spec.problems) == 2
