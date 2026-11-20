"""Frozen task candidates. Answers and model-facing prompts are separate types."""

from dataclasses import dataclass, field
from typing import Literal, Protocol

from packaging.utils import canonicalize_version

from notinspec.inventory import Source, parse_version
from notinspec.inventory.objects import sort_sources

type QuestionKind = Literal["exists", "choice", "required-parameters", "default", "path"]


def nonempty(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a non-empty string")


def positive(value: int) -> None:
    if type(value) is not int or value < 1:
        raise ValueError("versions must be positive integers")


@dataclass(frozen=True)
class Subject:
    symbol: str
    version: str
    parameter: str | None = None

    def __post_init__(self) -> None:
        nonempty(self.symbol)
        nonempty(self.version)
        if parse_version(self.version) is None:
            raise ValueError("tested version must be PEP 440")
        object.__setattr__(self, "version", canonicalize_version(self.version))
        if self.parameter is not None:
            nonempty(self.parameter)


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


@dataclass(frozen=True)
class ExistsReference:
    subject: Subject
    exists: bool
    kind: Literal["exists"] = field(default="exists", init=False)

    def __post_init__(self) -> None:
        check_subject(self.subject)
        if type(self.exists) is not bool:
            raise ValueError("exists must be boolean")


@dataclass(frozen=True)
class ChoiceReference:
    subject: Subject  # the correct symbol/parameter; all choices are frozen below
    options: tuple[Option, ...]
    correct_id: str
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


type Reference = (
    ExistsReference
    | ChoiceReference
    | RequiredParametersReference
    | DefaultReference
    | PathReference
)


@dataclass(frozen=True)
class TaskText:
    text: str
    paraphrases: tuple[str, ...]
    writer: str = "template-v1"

    def __post_init__(self) -> None:
        nonempty(self.text)
        nonempty(self.writer)
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
    options: tuple[Option, ...] = ()


class TaskTextWriter(Protocol):
    def write(self, question: Question) -> TaskText: ...


@dataclass(frozen=True)
class ModelPrompt:
    text: str
    answer_format: Literal["yes-no", "option-id", "open"]
    options: tuple[Option, ...] = ()


@dataclass(frozen=True)
class TestItem:
    project: str
    chunk_id: str
    chunk_ids: tuple[str, ...]
    level: Literal["L0", "L1"]
    question_kind: QuestionKind
    reference: Reference
    sources: tuple[Source, ...]
    wording: TaskText
    input_snapshot_hash: str
    docs_version: str
    generator_version: int = 1
    operator_version: int = 1
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
            ),
        ):
            raise ValueError("unknown reference")
        if self.question_kind != self.reference.kind:
            raise ValueError("question kind and reference disagree")
        expected = "L0" if self.question_kind in ("exists", "choice") else "L1"
        if self.level != expected:
            raise ValueError("level and question kind disagree")
        if self.operator is not None or self.source_example_id is not None:
            raise ValueError("inventory recall has no usage operator or source example")
        if (self.format, self.difficulty, self.status) != (
            "python",
            "explicit-single-step",
            "candidate",
        ):
            raise ValueError("only Python, explicit single-step candidates are supported")
        if parse_version(self.docs_version) != parse_version(self.reference.subject.version):
            raise ValueError("reference version differs from the snapshot's docs version")
        object.__setattr__(self, "chunk_ids", tuple(sorted(set(self.chunk_ids))))
        sort_sources(self)

    @property
    def id(self) -> str:
        from notinspec.tasks.identity import item_id

        return item_id(self)

    def model_prompt(self, *, paraphrase: int | None = None) -> ModelPrompt:
        text = self.wording.text if paraphrase is None else self.wording.paraphrases[paraphrase]
        if isinstance(self.reference, ChoiceReference):
            return ModelPrompt(text, "option-id", self.reference.options)
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
