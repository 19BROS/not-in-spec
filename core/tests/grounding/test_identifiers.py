from collections.abc import Callable, Mapping
from functools import partial
from pathlib import Path
from typing import Any

import pytest

from notinspec.chunking import Chunk, Document, chunk_blocks, chunk_document
from notinspec.grounding import inventory_names, missing_identifiers, section_reference
from notinspec.inventory import Inventory
from notinspec.sphinx import read_sphinx_xml

SPHINX = Path(__file__).parents[1] / "fixtures" / "sphinx"

NONE: frozenset[str] = frozenset()


def _missing(claim: str, reference: str, known: frozenset[str] = NONE) -> tuple[str, ...]:
    return missing_identifiers(claim, reference, project="urllib3", known_names=known)


# --- carried over from the prototype (experiments/nli/id_check.py) -------------------------


def test_names_match_case_sensitive_on_name_boundaries() -> None:
    ref = "Set `proxy_ssl_context` on `ProxyConfig.ssl_context` or `PoolManager`."
    assert _missing("`ssl_context` is used.", ref) == ()
    assert _missing("`ssl_context` is used.", "Set `proxy_ssl_context`.") == ("ssl_context",)
    assert _missing("ProxyManager sends it.", ref) == ("ProxyManager",)
    assert _missing("Uses poolmanager.", ref) == ()  # a plain word is not checked
    assert _missing("`PoolManager.urlopen()` sends it.", ref) == ("PoolManager.urlopen",)


def test_numbers_and_versions_match_whole() -> None:
    assert _missing("Python 3.13 is supported.", "Python 3.13.14+ is supported.") == ("3.13",)
    assert _missing("Retries 3 times.", "Uses urllib3.") == ("3",)
    assert _missing("Fixed in 2.8.0.", "2.8.0 (2025-06-18)") == ()
    assert _missing("Removed in v3.0.", "will be removed in urllib3 v3.0") == ()


def test_project_prefix_is_optional() -> None:
    assert _missing("`urllib3.Timeout` sets limits.", "Use `Timeout` for limits.") == ()
    assert _missing("`requests.Timeout` sets limits.", "Use `Timeout` for limits.") == (
        "requests.Timeout",
    )


def test_quotes_backticks_and_abbreviations() -> None:
    assert _missing("It’s `Retry.total`, e.g. three.", "Set Retry.total to retry.") == ()


# --- issue #26 ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("claim", "reference"),
    [
        ("A connect timeout of 1 second.", "Use `Timeout(connect=1.0)`."),
        ("A connect timeout of 1.0 second.", "Use `Timeout(connect=1)`."),
        ("A connect timeout of 1.00 second.", "Use `Timeout(connect=1.0)`."),
        ("At most 1,000 connections.", "At most 1000 connections."),
        ("At most 1000000 bytes.", "At most 1,000,000 bytes."),
    ],
)
def test_trailing_zeros_and_thousands_separators(claim: str, reference: str) -> None:
    assert _missing(claim, reference) == ()


@pytest.mark.parametrize(
    ("claim", "reference", "missing"),
    [
        ("Python 3.10 is supported.", "Python 3.1 is supported.", ("3.10",)),
        ("Waits 0.50 seconds.", "Waits 0.5 seconds.", ("0.50",)),
        ("At most 1,00 connections.", "At most 100 connections.", ("1", "00")),
    ],
)
def test_other_numbers_are_compared_as_written(
    claim: str, reference: str, missing: tuple[str, ...]
) -> None:
    assert _missing(claim, reference) == missing


def test_versions_are_compared_as_written() -> None:
    assert _missing("Added in 2.0.0.", "Added in 2.0.0.") == ()
    assert _missing("Added in 2.0.0.", "Added in 2.0.") == ("2.0.0",)


@pytest.mark.parametrize(
    ("claim", "reference"),
    [
        ("Waits 2.5 seconds.", "Waits 2.5s."),
        ("Waits 2.5s.", "Waits 2.5 seconds."),
        ("Limit is 100 ms.", "Limit is 100ms by default."),
    ],
)
def test_a_unit_glued_to_a_number_is_allowed(claim: str, reference: str) -> None:
    assert _missing(claim, reference) == ()


def test_a_glued_unit_does_not_hide_a_wrong_number() -> None:
    assert _missing("Waits 3 seconds.", "Waits 2.5s.") == ("3",)


def test_backticked_name_with_a_leading_dot() -> None:
    assert _missing("Call `.request()` to send.", "Call `PoolManager.request()`.") == ()
    assert _missing("Call `.urlopen()` to send.", "Call `PoolManager.request()`.") == ("urlopen",)


@pytest.mark.parametrize(
    ("claim", "reference"),
    [
        ("`TLSv1.2` is the minimum.", "TLS 1.2 is the minimum."),
        ("TLS 1.2 is the minimum.", "Requires TLSv1.2 or later."),
        ("IPv6 hosts are supported.", "IP 6 hosts."),
    ],
)
def test_acronym_glued_to_a_version(claim: str, reference: str) -> None:
    assert _missing(claim, reference) == ()


def test_acronym_glued_to_a_wrong_version_fails() -> None:
    assert _missing("`TLSv1.3` is the minimum.", "TLS 1.2 is the minimum.") == ("1.3",)


@pytest.mark.parametrize("claim", ["Custom CAs are loaded.", "URLs are parsed.", "Two APIs."])
def test_acronym_plurals_are_not_identifiers(claim: str) -> None:
    assert _missing(claim, "Loads CA certificates, parses an URL, one API.") == ()


def test_backticked_expression_is_split_into_names_and_numbers() -> None:
    ref = "Pass total=3 to Retry."
    assert _missing("Use `Retry(total=3)`.", ref) == ()
    assert _missing("Use `Retry(total=5)`.", ref) == ("5",)
    assert _missing("Use `Retry(connect=3)`.", ref) == ("connect",)


def test_inner_capital_names_are_still_identifiers() -> None:
    assert _missing("Raises `SSLError`.", "Raises an error.") == ("SSLError",)
    assert _missing("Uses HTTPSConnection.", "Uses a connection.") == ("HTTPSConnection",)


def test_capitalized_inventory_names_are_identifiers() -> None:
    known = frozenset({"Retry", "Timeout", "read", "total"})
    ref = "Use Timeout to limit how long a request waits."
    assert _missing("Retry limits how long a request waits.", ref, known) == ("Retry",)
    assert _missing("Retry limits how long a request waits.", ref) == ()  # not in inventory
    assert _missing("Timeout limits how long a request waits.", ref, known) == ()


def test_capitalized_inventory_name_starting_a_sentence_matches_any_case() -> None:
    known = frozenset({"Timeout", "Retry"})
    ref = "Read timeout errors are retried."
    assert _missing("Timeout errors are retried.", ref, known) == ()
    assert _missing("Errors are counted. Timeout errors are retried.", ref, known) == ()
    assert _missing("The Timeout object is retried.", ref, known) == ("Timeout",)
    assert _missing("`Timeout` errors are retried.", ref, known) == ("Timeout",)
    # also elsewhere in the claim: case matters again
    assert _missing("Timeout errors use Timeout.", ref, known) == ("Timeout",)
    assert _missing("Retry errors are retried.", ref, known) == ("Retry",)


def test_lowercase_inventory_names_count_only_when_backticked() -> None:
    known = frozenset({"read", "total"})
    ref = "The connect timeout is in seconds."
    assert _missing("Read the total in seconds.", ref, known) == ()
    assert _missing("Set `total` in seconds.", ref, known) == ("total",)


# --- reference -----------------------------------------------------------------------------


def _chunks(text: str, **kwargs: int) -> tuple[Chunk, ...]:
    return chunk_document(Document("docs/a.md", text), project="urllib3", **kwargs)


def test_reference_is_breadcrumb_and_prose_of_all_parts(
    make_inventory: Callable[[Mapping[str, Mapping[str, Any]]], Inventory],
) -> None:
    text = "# Using Timeouts\n\n" + "\n\n".join(
        f"Paragraph {i} mentions `name_{i}`." for i in range(40)
    )
    text += "\n\n```python\ncode_only = 1\n```\n"
    parts = _chunks(text, soft_limit=100)
    assert len(parts) > 1
    ref = section_reference(parts, make_inventory({}))
    assert ref.startswith("urllib3 > Using Timeouts\n")
    assert _missing("`name_0` and `name_39` in Using Timeouts.", ref) == ()
    assert _missing("`code_only` is set.", ref) == ("code_only",)  # code doesn't count


def test_api_description_adds_inventory_names(
    make_inventory: Callable[[Mapping[str, Mapping[str, Any]]], Inventory],
) -> None:
    xml = read_sphinx_xml(SPHINX / "xml-plain")
    chunks = [c for d in xml.documents for c in chunk_blocks(d, project="fixturelib")]
    connect = [c for c in chunks if c.breadcrumb == "fixturelib > API Reference > connect()"]
    check = partial(missing_identifiers, project="fixturelib", known_names=NONE)
    # not in the inventory: the signature block's own names
    ref = section_reference(connect, make_inventory({}))
    assert check("`connect()` takes `retries`.", ref) == ()
    assert check("`fixturelib.connect()` takes `backoff`.", ref) == ("backoff",)
    inventory = make_inventory(
        {"fixturelib.connect": {"kind": "function", "params": ["host", "backoff=None"]}}
    )
    ref = section_reference(connect, inventory)
    assert check("`connect()` takes `backoff`.", ref) == ()
    # a guide section gets no API names
    guide = [c for c in chunks if c.breadcrumb == "fixturelib > User Guide > Timeouts"]
    assert check("`connect()` takes `backoff`.", section_reference(guide, inventory)) == (
        "connect",
        "backoff",
    )


def test_inventory_names(
    make_inventory: Callable[[Mapping[str, Mapping[str, Any]]], Inventory],
) -> None:
    inventory = make_inventory(
        {
            "urllib3.util.Retry": {"kind": "class", "params": ["total=10", "**kw"]},
            "urllib3.util.Retry.sleep": {"kind": "method", "params": ["self"]},
        }
    )
    assert inventory_names(inventory) == frozenset({"Retry", "total", "kw", "sleep", "self"})
    assert section_reference((), inventory) == ""
