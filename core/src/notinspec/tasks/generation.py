"""Shared candidate generation, conservative evidence handling and frozen-item reuse."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

from packaging.version import Version

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.chunking import Chunk
from notinspec.inventory import Change, Conflict, Inventory, Source, parse_version
from notinspec.tasks.identity import identity_key
from notinspec.tasks.models import (
    ChoiceReference,
    GenerationResult,
    PathReference,
    Question,
    Reference,
    SkippedTask,
    Subject,
    TaskTextWriter,
    TestItem,
    nonempty,
    positive,
)
from notinspec.tasks.text import TemplateWriter


@dataclass(frozen=True)
class GenerationContext:
    """Inventory MUST describe this version; historical signatures are not reconstructed."""

    project: str
    docs_version: str
    input_snapshot_hash: str
    generator_version: int = 2
    operator_version: int = 2
    api_version: str | None = None

    def __post_init__(self) -> None:
        for value in (self.project, self.docs_version, self.input_snapshot_hash):
            nonempty(value)
        if self.api_version is not None and parse_version(self.api_version) is None:
            raise ValueError("api_version must be PEP 440")
        positive(self.generator_version)
        positive(self.operator_version)

    @property
    def comparison_version(self) -> str | None:
        """Explicit API version, or a parseable label; needed only for Change evidence."""
        if self.api_version is not None:
            return self.api_version
        return self.docs_version if parse_version(self.docs_version) is not None else None


def trusted(sources: tuple[Source, ...]) -> bool:
    return any(s.type in ("spec", "signature") for s in sources)


@dataclass(frozen=True)
class Evidence:
    exists: bool | None
    sources: tuple[Source, ...]
    reason: str = ""
    tested_version: str | None = None


def existence(
    inventory: Inventory,
    symbol: str,
    parameter: str | None,
    version: str | None,
    present: bool,
    sources: tuple[Source, ...],
) -> Evidence:
    """An absent entry alone never proves absence. Only an effective explicit removal does."""
    changes = [c for c in inventory.changes if (c.symbol, c.parameter) == (symbol, parameter)]
    # Deprecation does not affect current-snapshot existence. In particular, a display
    # label like "main" must not block current inventory tasks because of a directive.
    status_changes = [c for c in changes if c.kind in ("added", "removed")]
    if not status_changes:
        if present and trusted(sources):
            return Evidence(True, sources)
        return Evidence(None, (), "no reliable snapshot entry or effective removal")
    target = parse_version(version) if version is not None else None
    if target is None:
        return Evidence(None, (), "Change evidence needs a comparable API version")
    dated: list[tuple[Version, Change]] = []
    for change in changes:
        parsed = parse_version(change.version)
        if parsed is None:
            return Evidence(None, (), "invalid change version")
        dated.append((parsed, change))
    if any(not trusted(c.sources) for c in changes):
        return Evidence(None, (), "change requires review; no spec/signature evidence")
    effective = [(v, c) for v, c in dated if v <= target]
    latest: list[Change] = []
    if effective:
        last = max(v for v, _ in effective)
        latest = [c for v, c in effective if v == last]
    kinds = {c.kind for c in latest}
    if "removed" in kinds and len(kinds) > 1:
        return Evidence(None, (), "contradictory changes at the same version")
    proof = tuple(s for c in latest for s in c.sources)
    if "removed" in kinds:
        if present:
            return Evidence(None, (), "removed name still appears in snapshot")
        return Evidence(False, proof, tested_version=version)
    # A snapshot with a future addition is inconsistent; don't invent historic signatures.
    if present and not effective and any(c.kind == "added" for c in changes):
        return Evidence(None, (), "snapshot predates the documented addition")
    if present and trusted(sources):
        return Evidence(True, sources + proof)
    return Evidence(None, (), "no reliable snapshot entry or effective removal")


class Builder:
    def __init__(
        self,
        context: GenerationContext,
        chunks: Sequence[Chunk],
        writer: TaskTextWriter | None,
        existing: Iterable[TestItem],
        conflicts: Sequence[Conflict],
    ) -> None:
        self.context = context
        self.writer = writer or TemplateWriter()
        self.chunks = chunks
        self.conflicts = conflicts
        self.existing: dict[str, TestItem] = {}
        for item in existing:
            if item.id in self.existing and item != self.existing[item.id]:
                raise ValueError("different frozen items have the same identity")
            self.existing[item.id] = item
        self.items: dict[str, TestItem] = {}
        self.skipped: list[SkippedTask] = []

    def skip(self, symbol: str, kind: str, reason: str) -> None:
        self.skipped.append(SkippedTask(symbol, kind, reason))

    def conflicted(self, symbol: str, sources: tuple[Source, ...]) -> bool:
        sections = {s.section_id for s in sources if s.section_id}
        return any(
            c.subject == symbol
            or c.subject.startswith(symbol + "(")
            or any(s.section_id in sections for s in c.sources if s.section_id)
            for c in self.conflicts
        )

    def source_chunks(self, reference: Reference, sources: tuple[Source, ...]) -> tuple[Chunk, ...]:
        """Eligibility before text writing, also used to gate the L0 class distribution."""
        s = reference.subject
        if self.conflicted(s.symbol, sources):
            self.skip(s.symbol, reference.kind, "conflicting inventory evidence")
            return ()
        sections = {source.section_id for source in sources if source.section_id}
        matched = sorted(
            (c for c in self.chunks if c.section_id in sections),
            key=lambda c: (c.section_id, c.part, c.id),
        )
        if not matched or sections - {c.section_id for c in matched}:
            self.skip(s.symbol, reference.kind, "source sections are missing from chunks")
            return ()
        return tuple(matched)

    def add(
        self, reference: Reference, sources: tuple[Source, ...], display_name: str = ""
    ) -> None:
        matched = self.source_chunks(reference, sources)
        if not matched:
            return
        s = reference.subject
        level: Literal["L0", "L1"] = "L0" if reference.kind in ("exists", "choice") else "L1"
        ctx = self.context
        key = content_hash(
            identity_key(ctx.project, matched[0].id, level, ctx.operator_version, reference)
        )
        if key in self.items:
            return
        if key in self.existing:
            self.items[key] = self.existing[key]  # no writer, no metadata overwrite
            return
        # MCQ writer input identifies the scope, never which option is correct.
        question_subject = s
        question_display = display_name or s.symbol
        if isinstance(reference, ChoiceReference):
            question_subject = Subject(
                s.symbol if s.parameter else ctx.project,
                "*" if s.parameter else None,
            )
            question_display = question_subject.symbol
        elif isinstance(reference, PathReference):
            # Do not rely on a writer ignoring the answer hidden in another field.
            question_subject = Subject(display_name)
        version = getattr(reference, "tested_version", None)
        question = Question(
            reference.kind,
            question_subject,
            question_display,
            reference.model_options() if isinstance(reference, ChoiceReference) else (),
            version,
        )
        item = TestItem(
            project=ctx.project,
            chunk_id=matched[0].id,
            chunk_ids=tuple(c.id for c in matched),
            level=level,
            question_kind=reference.kind,
            reference=reference,
            sources=sources,
            wording=self.writer.write(question),
            input_snapshot_hash=ctx.input_snapshot_hash,
            docs_version=ctx.docs_version,
            generator_version=ctx.generator_version,
            operator_version=ctx.operator_version,
        )
        self.items[key] = item

    def result(self) -> GenerationResult:
        return GenerationResult(
            tuple(self.items[k] for k in sorted(self.items)),
            tuple(sorted(set(self.skipped), key=canonical_json)),
        )
