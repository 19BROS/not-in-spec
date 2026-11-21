import pytest

from notinspec.runner.fence import strip_code_fence


@pytest.mark.parametrize(
    "text",
    [
        '```json\n{"a": 1}\n```',
        '```\n{"a": 1}\n```',
        '```JSON  \n{"a": 1}```',
        '```json\r\n{"a": 1}\r\n```',  # issue #30
        '  \n```json\n{"a": 1}\n```\n  ',
    ],
)
def test_one_fence_around_the_whole_text_is_stripped(text: str) -> None:
    assert strip_code_fence(text) == '{"a": 1}'


@pytest.mark.parametrize(
    "text",
    [
        '{"a": 1}',
        'Here it is:\n```json\n{"a": 1}\n```',  # prose before the fence
        '```json {"a": 1}```',  # no line break after the language tag
    ],
)
def test_anything_else_is_unchanged(text: str) -> None:
    assert strip_code_fence(text) == text
