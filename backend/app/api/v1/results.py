from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import Result, User
from app.schemas.result import ResultResponse

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/me", response_model=list[ResultResponse])
async def my_results(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Result)
        .options(selectinload(Result.quiz))
        .where(Result.user_id == user.id)
        .order_by(Result.created_at.desc())
    )
    results = res.scalars().all()
    return [
        ResultResponse(
            id=r.id,
            session_id=r.session_id,
            quiz_id=r.quiz_id,
            score=r.score,
            total_questions=r.total_questions,
            correct_answers=r.correct_answers,
            percentage=r.percentage,
            created_at=r.created_at,
            quiz_title=r.quiz.title if r.quiz else "",
        )
        for r in results
    ]
