from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.core.database import get_db
from app.core.security import hash_password
from app.models.models import User, Quiz, Question, Choice, Answer, QuizSession, Result

router = APIRouter()


@router.post("/seed", tags=["seed"])
async def seed_database(db: AsyncSession = Depends(get_db)):
    # Clear all data
    await db.execute(delete(Answer))
    await db.execute(delete(Result))
    await db.execute(delete(QuizSession))
    await db.execute(delete(Choice))
    await db.execute(delete(Question))
    await db.execute(delete(Quiz))
    await db.execute(delete(User))
    await db.flush()

    # Create users
    asliddin = User(email="asliddin@example.com", username="Asliddin", hashed_password=hash_password("root123"), role="admin")
    alex = User(email="alex@example.com", username="Alex", hashed_password=hash_password("root123"), role="admin")
    ali = User(email="ali@example.com", username="Ali", hashed_password=hash_password("root123"), role="student")
    zara = User(email="zara@example.com", username="Zara", hashed_password=hash_password("root123"), role="student")
    db.add_all([asliddin, alex, ali, zara])
    await db.flush()

    asliddin_quizzes = [
        {
            "title": "Python Asoslari",
            "description": "Python dasturlash tili bo'yicha test",
            "questions": [
                {"text": "Python qaysi tilda yozilgan?", "choices": [("C", True), ("Java", False), ("C++", False), ("Rust", False)]},
                {"text": "Python da list yaratish uchun qaysi belgi?", "choices": [("{}", False), ("[]", True), ("()", False), ("<>", False)]},
                {"text": "Python da comment qo'yish uchun qaysi belgi?", "choices": [("//", False), ("/*", False), ("#", True), ("--", False)]},
                {"text": "O'zgaruvchi turini aniqlash funksiyasi?", "choices": [("typeof()", False), ("type()", True), ("gettype()", False), ("vartype()", False)]},
            ]
        },
        {
            "title": "Web Texnologiyalar",
            "description": "HTML, CSS va JavaScript bo'yicha test",
            "questions": [
                {"text": "HTML qisqartmasi nima?", "choices": [("Hyper Text Markup Language", True), ("High Tech Modern Language", False), ("Hyper Transfer Markup Language", False), ("Home Tool Markup Language", False)]},
                {"text": "CSS da rang berish xususiyati?", "choices": [("font-color", False), ("text-color", False), ("color", True), ("background", False)]},
                {"text": "JavaScript da massiv uzunligi?", "choices": [("size", False), ("count", False), ("length", True), ("total", False)]},
                {"text": "HTML da havola yaratish tegi?", "choices": [("<link>", False), ("<a>", True), ("<href>", False), ("<url>", False)]},
            ]
        },
        {
            "title": "Ma'lumotlar Bazasi",
            "description": "SQL bo'yicha test",
            "questions": [
                {"text": "Jadvaldan ma'lumot olish buyrug'i?", "choices": [("GET", False), ("FETCH", False), ("SELECT", True), ("RETRIEVE", False)]},
                {"text": "Yangi jadval yaratish buyrug'i?", "choices": [("NEW TABLE", False), ("CREATE TABLE", True), ("MAKE TABLE", False), ("ADD TABLE", False)]},
                {"text": "Shartli so'rov uchun kalit so'z?", "choices": [("IF", False), ("FILTER", False), ("WHERE", True), ("CONDITION", False)]},
                {"text": "PRIMARY KEY vazifasi nima?", "choices": [("Shifrlaydi", False), ("Noyob identifikatsiya qiladi", True), ("Indekslaydi", False), ("Majburiy qiladi", False)]},
            ]
        },
        {
            "title": "Tarmoqlar va Internet",
            "description": "Tarmoq asoslari bo'yicha test",
            "questions": [
                {"text": "HTTP ning to'liq nomi?", "choices": [("HyperText Transfer Protocol", True), ("High Transfer Text Protocol", False), ("Hyper Text Transmission Protocol", False), ("Home Text Transfer Protocol", False)]},
                {"text": "Qaysi port HTTPS uchun standart?", "choices": [("80", False), ("443", True), ("8080", False), ("3000", False)]},
                {"text": "IP manzil necha bitdan iborat (IPv4)?", "choices": [("16", False), ("32", True), ("64", False), ("128", False)]},
                {"text": "DNS nima vazifani bajaradi?", "choices": [("Ma'lumot shifrlaydi", False), ("Domain nomini IP ga aylantiradi", True), ("Tarmoq tezligini oshiradi", False), ("Firewall vazifasini bajaradi", False)]},
            ]
        },
    ]

    alex_quizzes = [
        {
            "title": "Matematika Asoslari",
            "description": "Matematika bo'yicha test",
            "questions": [
                {"text": "2 + 2 = ?", "choices": [("3", False), ("4", True), ("5", False), ("6", False)]},
                {"text": "10 * 5 = ?", "choices": [("40", False), ("45", False), ("50", True), ("55", False)]},
                {"text": "√16 = ?", "choices": [("2", False), ("3", False), ("4", True), ("8", False)]},
                {"text": "2³ = ?", "choices": [("6", False), ("8", True), ("12", False), ("16", False)]},
            ]
        },
        {
            "title": "Ingliz Tili",
            "description": "Ingliz tili grammatikasi bo'yicha test",
            "questions": [
                {"text": "\"I ___ a student\" bo'sh joyga nima?", "choices": [("is", False), ("are", False), ("am", True), ("be", False)]},
                {"text": "\"Cat\" so'zining ko'pligi?", "choices": [("Cats", True), ("Cates", False), ("Cat's", False), ("Caties", False)]},
                {"text": "\"Beautiful\" antonimi?", "choices": [("Pretty", False), ("Ugly", True), ("Nice", False), ("Lovely", False)]},
                {"text": "\"Yesterday I ___ to school\" to'g'ri fe'l?", "choices": [("go", False), ("goes", False), ("went", True), ("going", False)]},
            ]
        },
        {
            "title": "Tarix",
            "description": "Jahon tarixi bo'yicha test",
            "questions": [
                {"text": "Birinchi Jahon urushi qachon boshlangan?", "choices": [("1912", False), ("1914", True), ("1916", False), ("1918", False)]},
                {"text": "Ikkinchi Jahon urushi qachon tugagan?", "choices": [("1943", False), ("1944", False), ("1945", True), ("1946", False)]},
                {"text": "AQSh mustaqilligini qachon e'lon qilgan?", "choices": [("1776", True), ("1789", False), ("1800", False), ("1812", False)]},
                {"text": "Birinchi kosmosga chiqqan davlat?", "choices": [("AQSh", False), ("Xitoy", False), ("SSSR", True), ("Germaniya", False)]},
            ]
        },
        {
            "title": "Geografiya",
            "description": "Jahon geografiyasi bo'yicha test",
            "questions": [
                {"text": "Dunyodagi eng baland tog' qaysi?", "choices": [("K2", False), ("Everest", True), ("Kazbek", False), ("Elbrus", False)]},
                {"text": "Eng katta okean qaysi?", "choices": [("Atlantik", False), ("Hind", False), ("Tinch", True), ("Arktika", False)]},
                {"text": "Avstraliyaning poytaxti qaysi?", "choices": [("Sidney", False), ("Melburn", False), ("Kanberra", True), ("Brisben", False)]},
                {"text": "Nil daryosi qaysi qit'ada?", "choices": [("Osiyo", False), ("Afrika", True), ("Yevropa", False), ("Amerika", False)]},
            ]
        },
    ]

    for quiz_data in asliddin_quizzes:
        quiz = Quiz(title=quiz_data["title"], description=quiz_data["description"], duration_minutes=1, created_by=asliddin.id)
        db.add(quiz)
        await db.flush()
        for i, q in enumerate(quiz_data["questions"]):
            question = Question(quiz_id=quiz.id, text=q["text"], order=i)
            db.add(question)
            await db.flush()
            for text, correct in q["choices"]:
                db.add(Choice(question_id=question.id, text=text, is_correct=correct))

    for quiz_data in alex_quizzes:
        quiz = Quiz(title=quiz_data["title"], description=quiz_data["description"], duration_minutes=1, created_by=alex.id)
        db.add(quiz)
        await db.flush()
        for i, q in enumerate(quiz_data["questions"]):
            question = Question(quiz_id=quiz.id, text=q["text"], order=i)
            db.add(question)
            await db.flush()
            for text, correct in q["choices"]:
                db.add(Choice(question_id=question.id, text=text, is_correct=correct))

    await db.commit()
    return {
        "message": "Seeded successfully",
        "admins": ["Asliddin", "Alex"],
        "students": ["Ali", "Zara"],
        "quizzes_per_admin": 4
    }
