from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_admin_user, get_current_user
from app.core.database import get_db
from app.models.models import Answer, Choice, Question, Quiz, QuizSession, Result, User
from app.schemas.quiz import QuizCreate, QuizDetailResponse, QuizResponse

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("", response_model=QuizDetailResponse, status_code=201)
async def create_quiz(
    body: QuizCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    quiz = Quiz(
        title=body.title,
        description=body.description,
        duration_minutes=body.duration_minutes,
        created_by=admin.id,
    )
    db.add(quiz)
    await db.flush()

    for q_data in body.questions:
        question = Question(quiz_id=quiz.id, text=q_data.text, order=q_data.order)
        db.add(question)
        await db.flush()
        for c_data in q_data.choices:
            db.add(Choice(question_id=question.id, text=c_data.text, is_correct=c_data.is_correct))

    await db.commit()

    res = await db.execute(
        select(Quiz)
        .options(selectinload(Quiz.questions).selectinload(Question.choices))
        .where(Quiz.id == quiz.id)
    )
    return res.scalar_one()


@router.get("/my", response_model=list[QuizResponse])
async def my_quizzes(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    res = await db.execute(
        select(Quiz)
        .options(selectinload(Quiz.questions))
        .where(Quiz.is_active == True, Quiz.created_by == admin.id)
        .order_by(Quiz.created_at.desc())
    )
    quizzes = res.scalars().all()
    return [
        QuizResponse(
            id=q.id, title=q.title, description=q.description,
            duration_minutes=q.duration_minutes, is_active=q.is_active,
            question_count=len(q.questions),
        )
        for q in quizzes
    ]


@router.get("", response_model=list[QuizResponse])
async def list_quizzes(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Quiz)
        .options(selectinload(Quiz.questions))
        .where(Quiz.is_active == True)
        .order_by(Quiz.created_at.desc())
    )
    quizzes = res.scalars().all()
    return [
        QuizResponse(
            id=q.id,
            title=q.title,
            description=q.description,
            duration_minutes=q.duration_minutes,
            is_active=q.is_active,
            question_count=len(q.questions),
        )
        for q in quizzes
    ]


@router.get("/{quiz_id}", response_model=QuizDetailResponse)
async def get_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Quiz)
        .options(selectinload(Quiz.questions).selectinload(Question.choices))
        .where(Quiz.id == quiz_id, Quiz.is_active == True)
    )
    quiz = res.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz topilmadi")
    return quiz


@router.get("/{quiz_id}/stats")
async def quiz_stats(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    # Quiz va savollarni yuklash
    quiz_res = await db.execute(
        select(Quiz)
        .options(selectinload(Quiz.questions).selectinload(Question.choices))
        .where(Quiz.id == quiz_id)
    )
    quiz = quiz_res.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz topilmadi")
    if quiz.created_by != admin.id:
        raise HTTPException(status_code=403, detail="Bu test sizga tegishli emas")

    # To'g'ri javoblar map
    correct_map: dict[int, str] = {}
    for q in quiz.questions:
        for c in q.choices:
            if c.is_correct:
                correct_map[q.id] = c.text

    # Tugatilgan sessiyalarni yuklash
    sessions_res = await db.execute(
        select(QuizSession)
        .options(
            selectinload(QuizSession.user),
            selectinload(QuizSession.answers).selectinload(Answer.choice),
            selectinload(QuizSession.result),
        )
        .where(QuizSession.quiz_id == quiz_id, QuizSession.is_completed == True)
        .order_by(QuizSession.finished_at.desc())
    )
    sessions = sessions_res.scalars().all()

    students = []
    for s in sessions:
        answer_map = {a.question_id: a.choice for a in s.answers}
        question_details = []
        for q in sorted(quiz.questions, key=lambda x: x.order):
            chosen = answer_map.get(q.id)
            chosen_text = chosen.text if chosen else "Javob berilmagan"
            is_correct = chosen.is_correct if chosen else False
            question_details.append({
                "question": q.text,
                "selected": chosen_text,
                "correct_answer": correct_map.get(q.id, ""),
                "is_correct": is_correct,
            })

        students.append({
            "username": s.user.username,
            "score": s.result.score if s.result else 0,
            "correct_answers": s.result.correct_answers if s.result else 0,
            "total_questions": s.result.total_questions if s.result else 0,
            "percentage": s.result.percentage if s.result else 0,
            "finished_at": s.finished_at,
            "questions": question_details,
        })

    return {
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "total_participants": len(students),
        "students": students,
    }
