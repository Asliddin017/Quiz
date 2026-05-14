import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.models import Answer, Question, Quiz, QuizSession, Result, User


async def _fetch_questions(quiz_id: int) -> list[Question]:
    async with AsyncSessionLocal() as db:
        res = await db.execute(
            select(Question)
            .options(selectinload(Question.choices))
            .where(Question.quiz_id == quiz_id)
        )
        return res.scalars().all()


async def _fetch_answers(session_id: int) -> list[Answer]:
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Answer).where(Answer.session_id == session_id))
        return res.scalars().all()


async def _fetch_quiz_title(quiz_id: int) -> str:
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Quiz.title).where(Quiz.id == quiz_id))
        return res.scalar_one_or_none() or ""


async def calculate_and_save_result(
    session: QuizSession,
    user: User,
) -> dict:
    # asyncio.gather — questions, answers, quiz title parallel yuklash
    questions, answers, quiz_title = await asyncio.gather(
        _fetch_questions(session.quiz_id),
        _fetch_answers(session.id),
        _fetch_quiz_title(session.quiz_id),
    )

    correct_ids = {c.id for q in questions for c in q.choices if c.is_correct}
    answer_map = {a.question_id: a.choice_id for a in answers}

    correct_count = sum(
        1 for q in questions if answer_map.get(q.id) in correct_ids
    )
    total = len(questions)
    percentage = round(correct_count / total * 100, 2) if total > 0 else 0.0

    async with AsyncSessionLocal() as db:
        qs = await db.get(QuizSession, session.id)
        qs.is_completed = True
        qs.finished_at = datetime.now(timezone.utc)

        result = Result(
            session_id=session.id,
            user_id=user.id,
            quiz_id=session.quiz_id,
            score=correct_count * 10,
            total_questions=total,
            correct_answers=correct_count,
            percentage=percentage,
        )
        db.add(result)
        await db.commit()
        await db.refresh(result)

    return {
        "id": result.id,
        "session_id": result.session_id,
        "quiz_id": result.quiz_id,
        "score": result.score,
        "total_questions": result.total_questions,
        "correct_answers": result.correct_answers,
        "percentage": result.percentage,
        "created_at": result.created_at,
        "quiz_title": quiz_title,
    }
