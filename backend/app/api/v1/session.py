import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.redis_client import get_redis
from app.models.models import Answer, Quiz, QuizSession, User
from app.schemas.quiz import AnswerSubmit, SessionStartResponse
from app.schemas.result import ResultResponse
from app.services.result_service import calculate_and_save_result

router = APIRouter(prefix="/sessions", tags=["sessions"])

_executor = ThreadPoolExecutor(max_workers=4)


def _log_session_finish_sync(session_id: int, username: str, percentage: float) -> None:
    """Sinxron log — run_in_executor bilan chaqiriladi."""
    import time
    time.sleep(0.05)  # simulate blocking I/O (file write, external log service, etc.)
    print(f"[LOG] Session {session_id} finished | user={username} | score={percentage}%")


@router.post("/start/{quiz_id}", response_model=SessionStartResponse)
async def start_session(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    quiz_res = await db.execute(
        select(Quiz).where(Quiz.id == quiz_id, Quiz.is_active == True)
    )
    quiz = quiz_res.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz topilmadi")

    active = await db.execute(
        select(QuizSession).where(
            QuizSession.user_id == user.id,
            QuizSession.quiz_id == quiz_id,
            QuizSession.is_completed == False,
        )
    )
    if active.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bu quizda faol sessiya mavjud")

    session = QuizSession(user_id=user.id, quiz_id=quiz_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)

    redis = get_redis()
    deadline = datetime.now(timezone.utc).timestamp() + quiz.duration_minutes * 60
    await redis.set(
        f"session:{session.id}:deadline",
        deadline,
        ex=quiz.duration_minutes * 60 + 60,
    )

    return SessionStartResponse(
        session_id=session.id,
        quiz_id=quiz_id,
        duration_minutes=quiz.duration_minutes,
    )


@router.post("/{session_id}/answer")
async def submit_answer(
    session_id: int,
    body: AnswerSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sess_res = await db.execute(
        select(QuizSession).where(
            QuizSession.id == session_id,
            QuizSession.user_id == user.id,
            QuizSession.is_completed == False,
        )
    )
    session = sess_res.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Faol sessiya topilmadi")

    redis = get_redis()
    deadline = await redis.get(f"session:{session_id}:deadline")
    if deadline and float(deadline) < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=400, detail="Vaqt tugagan")

    existing = await db.execute(
        select(Answer).where(
            Answer.session_id == session_id,
            Answer.question_id == body.question_id,
        )
    )
    answer = existing.scalar_one_or_none()
    if answer:
        answer.choice_id = body.choice_id
    else:
        db.add(Answer(
            session_id=session_id,
            question_id=body.question_id,
            choice_id=body.choice_id,
        ))
    await db.commit()
    return {"message": "Javob saqlandi"}


@router.post("/{session_id}/finish", response_model=ResultResponse)
async def finish_session(
    session_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sess_res = await db.execute(
        select(QuizSession).where(
            QuizSession.id == session_id,
            QuizSession.user_id == user.id,
            QuizSession.is_completed == False,
        )
    )
    session = sess_res.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Faol sessiya topilmadi")

    result = await calculate_and_save_result(session, user)

    redis = get_redis()
    await redis.delete(f"session:{session_id}:deadline")

    # run_in_executor — sinxron logging ni bloklasdan bajarish
    loop = asyncio.get_event_loop()
    background_tasks.add_task(
        loop.run_in_executor,
        _executor,
        _log_session_finish_sync,
        session_id,
        user.username,
        result["percentage"],
    )

    return result
