"""L1: open recall, only from an unambiguous reliable snapshot signature."""

from collections import Counter
from collections.abc import Iterable, Sequence

from notinspec.chunking import Chunk
from notinspec.inventory import Conflict, Inventory
from notinspec.tasks.generation import Builder, GenerationContext, existence, trusted
from notinspec.tasks.models import (
    DefaultReference,
    GenerationResult,
    PathReference,
    RequiredParametersReference,
    Subject,
    TaskTextWriter,
    TestItem,
)


def generate_l1(
    inventory: Inventory,
    *,
    context: GenerationContext,
    chunks: Sequence[Chunk],
    writer: TaskTextWriter | None = None,
    existing: Iterable[TestItem] = (),
    conflicts: Sequence[Conflict] = (),
) -> GenerationResult:
    build = Builder(context, chunks, writer, existing, conflicts)
    short_names = Counter(s.path.rsplit(".", 1)[-1] for s in inventory.symbols)
    for symbol in inventory.symbols:
        name = symbol.path
        proof = existence(inventory, name, None, context.comparison_version, True, symbol.sources)
        if proof.exists is not True:
            build.skip(name, "L1", proof.reason)
            continue
        if len(symbol.signatures) != 1:
            build.skip(name, "L1", "missing signature or ambiguous overloads")
            continue
        sig = symbol.signatures[0]
        if not trusted(sig.sources) or any(not trusted(p.sources) for p in sig.parameters):
            build.skip(name, "L1", "signature or parameters lack reliable sources")
            continue
        if len({p.name for p in sig.parameters}) != len(sig.parameters):
            build.skip(name, "L1", "duplicate parameter names")
            continue
        if symbol.kind == "operation" or any(p.location is not None for p in sig.parameters):
            build.skip(name, "L1", "OpenAPI mapping is not supported yet")
            continue
        if any(
            existence(inventory, name, p.name, context.comparison_version, True, p.sources).exists
            is not True
            for p in sig.parameters
        ):
            build.skip(name, "L1", "parameter changes disagree with snapshot or need review")
            continue
        sources = symbol.sources + sig.sources + tuple(s for p in sig.parameters for s in p.sources)
        subject = Subject(name)
        short = name.rsplit(".", 1)[-1]
        if short_names[short] == 1 and short != name:
            build.add(PathReference(subject, name), sources, short)
        else:
            build.skip(name, "path", "short name is ambiguous or already the complete path")
        build.add(
            RequiredParametersReference(
                subject, tuple(p.name for p in sig.parameters if p.required)
            ),
            sources,
        )
        for p in sig.parameters:
            if p.kind in ("var_positional", "var_keyword") or p.required:
                continue
            if p.default is None:
                build.skip(name, "default", f"{p.name}: default is not documented")
                continue
            build.add(DefaultReference(Subject(name, p.name), p.default), sources)
    return build.result()
