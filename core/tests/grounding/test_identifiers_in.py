"""identifiers_in: the names a claim mentions, in text order (used to pick L2 subjects)."""

from notinspec.grounding import identifiers_in

NAMES = frozenset({"Retry", "total", "PoolManager", "allowed_methods"})


def test_identifiers_in_order() -> None:
    claim = "Setting `total` to False makes urllib3.util.Retry stop; Retry then raises."
    assert identifiers_in(claim, NAMES) == ("total", "urllib3.util.Retry", "Retry")


def test_identifiers_in_no_duplicates() -> None:
    claim = "`allowed_methods` set to None retries any verb; allowed_methods is a set."
    assert identifiers_in(claim, NAMES) == ("allowed_methods",)


def test_identifiers_in_skips_phrases() -> None:
    assert identifiers_in("`pip install urllib3` installs it", NAMES) == ()


def test_plain_lowercase_word_is_not_a_name() -> None:
    # the identifier rules need backticks, `_`, `.`, mixed case or digits for a lower-case name
    assert identifiers_in("Setting the total parameter to False", NAMES) == ()
