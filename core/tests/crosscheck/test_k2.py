"""K2 with hand-made chunks and NLI scores: facts, prefilter, decision, findings, type check."""

from dataclasses import replace

import pytest

from notinspec.chunking import Block, Chunk, Document, SignatureParameter, chunk_document
from notinspec.claims import ExtractedClaim, GroundedClaim
from notinspec.crosscheck import (
    K2_VERSION,
    SignatureFact,
    check_claims_against_signatures,
    check_documented_types,
    names_parameter,
    signature_facts,
    type_names,
)
from notinspec.inventory import (
    Constraint,
    Inventory,
    Parameter,
    Signature,
    Source,
    Symbol,
    build_inventory,
)
from notinspec.nli import MODEL_ID, REVISION, NliScores, RecordedNli

E = NliScores(0.9, 0.08, 0.02)
N = NliScores(0.1, 0.8, 0.1)
C = NliScores(0.02, 0.08, 0.9)


def _chunk(name: str, *blocks: Block) -> Chunk:
    text = f"# {name}\n\nSome text.\n"
    chunk = chunk_document(Document(f"docs/{name}.md", text), project="acme")[0]
    return replace(chunk, blocks=chunk.blocks + blocks)


def _sig(name: str, objtype: str, *params: SignatureParameter, type_: str | None = None) -> Block:
    return Block(
        "signature", 1, 1, 1, name=name, objtype=f"py:{objtype}", parameters=params, type=type_
    )


def _attribute(name: str, objtype: str, type_: str) -> Block:
    return Block("signature", 1, 1, 1, name=name, objtype=f"py:{objtype}", type=type_)


def _field(name: str, type_: str | None) -> Block:
    return Block("field", 1, 1, 1, name=name, field="param", type=type_)


def _return_type(type_: str) -> Block:
    return Block("signature", 1, 1, 1, field="return-type", type=type_)


P = SignatureParameter

RETRY = _chunk(
    "Retry",
    _sig(
        "acme.Retry",
        "class",
        P("total", default="10"),
        P("connect", default="None"),
        P("token", default="_DEFAULT.token"),
        P("methods", default="frozenset({'GET', 'PUT'})"),
        P("factor", default="-1"),
        P("*args"),
        P("**kwargs"),
        type_="None",
    ),
    _field("total", "int"),
    _field("connect", "int | None"),
)
INCREMENT = _chunk(
    "increment",
    _sig(
        "acme.Retry.increment",
        "method",
        P("method", "str | None", "None"),
        P("response", "Response | None", "None"),
        type_="Self",
    ),
)
TIMEOUT = _chunk("Timeout", _sig("acme.Timeout", "class", P("read", default="None")))
READ_TIMEOUT = _chunk(
    "read_timeout",
    _attribute("acme.Timeout.read_timeout", "property", "float | None"),
    _return_type("int, float or None"),
)
OPEN = _chunk(
    "open",
    _sig("acme.open", "function", P("mode", "Literal['r', 'w']", "'r'"), type_="File"),
)
WRAP = _chunk(
    "wrap",
    _sig("acme.wrap", "function", P("sock", "socket"), P("tls", "Literal[False]", "False")),
    _sig("acme.wrap", "function", P("sock", "socket"), P("tls", "bool", "False")),
    _field("sock", "socket.socket"),
    _field("tls", "bool"),
    _return_type("ssl.SSLSocket | Transport"),
)
GUIDE = _chunk("Guide")
CHUNKS = [RETRY, INCREMENT, TIMEOUT, READ_TIMEOUT, OPEN, WRAP, GUIDE]
INVENTORY = build_inventory(CHUNKS).inventory


def _facts() -> dict[str, SignatureFact]:
    return {f.ref: f for f in signature_facts(CHUNKS, INVENTORY)}


def _claim(
    text: str,
    chunk: Chunk = RETRY,
    *,
    extractor: str = "x",
    local_id: str = "c1",
    citation: str | None = None,
    span: tuple[int, int] = (10, 20),
    status: str = "kept",
) -> GroundedClaim:
    return GroundedClaim(
        claim=ExtractedClaim(
            chunk.id, extractor, local_id, text, citation or text, "fact", "r", "h", "m"
        ),
        prompt_version=1,
        status=status,  # type: ignore[arg-type]
        citation_span=span,
        citation_matches=1,
        premise_candidates=1,
        premise="premise",
        premise_span=span,
        nli=E,
        missing=(),
    )


def _nli(scores: dict[tuple[str, str], NliScores]) -> RecordedNli:
    """Replays exactly these pairs; a pair outside the prefilter raises."""
    return RecordedNli({(MODEL_ID, REVISION, p, h): s for (p, h), s in scores.items()})


def _both(fact: str, claim: str, forward: NliScores, back: NliScores) -> dict:
    sentence = _facts()[fact].sentence
    return {(sentence, claim): forward, (claim, sentence): back}


# --- facts ------------------------------------------------------------------------------------


def test_facts_of_a_class() -> None:
    facts = {r: f for r, f in _facts().items() if f.symbol == "acme.Retry"}
    assert {r: (f.sentence, f.quote) for r, f in facts.items()} == {
        "acme.Retry(total).default": (
            "The default value of the total parameter of Retry is 10.",
            "total=10",
        ),
        "acme.Retry(total).type": ("The total parameter of Retry has type int.", "total (int)"),
        "acme.Retry(connect).type": (
            "The connect parameter of Retry has type int or None.",
            "connect (int | None)",
        ),
        "acme.Retry(methods).default": (
            "The default value of the methods parameter of Retry is frozenset({'GET', 'PUT'}).",
            "methods=frozenset({'GET', 'PUT'})",
        ),
        "acme.Retry(factor).default": (
            "The default value of the factor parameter of Retry is -1.",
            "factor=-1",
        ),
    }
    # left out: `connect=None` ("computed inside"), the sentinel `token`, *args / **kwargs, and
    # the `-> None` of a class
    assert {f.evidence for f in facts.values()} == {"parameter"}
    assert {f.section_id for f in facts.values()} == {RETRY.section_id}


def test_method_returns_self_and_annotations_are_quoted_as_written() -> None:
    facts = {r: f for r, f in _facts().items() if f.symbol == "acme.Retry.increment"}
    assert facts["acme.Retry.increment(method).type"].sentence == (
        "The method parameter of Retry.increment() has type str or None."
    )
    assert facts["acme.Retry.increment(method).type"].quote == "method: str | None = None"
    returns = facts["acme.Retry.increment.returns"]
    assert (returns.sentence, returns.quote, returns.evidence) == (
        "Retry.increment() returns Retry.",
        "-> Self",
        "signature",
    )


def test_property_type_and_literal_enum() -> None:
    facts = _facts()
    prop = facts["acme.Timeout.read_timeout.type"]
    assert (prop.sentence, prop.quote, prop.parameter) == (
        "The read_timeout property of Timeout has type float or None.",
        "read_timeout: float | None",
        None,
    )
    assert facts["acme.open(mode).enum"].sentence == (
        "The mode parameter of open() must be one of 'r', 'w'."
    )
    assert facts["acme.open(mode).enum"].evidence == "constraint"
    assert facts["acme.open(mode).default"].quote == "mode: Literal['r', 'w'] = 'r'"
    assert "acme.open(mode).type" not in facts  # the enum says it
    assert facts["acme.open.returns"].sentence == "open() returns File."


def test_overloads_that_disagree_give_no_fact() -> None:
    facts = {r: f for r, f in _facts().items() if f.symbol == "acme.wrap"}
    # tls is `Literal[False]` in one overload and `bool` in the other; the default agrees
    assert set(facts) == {"acme.wrap(sock).type", "acme.wrap(tls).default", "acme.wrap.returns"}
    assert facts["acme.wrap.returns"].quote == "Return type: ssl.SSLSocket | Transport"


def test_range_unit_format_and_dict_defaults() -> None:
    """The Sphinx builder makes only enums; a formal spec gives the other constraints."""
    chunk = _chunk("sleep", _sig("acme.sleep", "function", P("seconds")))
    src = (Source("signature", section_id=chunk.section_id),)

    def param(name: str, *constraints: Constraint, default: str | None = None) -> Parameter:
        return Parameter(
            name, "positional_or_keyword", default is None, src, "float", default, None,
            constraints,
        )  # fmt: skip

    params = (
        param("seconds", Constraint("range", src, minimum="0", maximum="60",
                                    exclusive_maximum=True)),
        param("delay", Constraint("range", src, minimum="1", exclusive_minimum=True),
              Constraint("unit", src, unit="seconds")),
        param("until", Constraint("range", src, maximum="9"), Constraint("format", src,
              format="date-time")),
        param("headers", default="{'a': 1}"),
    )  # fmt: skip
    inventory = Inventory((Symbol("acme.sleep", "function", src, (Signature(params, src),)),))
    facts = {f.ref: f for f in signature_facts([chunk], inventory)}
    assert {r: f.sentence for r, f in facts.items() if f.kind != "type"} == {
        "acme.sleep(seconds).range": (
            "The seconds parameter of sleep() must be at least 0 and less than 60."
        ),
        "acme.sleep(delay).range": "The delay parameter of sleep() must be greater than 1.",
        "acme.sleep(delay).unit": "The delay parameter of sleep() is given in seconds.",
        "acme.sleep(until).range": "The until parameter of sleep() must be at most 9.",
        "acme.sleep(until).format": "The until parameter of sleep() has the format date-time.",
        "acme.sleep(headers).default": (
            "The default value of the headers parameter of sleep() is {'a': 1}."
        ),
    }
    assert facts["acme.sleep(seconds).range"].value == "0..60"
    assert facts["acme.sleep(delay).unit"].evidence == "constraint"
    assert facts["acme.sleep(seconds).range"].quote == "seconds"  # as the signature shows it
    assert facts["acme.sleep(delay).type"].quote == "delay: float"  # not in the signature block


# --- prefilter --------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("claim", "name", "expected"),
    [
        ("The backoff_factor is multiplied each time.", "backoff_factor", True),
        ("Set `total` to 0 to fail on the first retry.", "total", True),
        ("Pass `total=3` to retry three times.", "total", True),
        ("The total parameter caps all other counts.", "total", True),
        ("The parameter total caps all other counts.", "total", True),
        ("Use Retry(total=3).", "total", True),
        # a plain word is a parameter only where the claim says so
        ("The total number of retries to allow.", "total", False),
        ("The increment() method returns a new object.", "method", False),
        ("If self.total is set, the read timeout depends on it.", "total", False),
        ("The read_timeout property returns a float.", "read", False),
        ("The read_timeout property returns a float.", "read_timeout", True),
        ("Use proxy_ssl_context for the proxy.", "ssl_context", False),
    ],
)
def test_names_parameter(claim: str, name: str, expected: bool) -> None:
    assert names_parameter(claim, name) is expected


# --- claims vs. facts -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("forward", "back", "contradiction"),
    [
        (C, N, True),
        (N, C, True),  # one direction is enough (run 009: is_connection_dropped)
        (C, C, True),
        (N, N, False),
        (E, N, False),
        (N, E, False),
    ],
)
def test_decision(forward: NliScores, back: NliScores, contradiction: bool) -> None:
    text = "The total parameter of Retry defaults to 3."
    nli = _nli(
        _both("acme.Retry(total).default", text, forward, back)
        | _both("acme.Retry(total).type", text, N, N)
    )
    result = check_claims_against_signatures([_claim(text)], CHUNKS, INVENTORY, nli)
    assert [(p.fact, p.contradiction) for p in result.pairs] == [
        ("acme.Retry(total).default", contradiction),
        ("acme.Retry(total).type", False),
    ]
    assert len(result.findings) == int(contradiction)
    assert result.contradicted == ((f"{RETRY.id}/x/c1",) if contradiction else ())


def test_only_facts_of_the_claims_own_section_and_kept_claims() -> None:
    # names `total`, but in a guide and in another class: no NLI call (RecordedNli would raise)
    guide = _claim("The total parameter of Retry defaults to 3.", GUIDE)
    other = _claim("The `read` parameter of Retry defaults to 3.", RETRY, local_id="c2")
    dropped = _claim("The total parameter defaults to 3.", local_id="c3", status="nli_neutral")
    timeout = _claim("The `read` parameter defaults to 3.", TIMEOUT, local_id="c4")
    result = check_claims_against_signatures(
        [guide, other, dropped, timeout], CHUNKS, INVENTORY, _nli({})
    )
    assert result.pairs == ()  # Timeout's `read=None` gives no fact


def test_return_and_property_facts_need_no_parameter_name() -> None:
    returns = "increment() returns a new Retry object."
    other = "increment() raises MaxRetryError when exhausted."
    prop = "The read_timeout property is an integer."
    nli = _nli(
        _both("acme.Retry.increment.returns", returns, N, N)
        | _both("acme.Timeout.read_timeout.type", prop, C, C)
    )
    claims = [
        _claim(returns, INCREMENT),
        _claim(other, INCREMENT, local_id="c2"),
        _claim(prop, READ_TIMEOUT),
    ]
    result = check_claims_against_signatures(claims, CHUNKS, INVENTORY, nli)
    assert [p.fact for p in result.pairs] == [
        "acme.Retry.increment.returns",
        "acme.Timeout.read_timeout.type",
    ]
    (finding,) = result.findings
    assert (finding.check, finding.kind, finding.confidence, finding.subject) == (
        "K2",
        "contradiction",
        "low",
        "acme.Timeout.read_timeout",
    )
    assert finding.message == (
        "a claim contradicts the signature of acme.Timeout.read_timeout: “The read_timeout "
        "property is an integer.” vs `read_timeout: float | None`"
    )
    assert [e.kind for e in finding.evidence] == ["signature", "claim"]
    assert len(finding.nli) == 2
    assert dict(finding.versions)["k2"] == str(K2_VERSION)
    assert dict(finding.versions)["prefilter"] == result.versions.prefilter


def _contradicting(*claims: GroundedClaim) -> RecordedNli:
    scores: dict = {}
    for c in claims:
        scores |= _both("acme.Retry(total).default", c.claim.text, C, N)
        scores |= _both("acme.Retry(total).type", c.claim.text, N, N)
    return _nli(scores)


def test_claims_that_quote_the_same_text_are_one_finding() -> None:
    qwen = _claim("The total parameter defaults to 3.", citation="`total` defaults to 3")
    gemma = _claim(
        "By default the total parameter is 3.",
        extractor="y",
        citation="`total` defaults to 3.",  # a full stop more, same place: overlapping spans
        span=(10, 21),
    )
    elsewhere = _claim(
        "The total parameter is 3 unless set.",
        extractor="y",
        local_id="c2",
        citation="total is 3 unless set",
        span=(40, 60),
    )
    claims = [qwen, gemma, elsewhere]
    result = check_claims_against_signatures(claims, CHUNKS, INVENTORY, _contradicting(*claims))
    assert sorted(len(f.evidence) for f in result.findings) == [2, 3]
    joint = next(f for f in result.findings if len(f.evidence) == 3)
    assert joint.message.endswith("vs `total=10` (+1 more claims)")
    # the same docs text without the second extractor's claim: the same finding
    alone = check_claims_against_signatures([qwen], CHUNKS, INVENTORY, _contradicting(qwen))
    assert alone.findings[0].key == joint.key
    assert len(result.contradicted) == 3


def test_same_result_in_any_order() -> None:
    a = _claim("The total parameter defaults to 3.")
    b = _claim("The total parameter defaults to 5.", local_id="c2", span=(40, 50))
    one = check_claims_against_signatures([a, b], CHUNKS, INVENTORY, _contradicting(a, b))
    other = check_claims_against_signatures([b, a], CHUNKS, INVENTORY, _contradicting(a, b))
    assert one.findings == other.findings
    assert one.contradicted == other.contradicted


def test_invalid_input() -> None:
    claim = _claim("The total parameter defaults to 3.")
    with pytest.raises(ValueError, match="not in `chunks`"):
        check_claims_against_signatures([claim], [GUIDE], INVENTORY, _nli({}))
    with pytest.raises(ValueError, match="same chunk, extractor and local id"):
        check_claims_against_signatures([claim, claim], CHUNKS, INVENTORY, _nli({}))


# --- annotation vs. documented type -----------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "names"),
    [
        ("int, float, or None", {"int", "float", "None"}),
        ("float | None", {"float", "None"}),
        ("Optional[ssl.SSLSocket]", {"SSLSocket", "None"}),
        ("typing.Union[int, str]", {"int", "str"}),
        ("Literal[False]", {"bool"}),
        ("Literal['r', 'w'] | None", {"str", "None"}),
        ("dict[str, str]", {"dict[str,str]"}),
        ("tuple[None, None] | tuple[str, str | None]", {"tuple[None,None]", "tuple[str,str|None]"}),
        ("integer or string", {"int", "str"}),
        ("int, optional", {"int"}),
        ("int, default 3", {"int"}),
        ("Literal[Mode.READ]", {"Mode.READ"}),
    ],
)
def test_type_names(text: str, names: set[str]) -> None:
    assert type_names(text) == names


def test_documented_types() -> None:
    (finding,) = check_documented_types(CHUNKS)
    assert (finding.check, finding.kind, finding.confidence, finding.subject) == (
        "K2",
        "type-mismatch",
        "medium",
        "acme.Timeout.read_timeout",
    )
    assert finding.message == (
        "acme.Timeout.read_timeout: the signature gives the type as `float | None`, the docs "
        "text as `int, float or None`"
    )
    assert [e.quote for e in finding.evidence] == [
        "float | None",
        "Return type: int, float or None",
    ]
    # not reported: `socket` vs `socket.socket`, `Literal[False]` / `bool` vs `bool`, and a
    # `Return type` without an annotation (acme.wrap)


def test_documented_parameter_type_mismatch() -> None:
    chunk = _chunk(
        "connect",
        _sig("acme.connect", "function", P("conn", "Connection")),
        _field("conn", "BaseConnection"),
    )
    (finding,) = check_documented_types([chunk])
    assert finding.message == (
        "acme.connect: the signature gives the conn parameter as `Connection`, the docs text "
        "as `BaseConnection`"
    )
    assert [e.kind for e in finding.evidence] == ["parameter", "parameter"]
    assert finding.evidence[1].quote == "conn (BaseConnection)"
