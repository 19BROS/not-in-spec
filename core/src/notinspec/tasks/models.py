"""Frozen task candidates. Answers and model-facing prompts are separate types."""

from dataclasses import dataclass, field
from typing import Literal, Protocol

from packaging.utils import canonicalize_version

from notinspec.inventory import Source, parse_version
from notinspec.inventory.objects import sort_sources

type QuestionKind = Literal["exists", "choice", "required-parameters", "default", "path", "claim"]


def nonempty(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a non-empty string")


def positive(value: int) -> None:
    if type(value) is not int or value < 1:
        raise ValueError("versions must be positive integers")


@dataclass(frozen=True)
class Subject:
    symbol: str
    parameter: str | None = None

    def __post_init__(self) -> None:
        nonempty(self.symbol)
        if self.parameter is not None:
            nonempty(self.parameter)


def tested_version(value: str | None) -> str | None:
    """Only Change-dependent answers have a semantic version, never a display label."""
    if value is None:
        return None
    nonempty(value)
    if parse_version(value) is None:
        raise ValueError("tested version must be PEP 440")
    return canonicalize_version(value)


def check_subject(subject: Subject, *, whole_symbol: bool = False) -> None:
    if not isinstance(subject, Subject):
        raise ValueError("reference needs a typed Subject")
    if whole_symbol and subject.parameter is not None:
        raise ValueError("this reference must describe a whole symbol")


@dataclass(frozen=True)
class Option:
    id: str
    text: str

    def __post_init__(self) -> None:
        nonempty(self.id)
        nonempty(self.text)


CHOICE_LABELS = ("A", "B", "C", "D")


@dataclass(frozen=True)
class ModelOption:
    """The displayed option. Internal IDs and correctness stay in ChoiceReference."""

    label: str
    text: str


@dataclass(frozen=True)
class ExistsReference:
    subject: Subject
    exists: bool
    tested_version: str | None = None
    kind: Literal["exists"] = field(default="exists", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject)
        if type(self.exists) is not bool:
            raise ValueError("exists must be boolean")
        object.__setattr__(self, "tested_version", tested_version(self.tested_version))


@dataclass(frozen=True)
class ChoiceReference:
    subject: Subject  # the correct symbol/parameter; all choices are frozen below
    options: tuple[Option, ...]
    correct_id: str
    tested_version: str | None = None
    kind: Literal["choice"] = field(default="choice", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject)
        if not isinstance(self.options, tuple) or not all(
            isinstance(o, Option) for o in self.options
        ):
            raise ValueError("options must be an immutable tuple of Option objects")
        if len(self.options) != 4:
            raise ValueError("MCQ needs four options")
        if len({o.id for o in self.options}) != 4 or len({o.text for o in self.options}) != 4:
            raise ValueError("MCQ options must have unique IDs and text")
        if sum(o.id == self.correct_id for o in self.options) != 1:
            raise ValueError("MCQ needs exactly one correct option ID")
        object.__setattr__(self, "options", tuple(sorted(self.options, key=lambda o: o.id)))
        object.__setattr__(self, "tested_version", tested_version(self.tested_version))

    def _ordered_options(self, option_order: tuple[str, ...] | None) -> tuple[Option, ...]:
        if option_order is None:
            return self.options
        by_id = {o.id: o for o in self.options}
        if len(option_order) != 4 or set(option_order) != set(by_id):
            raise ValueError("option_order must be a permutation of the four internal IDs")
        return tuple(by_id[key] for key in option_order)

    def model_options(self, option_order: tuple[str, ...] | None = None) -> tuple[ModelOption, ...]:
        return tuple(
            ModelOption(label, option.text)
            for label, option in zip(
                CHOICE_LABELS, self._ordered_options(option_order), strict=True
            )
        )

    def option_id(self, label: str, option_order: tuple[str, ...] | None = None) -> str:
        """Translate the answer using the SAME order sent to the model (not an evaluator)."""
        if label not in CHOICE_LABELS:
            raise ValueError("answer label must be A, B, C or D")
        return self._ordered_options(option_order)[CHOICE_LABELS.index(label)].id


@dataclass(frozen=True)
class RequiredParametersReference:
    subject: Subject
    names: tuple[str, ...]
    kind: Literal["required-parameters"] = field(default="required-parameters", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject, whole_symbol=True)
        if not isinstance(self.names, tuple):
            raise ValueError("parameter names must be an immutable tuple")
        for name in self.names:
            nonempty(name)
        if len(set(self.names)) != len(self.names):
            raise ValueError("duplicate required parameter")
        object.__setattr__(self, "names", tuple(sorted(self.names)))


@dataclass(frozen=True)
class DefaultReference:
    subject: Subject
    value: str  # as written, like inventory.Parameter.default: "None" != missing
    kind: Literal["default"] = field(default="default", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject)
        nonempty(self.value)
        if self.subject.parameter is None:
            raise ValueError("default reference needs a parameter")


@dataclass(frozen=True)
class PathReference:
    subject: Subject
    path: str
    kind: Literal["path"] = field(default="path", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject, whole_symbol=True)
        nonempty(self.path)
        if self.path != self.subject.symbol:
            raise ValueError("path answer must identify the subject")


@dataclass(frozen=True)
class ClaimReference:
    """L2: a grounded fact claim, built by code. The writer's answer phrase is task text."""

    subject: Subject
    claim: str  # the claim text, as extracted
    claim_ref: str  # crosscheck.k5a.claim_ref: chunk_id/extractor/local_id
    kind: Literal["claim"] = field(default="claim", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject)
        nonempty(self.claim)
        nonempty(self.claim_ref)


type Reference = (
    ExistsReference
    | ChoiceReference
    | RequiredParametersReference
    | DefaultReference
    | PathReference
    | ClaimReference
)

LEVEL_OF_KIND: dict[str, Literal["L0", "L1", "L2"]] = {
    "exists": "L0",
    "choice": "L0",
    "required-parameters": "L1",
    "default": "L1",
    "path": "L1",
    "claim": "L2",
}


@dataclass(frozen=True)
class TaskText:
    text: str
    paraphrases: tuple[str, ...]
    writer: str = "template-v2"
    # L2 only: the phrase of the claim the question asks for, from the writer. Task text, not
    # reference: it is outside the identity and evaluation never reads it
    answer: str | None = None

    def __post_init__(self) -> None:
        nonempty(self.text)
        nonempty(self.writer)
        if self.answer is not None:
            nonempty(self.answer)
        if not isinstance(self.paraphrases, tuple):
            raise ValueError("paraphrases must be an immutable tuple")
        if len(self.paraphrases) not in (2, 3):
            raise ValueError("provide two or three paraphrases")
        for text in self.paraphrases:
            nonempty(text)
        if len(set((self.text, *self.paraphrases))) != len(self.paraphrases) + 1:
            raise ValueError("task text and paraphrases must be distinct")


@dataclass(frozen=True)
class Question:
    """Writer input, with no answer. Display name avoids leaking the qualified path in L1."""

    kind: QuestionKind
    subject: Subject
    display_name: str
    options: tuple[ModelOption, ...] = ()
    tested_version: str | None = None


class TaskTextWriter(Protocol):
    def write(self, question: Question) -> TaskText: ...


@dataclass(frozen=True)
class ModelPrompt:
    text: str
    answer_format: Literal["yes-no", "choice-label", "open"]
    options: tuple[ModelOption, ...] = ()


@dataclass(frozen=True)
class TestItem:
    project: str
    chunk_id: str
    chunk_ids: tuple[str, ...]
    level: Literal["L0", "L1", "L2"]
    question_kind: QuestionKind
    reference: Reference
    sources: tuple[Source, ...]
    wording: TaskText
    input_snapshot_hash: str
    docs_version: str
    generator_version: int = 2
    operator_version: int = 2
    # SPEC's named operators apply to usage/perturbation. Recall is not "copy".
    operator: None = None
    format: Literal["python"] = "python"
    difficulty: Literal["explicit-single-step"] = "explicit-single-step"
    source_example_id: None = None
    status: Literal["candidate"] = "candidate"

    def __post_init__(self) -> None:
        for value in (self.project, self.chunk_id, self.input_snapshot_hash, self.docs_version):
            nonempty(value)
        positive(self.generator_version)
        positive(self.operator_version)
        if not isinstance(self.wording, TaskText):
            raise ValueError("task needs validated TaskText")
        if not isinstance(self.sources, tuple) or not all(
            isinstance(s, Source) for s in self.sources
        ):
            raise ValueError("sources must be an immutable tuple of Source objects")
        if not isinstance(self.chunk_ids, tuple):
            raise ValueError("chunk_ids must be an immutable tuple")
        if self.chunk_id not in self.chunk_ids or not self.sources:
            raise ValueError("a task needs sources and its primary chunk")
        for chunk in self.chunk_ids:
            nonempty(chunk)
        if not isinstance(
            self.reference,
            (
                ExistsReference,
                ChoiceReference,
                RequiredParametersReference,
                DefaultReference,
                PathReference,
                ClaimReference,
            ),
        ):
            raise ValueError("unknown reference")
        if self.question_kind != self.reference.kind:
            raise ValueError("question kind and reference disagree")
        if self.level != LEVEL_OF_KIND[self.question_kind]:
            raise ValueError("level and question kind disagree")
        if (self.level == "L2") != (self.wording.answer is not None):
            raise ValueError("an L2 item needs the writer's answer, other levels have none")
        if self.operator is not None or self.source_example_id is not None:
            raise ValueError("inventory recall has no usage operator or source example")
        if (self.format, self.difficulty, self.status) != (
            "python",
            "explicit-single-step",
            "candidate",
        ):
            raise ValueError("only Python, explicit single-step candidates are supported")
        object.__setattr__(self, "chunk_ids", tuple(sorted(set(self.chunk_ids))))
        sort_sources(self)

    @property
    def id(self) -> str:
        from notinspec.tasks.identity import item_id

        return item_id(self)

    def model_prompt(
        self, *, paraphrase: int | None = None, option_order: tuple[str, ...] | None = None
    ) -> ModelPrompt:
        text = self.wording.text if paraphrase is None else self.wording.paraphrases[paraphrase]
        if isinstance(self.reference, ChoiceReference):
            return ModelPrompt(text, "choice-label", self.reference.model_options(option_order))
        if option_order is not None:
            raise ValueError("only MCQ supports option_order")
        return ModelPrompt(text, "yes-no" if self.question_kind == "exists" else "open")


@dataclass(frozen=True)
class SkippedTask:
    symbol: str
    question_kind: str
    reason: str

    def __post_init__(self) -> None:
        for value in (self.symbol, self.question_kind, self.reason):
            nonempty(value)


@dataclass(frozen=True)
class GenerationResult:
    items: tuple[TestItem, ...]
    skipped: tuple[SkippedTask, ...]
