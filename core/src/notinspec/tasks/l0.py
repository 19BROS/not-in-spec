"""L0: recognition from the current inventory and explicit versioned removal evidence."""

from collections.abc import Iterable, Sequence

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


def generate_l0(
    inventory: Inventory,
    *,
    context: GenerationContext,
    chunks: Sequence[Chunk],
    writer: TaskTextWriter | None = None,
    existing: Iterable[TestItem] = (),
    conflicts: Sequence[Conflict] = (),
) -> GenerationResult:
    build = Builder(context, chunks, writer, existing, conflicts)
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
        proof = existence(inventory, name, None, context.docs_version, symbol is not None, sources)
        if proof.exists is True and not signatures:
            proof = Evidence(
                None, (), "no reliable signature; call-record fallback not implemented"
            )
        if build.conflicted(name, sources + proof.sources):
            proof = Evidence(None, (), "conflicting inventory evidence")
        symbol_facts[name] = proof
        _yes_no(build, Subject(name, context.docs_version), proof)
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
                context.docs_version,
                param in all_param_names,
                params.get(param, ()),
            )
            if build.conflicted(name, evidence.sources):
                evidence = Evidence(None, (), "conflicting inventory evidence")
            facts[param] = evidence
            _yes_no(build, Subject(name, context.docs_version, param), evidence)
        _choices(build, name, facts)
    # One question per known positive, with three proven removed symbols.
    _choices(build, None, symbol_facts)
    return build.result()


def _yes_no(build: Builder, subject: Subject, evidence: Evidence) -> None:
    if evidence.exists is None:
        build.skip(subject.symbol, "exists", f"{subject.parameter or 'symbol'}: {evidence.reason}")
    else:
        build.add(ExistsReference(subject, evidence.exists), evidence.sources)


def _choices(build: Builder, symbol: str | None, facts: dict[str, Evidence]) -> None:
    negatives = sorted(name for name, fact in facts.items() if fact.exists is False)
    positives = sorted(name for name, fact in facts.items() if fact.exists is True)
    if not positives or len(negatives) < 3:
        build.skip(
            symbol or build.context.project,
            "choice",
            "need one confirmed name and three confirmed removals",
        )
        return
    for correct in positives:
        names = [correct, *negatives[:3]]
        options = tuple(Option(content_hash({"name": name}), name) for name in names)
        sources = tuple(s for name in names for s in facts[name].sources)
        subject = Subject(
            symbol or correct, build.context.docs_version, correct if symbol else None
        )
        build.add(ChoiceReference(subject, options, options[0].id), sources)
