"""L0: documented API recognition with removals and snapshot-checked near misses."""

from collections.abc import Iterable, Sequence
from dataclasses import replace

from notinspec.adapters.canonical import content_hash
from notinspec.chunking import Chunk
from notinspec.inventory import Conflict, Inventory, Source
from notinspec.tasks.generation import Builder, Evidence, GenerationContext, existence, trusted
from notinspec.tasks.models import (
    ChoiceReference,
    ExistsReference,
    GenerationResult,
    Option,
    Subject,
    TaskTextWriter,
    TestItem,
)
from notinspec.tasks.negatives import AbsenceIndex, near_misses

type Candidate = tuple[ExistsReference, tuple[Source, ...]]


def generate_l0(
    inventory: Inventory,
    *,
    context: GenerationContext,
    chunks: Sequence[Chunk],
    writer: TaskTextWriter | None = None,
    existing: Iterable[TestItem] = (),
    conflicts: Sequence[Conflict] = (),
) -> GenerationResult:
    context.version_for("L0")  # fail even for empty inputs, before reuse or writer calls
    build = Builder(context, chunks, writer, existing, conflicts)
    absent = AbsenceIndex(inventory, chunks, conflicts)
    if not absent.complete:
        build.skip(context.project, "exists", "near misses disabled: incomplete chunk set")
    candidates: list[Candidate] = []
    symbols = {s.path: s for s in inventory.symbols}
    names = set(symbols) | {c.symbol for c in inventory.changes if c.parameter is None}
    symbol_facts: dict[str, Evidence] = {}
    for name in sorted(names):
        symbol = symbols.get(name)
        sources = symbol.sources if symbol else ()
        if symbol and (
            symbol.kind == "operation"
            or any(p.location is not None for sig in symbol.signatures for p in sig.parameters)
        ):
            build.skip(name, "L0", "OpenAPI mapping is not supported yet")
            continue
        signatures = [sig for sig in symbol.signatures if trusted(sig.sources)] if symbol else []
        # §6.6: no signature means no inventory-based recognition in this implementation.
        proof = existence(
            inventory, name, None, context.comparison_version, symbol is not None, sources
        )
        if proof.exists is True and not signatures:
            proof = Evidence(
                None, (), "no reliable signature; call-record fallback not implemented"
            )
        if build.conflicted(name, sources + proof.sources):
            proof = Evidence(None, (), "conflicting inventory evidence")
        symbol_facts[name] = proof
        _yes_no(build, Subject(name), proof, candidates)
        if symbol is None or proof.exists is not True:
            continue
        params: dict[str, tuple[Source, ...]] = {}
        all_param_names = {p.name for sig in symbol.signatures for p in sig.parameters}
        for sig in signatures:
            for p in sig.parameters:
                params[p.name] = params.get(p.name, ()) + p.sources
        old_names = {c.parameter for c in inventory.changes if c.symbol == name and c.parameter}
        facts: dict[str, Evidence] = {}
        for param in sorted(all_param_names | old_names):
            evidence = existence(
                inventory,
                name,
                param,
                context.comparison_version,
                param in all_param_names,
                params.get(param, ()),
            )
            if build.conflicted(name, evidence.sources):
                evidence = Evidence(None, (), "conflicting inventory evidence")
            facts[param] = evidence
            _yes_no(build, Subject(name, param), evidence, candidates)
        # **kwargs and overloads can hide accepted names. Only a closed, reliable
        # signature may anchor synthetic parameter negatives.
        if (
            len(symbol.signatures) == 1
            and len(signatures) == 1
            and all(trusted(p.sources) for p in signatures[0].parameters)
            and not any(p.kind == "var_keyword" for p in signatures[0].parameters)
        ):
            _near_misses(build, name, facts, absent, candidates)
        _choices(build, name, facts)
    # Symbol alternatives stay within the same parent namespace for near misses.
    _near_misses(build, None, symbol_facts, absent, candidates)
    _choices(build, None, symbol_facts)
    _balanced_yes_no(build, candidates)
    return build.result()


def _near_misses(
    build: Builder,
    symbol: str | None,
    facts: dict[str, Evidence],
    absent: AbsenceIndex,
    candidates: list[Candidate],
) -> None:
    if not absent.complete:
        return
    skipped: dict[str, int] = {}
    for name, proof in sorted(tuple(facts.items())):
        if proof.exists is not True:
            continue
        anchor = Subject(symbol or name, name if symbol else None)
        if not build.source_chunks(ExistsReference(anchor, True), proof.sources):
            continue
        prefix, _, short = name.rpartition(".")
        accepted = 0
        for variant in near_misses(short):
            candidate = f"{prefix}.{variant}" if prefix else variant
            if not absent.absent(candidate):
                continue
            if candidate in facts:
                previous = facts[candidate]
                if previous.anchors:
                    facts[candidate] = replace(
                        previous, anchors=tuple(sorted(set((*previous.anchors, name))))
                    )
                    accepted += 1
                continue
            subject = Subject(symbol or candidate, candidate if symbol else None)
            if build.conflicted(subject.symbol, proof.sources):
                continue
            evidence = Evidence(False, proof.sources, anchors=(name,))
            facts[candidate] = evidence
            _yes_no(build, subject, evidence, candidates)
            accepted += 1
        if not accepted:
            scope = symbol or prefix or build.context.project
            skipped[scope] = skipped.get(scope, 0) + 1
    for scope, count in sorted(skipped.items()):
        build.skip(scope, "exists", f"no safe near-miss name for {count} anchors")


def _yes_no(
    build: Builder, subject: Subject, evidence: Evidence, candidates: list[Candidate]
) -> None:
    if evidence.exists is None:
        build.skip(subject.symbol, "exists", f"{subject.parameter or 'symbol'}: {evidence.reason}")
    else:
        reference = ExistsReference(subject, evidence.exists, evidence.tested_version)
        if build.source_chunks(reference, evidence.sources):
            candidates.append((reference, evidence.sources))


def _balanced_yes_no(build: Builder, candidates: list[Candidate]) -> None:
    """Do not emit a one-class or heavily skewed yes/no test.

    Check eligibility BEFORE balancing/writing so missing evidence cannot erase one class.
    Selection is deterministic and independent of input order and of the display version.
    """
    positive = sorted((c for c in candidates if c[0].exists), key=lambda c: content_hash(c[0]))
    negative = sorted(
        (c for c in candidates if not c[0].exists),
        key=lambda c: (c[0].tested_version is None, content_hash(c[0])),
    )
    count = min(len(positive), len(negative))
    if not count:
        build.skip(
            build.context.project,
            "exists",
            "yes/no disabled: need both classes "
            f"(eligible yes={len(positive)}, no={len(negative)})",
        )
        return
    for reference, sources in positive[:count] + negative[:count]:
        build.add(reference, sources)
    if len(positive) != len(negative):
        build.skip(
            build.context.project,
            "exists",
            f"balanced yes/no to {count} per class; "
            f"omitted {abs(len(positive) - len(negative))} items",
        )


def _choices(build: Builder, symbol: str | None, facts: dict[str, Evidence]) -> None:
    negatives = sorted(
        (name for name, fact in facts.items() if fact.exists is False),
        key=lambda name: (facts[name].tested_version is None, name),
    )
    positives = sorted(name for name, fact in facts.items() if fact.exists is True)
    if not positives:
        return
    skipped_scopes: set[str] = set()
    for correct in positives:
        eligible = [
            name
            for name in negatives
            if correct not in facts[name].anchors
            and (
                facts[name].tested_version is not None
                or symbol is not None
                or name.rpartition(".")[0] == correct.rpartition(".")[0]
            )
        ]
        eligible.sort(
            key=lambda name: (
                facts[name].tested_version is None,
                name if facts[name].tested_version is not None else content_hash((correct, name)),
            )
        )
        if len(eligible) < 3:
            skipped_scopes.add(symbol or correct.rpartition(".")[0] or build.context.project)
            continue
        names = [correct, *eligible[:3]]
        options = tuple(Option(content_hash({"name": name}), name) for name in names)
        sources = tuple(s for name in names for s in facts[name].sources)
        subject = Subject(symbol or correct, correct if symbol else None)
        build.add(
            ChoiceReference(
                subject,
                options,
                options[0].id,
                build.context.comparison_version
                if any(facts[n].tested_version is not None for n in names)
                else None,
            ),
            sources,
        )
    for scope in sorted(skipped_scopes):
        build.skip(
            scope, "choice", "need three verified negatives from other anchors in the same scope"
        )
