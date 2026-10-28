"""Why a hard answer failed (SPEC §2.6). Decided by code only, never by a model."""

from enum import StrEnum


class FailureCause(StrEnum):
    STALE_KNOWLEDGE = "stale-knowledge"  # valid against an older spec version
    HALLUCINATED = "hallucinated"  # uses a name absent from every known spec version
    WRONG_LOCATION = "wrong-location"  # right name, wrong place (e.g. query vs body)
    MISSING_REQUIRED = "missing-required"  # required field omitted
    INVALID_VALUE = "invalid-value"  # wrong type or enum value
    WRONG_AUTH = "wrong-auth"  # wrong authentication scheme
    TASK_MISMATCH = "task-mismatch"  # valid request, but not the requested operation or values
    MALFORMED_OUTPUT = "malformed-output"  # answer does not match the answer schema
    REFUSAL = "refusal"  # model declined or said it doesn't know
