"""Database versions of the pipeline's storage protocols (`claims.store.CallLog`, `ClaimStore`).

The CLI keeps its JSONL files; the worker and the API pass these instead, and the pipeline does
not know the difference (SPEC §18: pipeline code never imports `notinspec.db`).
"""

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from notinspec.claims.model import RawClaim
from notinspec.claims.store import LlmCall, ReuseKey, StoredAnswer
from notinspec.db import models, rows


class DbCallLog:
    """`CallLog`: one transaction per call, so a crash keeps every earlier call (SPEC §10)."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def append(self, call: LlmCall) -> None:
        with Session(self.engine) as session, session.begin():
            run_id = session.scalar(
                select(models.Run.id).where(models.Run.public_id == call.run_id)
            )
            session.add(rows.llm_call(rows.plain(call), run_id))


class DbClaimStore:
    """`ClaimStore` on the append-only `claim_answer` table: the latest answer for a key wins."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def get(self, key: ReuseKey) -> StoredAnswer | None:
        a = models.ClaimAnswer
        query = (
            select(a)
            .where(
                a.content_hash == key.content_hash,
                a.breadcrumb == key.breadcrumb,
                a.extractor == key.extractor,
                a.model == key.model,
                a.prompt_version == key.prompt_version,
                a.reasoning_effort.is_not_distinct_from(key.reasoning_effort),
                a.parser_version.is_not_distinct_from(key.parser_version),
                a.thinking.is_not_distinct_from(key.thinking),
            )
            .order_by(a.id.desc())
            .limit(1)
        )
        with Session(self.engine) as session:
            row = session.scalar(query)
            if row is None:
                return None
            return StoredAnswer(
                claims=tuple(RawClaim(**c) for c in row.claims),
                problems=tuple(row.problems),
                run_id=row.run_ref,
                prompt_hash=row.prompt_hash,
                model=row.answered_model,
            )

    def put(self, key: ReuseKey, answer: StoredAnswer) -> None:
        with Session(self.engine) as session, session.begin():
            session.add(rows.claim_answer(rows.plain(key), rows.plain(answer)))
