from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password
from app.models.models import User, Quiz, Question, Choice

router = APIRouter()


@router.post("/seed", tags=["seed"])
async def seed_database(db: AsyncSession = Depends(get_db)):
    # Check if already seeded
    result = await db.execute(select(User).where(User.username == "Asliddin"))
    if result.scalar_one_or_none():
        return {"message": "Already seeded"}

    # Create admins
    asliddin = User(
        email="asliddin@example.com",
        username="Asliddin",
        hashed_password=hash_password("root123"),
        role="admin",
    )
    alex = User(
        email="alex@example.com",
        username="Alex",
        hashed_password=hash_password("root123"),
        role="admin",
    )
    # Create students
    student1 = User(
        email="ali@example.com",
        username="Ali",
        hashed_password=hash_password("root123"),
        role="student",
    )
    student2 = User(
        email="zara@example.com",
        username="Zara",
        hashed_password=hash_password("root123"),
        role="student",
    )
    db.add_all([asliddin, alex, student1, student2])
    await db.flush()

    # Asliddin's quizzes
    asliddin_quizzes = [
        {
            "title": "Python Asoslari",
            "description": "Python dasturlash tili bo'yicha test",
            "questions": [
                {"text": "Python qaysi tilda yozilgan?", "choices": [
                    ("C", False), ("Java", False), ("C++", True), ("Rust", False)
                ]},
                {"text": "Python da list yaratish uchun qaysi belgi ishlatiladi?", "choices": [
                    ("{}", False), ("[]", True), ("()", False), ("<>", False)
                ]},
                {"text": "Python da comment qo'yish uchun qaysi belgi ishlatiladi?", "choices": [
                    ("//", False), ("/*", False), ("#", True), ("--", False)
                ]},
                {"text": "Python da o'zgaruvchi turini aniqlash uchun qaysi funksiya ishlatiladi?", "choices": [
                    ("typeof()", False), ("type()", True), ("gettype()", False), ("vartype()", False)
                ]},
            ]
        },
        {
            "title": "Web Texnologiyalar",
            "description": "HTML, CSS va JavaScript bo'yicha test",
            "questions": [
                {"text": "HTML qisqartmasi nima?", "choices": [
                    ("Hyper Text Markup Language", True), ("High Tech Modern Language", False),
                    ("Hyper Transfer Markup Language", False), ("Home Tool Markup Language", False)
                ]},
                {"text": "CSS da rang berish uchun qaysi xususiyat ishlatiladi?", "choices": [
                    ("font-color", False), ("text-color", False), ("color", True), ("background", False)
                ]},
                {"text": "JavaScript da massiv uzunligini olish uchun qaysi xususiyat ishlatiladi?", "choices": [
                    ("size", False), ("count", False), ("length", True), ("total", False)
                ]},
                {"text": "HTML da havola yaratish uchun qaysi teg ishlatiladi?", "choices": [
                    ("<link>", False), ("<a>", True), ("<href>", False), ("<url>", False)
                ]},
            ]
        },
        {
            "title": "Ma'lumotlar Bazasi",
            "description": "SQL va ma'lumotlar bazasi bo'yicha test",
            "questions": [
                {"text": "SQL da jadvaldan ma'lumot olish uchun qaysi buyruq ishlatiladi?", "choices": [
                    ("GET", False), ("FETCH", False), ("SELECT", True), ("RETRIEVE", False)
                ]},
                {"text": "SQL da yangi jadval yaratish uchun qaysi buyruq ishlatiladi?", "choices": [
                    ("NEW TABLE", False), ("CREATE TABLE", True), ("MAKE TABLE", False), ("ADD TABLE", False)
                ]},
                {"text": "SQL da shartli so'rov uchun qaysi kalit so'z ishlatiladi?", "choices": [
                    ("IF", False), ("FILTER", False), ("WHERE", True), ("CONDITION", False)
                ]},
                {"text": "PRIMARY KEY nima vazifani bajaradi?", "choices": [
                    ("Ustunni shifrlaydi", False), ("Har bir qatorni noyob identifikatsiya qiladi", True),
                    ("Ustunni indekslaydi", False), ("Ustunni majburiy qiladi", False)
                ]},
            ]
        },
    ]

    # Alex's quizzes
    alex_quizzes = [
        {
            "title": "Matematika Asoslari",
            "description": "Matematika bo'yicha test",
            "questions": [
                {"text": "2 + 2 = ?", "choices": [
                    ("3", False), ("4", True), ("5", False), ("6", False)
                ]},
                {"text": "10 * 5 = ?", "choices": [
                    ("40", False), ("45", False), ("50", True), ("55", False)
                ]},
                {"text": "√16 = ?", "choices": [
                    ("2", False), ("3", False), ("4", True), ("8", False)
                ]},
                {"text": "2³ = ?", "choices": [
                    ("6", False), ("8", True), ("12", False), ("16", False)
                ]},
            ]
        },
        {
            "title": "Ingliz Tili",
            "description": "Ingliz tili grammatikasi bo'yicha test",
            "questions": [
                {"text": "\"I ___ a student\" jumlasida bo'sh joyga nima keladi?", "choices": [
                    ("is", False), ("are", False), ("am", True), ("be", False)
                ]},
                {"text": "\"Cat\" so'zining ko'pligi qaysi?", "choices": [
                    ("Cats", True), ("Cates", False), ("Cat's", False), ("Caties", False)
                ]},
                {"text": "\"Beautiful\" so'zining antonimi qaysi?", "choices": [
                    ("Pretty", False), ("Ugly", True), ("Nice", False), ("Lovely", False)
                ]},
                {"text": "\"Yesterday I ___ to school\" jumlasida to'g'ri fe'l qaysi?", "choices": [
                    ("go", False), ("goes", False), ("went", True), ("going", False)
                ]},
            ]
        },
        {
            "title": "Tarix",
            "description": "Jahon tarixi bo'yicha test",
            "questions": [
                {"text": "Birinchi Jahon urushi qachon boshlangan?", "choices": [
                    ("1912", False), ("1914", True), ("1916", False), ("1918", False)
                ]},
                {"text": "Ikkinchi Jahon urushi qachon tugagan?", "choices": [
                    ("1943", False), ("1944", False), ("1945", True), ("1946", False)
                ]},
                {"text": "Buyuk Britaniya qachon AQSHni mustamlakachilikdan ozod qildi?", "choices": [
                    ("1776", True), ("1789", False), ("1800", False), ("1812", False)
                ]},
                {"text": "Qaysi davlat birinchi bo'lib kosmosga odam uchirgan?", "choices": [
                    ("AQSh", False), ("Xitoy", False), ("SSSR", True), ("Germaniya", False)
                ]},
            ]
        },
    ]

    for quiz_data in asliddin_quizzes:
        quiz = Quiz(
            title=quiz_data["title"],
            description=quiz_data["description"],
            duration_minutes=1,
            created_by=asliddin.id,
        )
        db.add(quiz)
        await db.flush()
        for i, q_data in enumerate(quiz_data["questions"]):
            question = Question(quiz_id=quiz.id, text=q_data["text"], order=i)
            db.add(question)
            await db.flush()
            for choice_text, is_correct in q_data["choices"]:
                db.add(Choice(question_id=question.id, text=choice_text, is_correct=is_correct))

    for quiz_data in alex_quizzes:
        quiz = Quiz(
            title=quiz_data["title"],
            description=quiz_data["description"],
            duration_minutes=1,
            created_by=alex.id,
        )
        db.add(quiz)
        await db.flush()
        for i, q_data in enumerate(quiz_data["questions"]):
            question = Question(quiz_id=quiz.id, text=q_data["text"], order=i)
            db.add(question)
            await db.flush()
            for choice_text, is_correct in q_data["choices"]:
                db.add(Choice(question_id=question.id, text=choice_text, is_correct=is_correct))

    await db.commit()
    return {"message": "Seeded successfully", "users": ["Asliddin", "Alex", "Ali", "Zara"]}
