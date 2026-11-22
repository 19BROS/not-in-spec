"""Deterministic L0/L1 candidates over the shared Sphinx inventory."""

from notinspec.tasks.generation import GenerationContext
from notinspec.tasks.l0 import generate_l0
from notinspec.tasks.l1 import generate_l1
from notinspec.tasks.models import (
    ChoiceReference,
    DefaultReference,
    ExistsReference,
    GenerationResult,
    ModelOption,
    ModelPrompt,
    Option,
    PathReference,
    Question,
    Reference,
    RequiredParametersReference,
    SkippedTask,
    Subject,
    TaskText,
    TaskTextWriter,
    TestItem,
)
from notinspec.tasks.serialization import dumps, load, loads, save
from notinspec.tasks.text import TemplateWriter

__all__ = [
    "ChoiceReference",
    "DefaultReference",
    "ExistsReference",
    "GenerationContext",
    "GenerationResult",
    "ModelPrompt",
    "ModelOption",
    "Option",
    "PathReference",
    "Question",
    "Reference",
    "RequiredParametersReference",
    "SkippedTask",
    "Subject",
    "TaskText",
    "TaskTextWriter",
    "TemplateWriter",
    "TestItem",
    "dumps",
    "generate_l0",
    "generate_l1",
    "load",
    "loads",
    "save",
]
