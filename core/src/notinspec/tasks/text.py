"""Local templates only; an LLM-backed TaskTextWriter can replace this after QC integration."""

from notinspec.tasks.models import Question, TaskText


class TemplateWriter:
    def write(self, question: Question) -> TaskText:
        s = question.subject
        at = (
            f"in version {question.tested_version}"
            if question.tested_version is not None
            else "according to the supplied documentation"
        )
        if question.kind == "exists":
            target = (
                f"parameter `{s.parameter}` of `{s.symbol}`" if s.parameter else f"`{s.symbol}`"
            )
            text = f"Is {target} part of the documented API {at}? Answer yes or no."
        elif question.kind == "choice":
            target = f"parameter of `{s.symbol}`" if s.parameter else "symbol"
            text = f"Which listed {target} is part of the documented API {at}? Answer A, B, C or D."
        elif question.kind == "required-parameters":
            text = (
                f"List the required parameters of `{s.symbol}` {at}, excluding *args and **kwargs."
            )
        elif question.kind == "default":
            text = f"What is the documented default of `{s.parameter}` in `{s.symbol}` {at}?"
        else:
            text = f"What is the fully qualified path of `{question.display_name}` {at}?"
        return TaskText(
            text,
            (f"Using the documentation: {text}", f"For this API, {text}"),
            writer="template-v3" if question.kind in ("exists", "choice") else "template-v2",
        )
