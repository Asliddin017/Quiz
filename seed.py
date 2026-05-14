"""
Seed script — Asliddin va Alex uchun 3 tadan test yaratadi.
Ishlatish: docker exec -i quiz-platform-backend-1 python seed.py
"""
import asyncio
import httpx

BASE = "http://localhost:8000/api/v1"

ASLIDDIN_QUIZZES = [
    {
        "title": "Python Asoslari",
        "description": "Python dasturlash tili bo'yicha savolar",
        "duration_minutes": 1,
        "questions": [
            {"text": "Python qaysi yilda yaratilgan?", "order": 0, "choices": [
                {"text": "1991", "is_correct": True},
                {"text": "1985", "is_correct": False},
                {"text": "2000", "is_correct": False},
                {"text": "1978", "is_correct": False},
            ]},
            {"text": "Python da ro'yxat (list) qanday belgilanadi?", "order": 1, "choices": [
                {"text": "[]", "is_correct": True},
                {"text": "{}", "is_correct": False},
                {"text": "()", "is_correct": False},
                {"text": "<>", "is_correct": False},
            ]},
            {"text": "Python da funksiya qanday e'lon qilinadi?", "order": 2, "choices": [
                {"text": "def", "is_correct": True},
                {"text": "function", "is_correct": False},
                {"text": "func", "is_correct": False},
                {"text": "fn", "is_correct": False},
            ]},
            {"text": "Python da izoh (comment) qanday yoziladi?", "order": 3, "choices": [
                {"text": "# izoh", "is_correct": True},
                {"text": "// izoh", "is_correct": False},
                {"text": "/* izoh */", "is_correct": False},
                {"text": "-- izoh", "is_correct": False},
            ]},
        ],
    },
    {
        "title": "FastAPI Bilimi",
        "description": "FastAPI framework bo'yicha savollar",
        "duration_minutes": 1,
        "questions": [
            {"text": "FastAPI qaysi til asosida ishlaydi?", "order": 0, "choices": [
                {"text": "Python", "is_correct": True},
                {"text": "JavaScript", "is_correct": False},
                {"text": "Go", "is_correct": False},
                {"text": "Java", "is_correct": False},
            ]},
            {"text": "FastAPI da GET endpoint qanday yoziladi?", "order": 1, "choices": [
                {"text": "@app.get('/')", "is_correct": True},
                {"text": "@app.route('/')", "is_correct": False},
                {"text": "@get('/')", "is_correct": False},
                {"text": "app.get('/')", "is_correct": False},
            ]},
            {"text": "FastAPI avtomatik qanday dokumentatsiya yaratadi?", "order": 2, "choices": [
                {"text": "Swagger UI", "is_correct": True},
                {"text": "Postman", "is_correct": False},
                {"text": "Redoc faqat", "is_correct": False},
                {"text": "Hech qanday", "is_correct": False},
            ]},
            {"text": "FastAPI da ma'lumotlarni tekshirish uchun nima ishlatiladi?", "order": 3, "choices": [
                {"text": "Pydantic", "is_correct": True},
                {"text": "Marshmallow", "is_correct": False},
                {"text": "Cerberus", "is_correct": False},
                {"text": "WTForms", "is_correct": False},
            ]},
        ],
    },
    {
        "title": "Ma'lumotlar Bazasi",
        "description": "SQL va database tushunchalari",
        "duration_minutes": 1,
        "questions": [
            {"text": "SQL da jadvaldan ma'lumot olish uchun qaysi buyruq ishlatiladi?", "order": 0, "choices": [
                {"text": "SELECT", "is_correct": True},
                {"text": "GET", "is_correct": False},
                {"text": "FETCH", "is_correct": False},
                {"text": "READ", "is_correct": False},
            ]},
            {"text": "Primary Key nima?", "order": 1, "choices": [
                {"text": "Har bir qatorni noyob belgilovchi kalit", "is_correct": True},
                {"text": "Eng muhim ustun", "is_correct": False},
                {"text": "Birinchi ustun", "is_correct": False},
                {"text": "Shifrlash kaliti", "is_correct": False},
            ]},
            {"text": "PostgreSQL qaysi turdagi ma'lumotlar bazasi?", "order": 2, "choices": [
                {"text": "Relyatsion (SQL)", "is_correct": True},
                {"text": "NoSQL", "is_correct": False},
                {"text": "Graph", "is_correct": False},
                {"text": "Key-Value", "is_correct": False},
            ]},
            {"text": "Redis asosan nima uchun ishlatiladi?", "order": 3, "choices": [
                {"text": "Cache va tez ma'lumot saqlash", "is_correct": True},
                {"text": "Rasm saqlash", "is_correct": False},
                {"text": "Fayl tizimi", "is_correct": False},
                {"text": "Faqat loglash", "is_correct": False},
            ]},
        ],
    },
]

ALEX_QUIZZES = [
    {
        "title": "Ingliz Tili Grammatikasi",
        "description": "Basic English grammar questions",
        "duration_minutes": 1,
        "questions": [
            {"text": "Which is correct?", "order": 0, "choices": [
                {"text": "She doesn't know", "is_correct": True},
                {"text": "She don't know", "is_correct": False},
                {"text": "She not know", "is_correct": False},
                {"text": "She didn't knows", "is_correct": False},
            ]},
            {"text": "Past tense of 'go' is:", "order": 1, "choices": [
                {"text": "went", "is_correct": True},
                {"text": "goed", "is_correct": False},
                {"text": "goes", "is_correct": False},
                {"text": "going", "is_correct": False},
            ]},
            {"text": "Choose the correct article: ___ apple", "order": 2, "choices": [
                {"text": "an", "is_correct": True},
                {"text": "a", "is_correct": False},
                {"text": "the only", "is_correct": False},
                {"text": "no article", "is_correct": False},
            ]},
            {"text": "Plural of 'child' is:", "order": 3, "choices": [
                {"text": "children", "is_correct": True},
                {"text": "childs", "is_correct": False},
                {"text": "childrens", "is_correct": False},
                {"text": "child's", "is_correct": False},
            ]},
        ],
    },
    {
        "title": "Jahon Tarixi",
        "description": "Jahon tarixi bo'yicha savollar",
        "duration_minutes": 1,
        "questions": [
            {"text": "Birinchi jahon urushi qachon boshlangan?", "order": 0, "choices": [
                {"text": "1914", "is_correct": True},
                {"text": "1939", "is_correct": False},
                {"text": "1905", "is_correct": False},
                {"text": "1920", "is_correct": False},
            ]},
            {"text": "Amerika Qo'shma Shtatlari qachon mustaqillik e'lon qilgan?", "order": 1, "choices": [
                {"text": "1776", "is_correct": True},
                {"text": "1789", "is_correct": False},
                {"text": "1812", "is_correct": False},
                {"text": "1765", "is_correct": False},
            ]},
            {"text": "Buyuk Britaniya poytaxti qaysi shahar?", "order": 2, "choices": [
                {"text": "London", "is_correct": True},
                {"text": "Manchester", "is_correct": False},
                {"text": "Edinburgh", "is_correct": False},
                {"text": "Birmingham", "is_correct": False},
            ]},
            {"text": "Ikkinchi jahon urushi qachon tugagan?", "order": 3, "choices": [
                {"text": "1945", "is_correct": True},
                {"text": "1944", "is_correct": False},
                {"text": "1946", "is_correct": False},
                {"text": "1943", "is_correct": False},
            ]},
        ],
    },
    {
        "title": "Umumiy Bilim",
        "description": "Turli sohalardagi umumiy savollar",
        "duration_minutes": 1,
        "questions": [
            {"text": "Quyosh sistemasidagi eng katta sayyora?", "order": 0, "choices": [
                {"text": "Yupiter", "is_correct": True},
                {"text": "Saturn", "is_correct": False},
                {"text": "Uran", "is_correct": False},
                {"text": "Neptun", "is_correct": False},
            ]},
            {"text": "Suv necha gradusda qaynaydi?", "order": 1, "choices": [
                {"text": "100°C", "is_correct": True},
                {"text": "90°C", "is_correct": False},
                {"text": "80°C", "is_correct": False},
                {"text": "120°C", "is_correct": False},
            ]},
            {"text": "Dunyo bo'yicha eng ko'p gapiriladigan til?", "order": 2, "choices": [
                {"text": "Mandarin (Xitoy)", "is_correct": True},
                {"text": "Ingliz", "is_correct": False},
                {"text": "Ispan", "is_correct": False},
                {"text": "Arab", "is_correct": False},
            ]},
            {"text": "O'zbekiston poytaxti?", "order": 3, "choices": [
                {"text": "Toshkent", "is_correct": True},
                {"text": "Samarqand", "is_correct": False},
                {"text": "Buxoro", "is_correct": False},
                {"text": "Namangan", "is_correct": False},
            ]},
        ],
    },
]


async def login(username: str, password: str, client: httpx.AsyncClient) -> str:
    r = await client.post(f"{BASE}/auth/login", json={"username": username, "password": password})
    return r.json()["access_token"]


async def create_quiz(quiz: dict, token: str, client: httpx.AsyncClient) -> str:
    r = await client.post(
        f"{BASE}/quizzes",
        json=quiz,
        headers={"Authorization": f"Bearer {token}"},
    )
    if r.status_code == 201:
        return f"✓ '{quiz['title']}' yaratildi"
    return f"✗ '{quiz['title']}' xato: {r.text}"


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        print("Loginlar...")
        asliddin_token = await login("Asliddin", "1234567", client)
        alex_token = await login("alex", "root123", client)
        print("✓ Tokenlar olindi\n")

        print("=== Asliddin testlari ===")
        for quiz in ASLIDDIN_QUIZZES:
            print(await create_quiz(quiz, asliddin_token, client))

        print("\n=== Alex testlari ===")
        for quiz in ALEX_QUIZZES:
            print(await create_quiz(quiz, alex_token, client))

        print("\nHammasi tayyor!")


asyncio.run(main())
