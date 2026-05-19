"""
English language test seed — 13 variants, each up to 20 questions.
Run inside the backend container:
  docker exec -i quiz-platform-backend-1 python seed_english.py
"""
import asyncio
import httpx

BASE = "http://localhost:8000/api/v1"

ENGLISH_QUIZZES = [
    # ─── Variant 1 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 1",
        "description": "English language test questions - Variant 1",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "This is Lola and her brother, Doniyor. ____ my friends.",
                "order": 0,
                "choices": [
                    {"text": "They're", "is_correct": True},
                    {"text": "We're", "is_correct": False},
                    {"text": "He's", "is_correct": False},
                    {"text": "She's", "is_correct": False},
                ],
            },
            {
                "text": "I ___ a teacher.",
                "order": 1,
                "choices": [
                    {"text": "am", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "She ___ from Uzbekistan.",
                "order": 2,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "They ___ students.",
                "order": 3,
                "choices": [
                    {"text": "are", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "My name ___ Ali.",
                "order": 4,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "We ___ in the classroom.",
                "order": 5,
                "choices": [
                    {"text": "are", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "Tashkent is in ___.",
                "order": 6,
                "choices": [
                    {"text": "Uzbekistan", "is_correct": True},
                    {"text": "Kazakhstan", "is_correct": False},
                    {"text": "Tajikistan", "is_correct": False},
                    {"text": "Kyrgyzstan", "is_correct": False},
                ],
            },
            {
                "text": "Paris is in ___.",
                "order": 7,
                "choices": [
                    {"text": "France", "is_correct": True},
                    {"text": "Germany", "is_correct": False},
                    {"text": "Italy", "is_correct": False},
                    {"text": "Spain", "is_correct": False},
                ],
            },
            {
                "text": "Tokyo is in ___.",
                "order": 8,
                "choices": [
                    {"text": "Japan", "is_correct": True},
                    {"text": "China", "is_correct": False},
                    {"text": "Korea", "is_correct": False},
                    {"text": "Vietnam", "is_correct": False},
                ],
            },
            {
                "text": "25 =",
                "order": 9,
                "choices": [
                    {"text": "twenty-five", "is_correct": True},
                    {"text": "twenty-four", "is_correct": False},
                    {"text": "twenty-six", "is_correct": False},
                    {"text": "two-five", "is_correct": False},
                ],
            },
            {
                "text": "14 =",
                "order": 10,
                "choices": [
                    {"text": "fourteen", "is_correct": True},
                    {"text": "forty", "is_correct": False},
                    {"text": "four", "is_correct": False},
                    {"text": "forty-one", "is_correct": False},
                ],
            },
            {
                "text": "….. are Uzbek and we like plov.",
                "order": 11,
                "choices": [
                    {"text": "We", "is_correct": True},
                    {"text": "They", "is_correct": False},
                    {"text": "You", "is_correct": False},
                    {"text": "I", "is_correct": False},
                ],
            },
            {
                "text": "I'm from Milan. ____ is in Italy.",
                "order": 12,
                "choices": [
                    {"text": "It", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "Milan", "is_correct": False},
                ],
            },
            {
                "text": "Excuse me, how ____ your last name?",
                "order": 13,
                "choices": [
                    {"text": "do you spell", "is_correct": True},
                    {"text": "do you say", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "do you write", "is_correct": False},
                ],
            },
            {
                "text": "Oh, ____ are my keys!",
                "order": 14,
                "choices": [
                    {"text": "here", "is_correct": True},
                    {"text": "there", "is_correct": False},
                    {"text": "where", "is_correct": False},
                    {"text": "how", "is_correct": False},
                ],
            },
            {
                "text": "I'd like ____ apple, please.",
                "order": 15,
                "choices": [
                    {"text": "an", "is_correct": True},
                    {"text": "a", "is_correct": False},
                    {"text": "the", "is_correct": False},
                    {"text": "some", "is_correct": False},
                ],
            },
            {
                "text": "______ name is Jasur. And my ______ is Aliev.",
                "order": 16,
                "choices": [
                    {"text": "My / surname", "is_correct": True},
                    {"text": "His / last name", "is_correct": False},
                    {"text": "My / first name", "is_correct": False},
                    {"text": "Your / surname", "is_correct": False},
                ],
            },
            {
                "text": "______ name is Anna. ______ Anna Baker.",
                "order": 17,
                "choices": [
                    {"text": "Her / She's", "is_correct": True},
                    {"text": "His / He's", "is_correct": False},
                    {"text": "My / I'm", "is_correct": False},
                    {"text": "Your / You're", "is_correct": False},
                ],
            },
            {
                "text": "Where ______ John from? ______is from the US.",
                "order": 18,
                "choices": [
                    {"text": "is / He", "is_correct": True},
                    {"text": "are / They", "is_correct": False},
                    {"text": "does / He", "is_correct": False},
                    {"text": "is / She", "is_correct": False},
                ],
            },
            {
                "text": "I have ______ brother. ______ name is David.",
                "order": 19,
                "choices": [
                    {"text": "a / His", "is_correct": True},
                    {"text": "the / Her", "is_correct": False},
                    {"text": "a / Her", "is_correct": False},
                    {"text": "an / Their", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 2 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 2",
        "description": "English language test questions - Variant 2",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "Pierre is a French boy. ______ from ______.",
                "order": 0,
                "choices": [
                    {"text": "He's / France", "is_correct": True},
                    {"text": "She's / France", "is_correct": False},
                    {"text": "They're / France", "is_correct": False},
                    {"text": "He's / Italy", "is_correct": False},
                ],
            },
            {
                "text": "Lisa and Max are Americans. ______ from the U.S.A.",
                "order": 1,
                "choices": [
                    {"text": "They're", "is_correct": True},
                    {"text": "He's", "is_correct": False},
                    {"text": "She's", "is_correct": False},
                    {"text": "We're", "is_correct": False},
                ],
            },
            {
                "text": "Hello! My ___ ___ Maria. I ___ ___ from Mexico.",
                "order": 2,
                "choices": [
                    {"text": "name is / am not", "is_correct": True},
                    {"text": "name is / am", "is_correct": False},
                    {"text": "names are / am not", "is_correct": False},
                    {"text": "name are / am not", "is_correct": False},
                ],
            },
            {
                "text": "How many ___ are there in the cupboard?",
                "order": 3,
                "choices": [
                    {"text": "cups", "is_correct": True},
                    {"text": "cup", "is_correct": False},
                    {"text": "cupper", "is_correct": False},
                    {"text": "cuppes", "is_correct": False},
                ],
            },
            {
                "text": "In our garden there is ___ huge pine tree.",
                "order": 4,
                "choices": [
                    {"text": "a", "is_correct": True},
                    {"text": "an", "is_correct": False},
                    {"text": "the", "is_correct": False},
                    {"text": "some", "is_correct": False},
                ],
            },
            {
                "text": "I have got ___ money.",
                "order": 5,
                "choices": [
                    {"text": "some", "is_correct": True},
                    {"text": "any", "is_correct": False},
                    {"text": "a", "is_correct": False},
                    {"text": "the", "is_correct": False},
                ],
            },
            {
                "text": "We have ___ books.",
                "order": 6,
                "choices": [
                    {"text": "some", "is_correct": True},
                    {"text": "any", "is_correct": False},
                    {"text": "a", "is_correct": False},
                    {"text": "the", "is_correct": False},
                ],
            },
            {
                "text": "Do you have ___ car?",
                "order": 7,
                "choices": [
                    {"text": "a", "is_correct": True},
                    {"text": "an", "is_correct": False},
                    {"text": "some", "is_correct": False},
                    {"text": "any", "is_correct": False},
                ],
            },
            {
                "text": "She ___ (read) a book now.",
                "order": 8,
                "choices": [
                    {"text": "is reading", "is_correct": True},
                    {"text": "reads", "is_correct": False},
                    {"text": "read", "is_correct": False},
                    {"text": "are reading", "is_correct": False},
                ],
            },
            {
                "text": "They ___ (play) football in the garden.",
                "order": 9,
                "choices": [
                    {"text": "are playing", "is_correct": True},
                    {"text": "is playing", "is_correct": False},
                    {"text": "plays", "is_correct": False},
                    {"text": "play", "is_correct": False},
                ],
            },
            {
                "text": "I ___ (write) a letter at the moment.",
                "order": 10,
                "choices": [
                    {"text": "am writing", "is_correct": True},
                    {"text": "is writing", "is_correct": False},
                    {"text": "write", "is_correct": False},
                    {"text": "are writing", "is_correct": False},
                ],
            },
            {
                "text": "He ___ (watch) TV now.",
                "order": 11,
                "choices": [
                    {"text": "is watching", "is_correct": True},
                    {"text": "are watching", "is_correct": False},
                    {"text": "watch", "is_correct": False},
                    {"text": "watches", "is_correct": False},
                ],
            },
            {
                "text": "We ___ (listen) to music.",
                "order": 12,
                "choices": [
                    {"text": "are listening", "is_correct": True},
                    {"text": "is listening", "is_correct": False},
                    {"text": "listen", "is_correct": False},
                    {"text": "listens", "is_correct": False},
                ],
            },
            {
                "text": "One box, three ___.",
                "order": 13,
                "choices": [
                    {"text": "boxes", "is_correct": True},
                    {"text": "boxs", "is_correct": False},
                    {"text": "box", "is_correct": False},
                    {"text": "boxies", "is_correct": False},
                ],
            },
            {
                "text": "One baby, five ___.",
                "order": 14,
                "choices": [
                    {"text": "babies", "is_correct": True},
                    {"text": "babys", "is_correct": False},
                    {"text": "babes", "is_correct": False},
                    {"text": "baby", "is_correct": False},
                ],
            },
            {
                "text": "Look! The boys ___ (run) in the park.",
                "order": 15,
                "choices": [
                    {"text": "are running", "is_correct": True},
                    {"text": "is running", "is_correct": False},
                    {"text": "run", "is_correct": False},
                    {"text": "runs", "is_correct": False},
                ],
            },
            {
                "text": "She ___ (cook) dinner now.",
                "order": 16,
                "choices": [
                    {"text": "is cooking", "is_correct": True},
                    {"text": "are cooking", "is_correct": False},
                    {"text": "cook", "is_correct": False},
                    {"text": "cooks", "is_correct": False},
                ],
            },
            {
                "text": "The children ___ (play) with their toys.",
                "order": 17,
                "choices": [
                    {"text": "are playing", "is_correct": True},
                    {"text": "is playing", "is_correct": False},
                    {"text": "plays", "is_correct": False},
                    {"text": "play", "is_correct": False},
                ],
            },
            {
                "text": "How ___ rice do we have left?",
                "order": 18,
                "choices": [
                    {"text": "much", "is_correct": True},
                    {"text": "many", "is_correct": False},
                    {"text": "more", "is_correct": False},
                    {"text": "few", "is_correct": False},
                ],
            },
            {
                "text": "How ___ cars are we buying?",
                "order": 19,
                "choices": [
                    {"text": "many", "is_correct": True},
                    {"text": "much", "is_correct": False},
                    {"text": "more", "is_correct": False},
                    {"text": "few", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 3 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 3",
        "description": "English language test questions - Variant 3",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "How ___ water do I need to run the experiment?",
                "order": 0,
                "choices": [
                    {"text": "much", "is_correct": True},
                    {"text": "many", "is_correct": False},
                    {"text": "more", "is_correct": False},
                    {"text": "few", "is_correct": False},
                ],
            },
            {
                "text": "____ tourists visit Uzbekistan.",
                "order": 1,
                "choices": [
                    {"text": "Many", "is_correct": True},
                    {"text": "Much", "is_correct": False},
                    {"text": "More", "is_correct": False},
                    {"text": "A lot", "is_correct": False},
                ],
            },
            {
                "text": "How ___ times did the phone ring?",
                "order": 2,
                "choices": [
                    {"text": "many", "is_correct": True},
                    {"text": "much", "is_correct": False},
                    {"text": "more", "is_correct": False},
                    {"text": "few", "is_correct": False},
                ],
            },
            {
                "text": "Is that your book? Yes, ___ is.",
                "order": 3,
                "choices": [
                    {"text": "it", "is_correct": True},
                    {"text": "that", "is_correct": False},
                    {"text": "he", "is_correct": False},
                    {"text": "this", "is_correct": False},
                ],
            },
            {
                "text": "He is a ___.",
                "order": 4,
                "choices": [
                    {"text": "teacher", "is_correct": True},
                    {"text": "teaches", "is_correct": False},
                    {"text": "teaching", "is_correct": False},
                    {"text": "teached", "is_correct": False},
                ],
            },
            {
                "text": "She works in a hospital. She is a ___.",
                "order": 5,
                "choices": [
                    {"text": "nurse", "is_correct": True},
                    {"text": "doctor", "is_correct": False},
                    {"text": "teacher", "is_correct": False},
                    {"text": "driver", "is_correct": False},
                ],
            },
            {
                "text": "My father is a ___. He fixes cars.",
                "order": 6,
                "choices": [
                    {"text": "mechanic", "is_correct": True},
                    {"text": "doctor", "is_correct": False},
                    {"text": "nurse", "is_correct": False},
                    {"text": "teacher", "is_correct": False},
                ],
            },
            {
                "text": "I want to be a ___ when I grow up.",
                "order": 7,
                "choices": [
                    {"text": "doctor", "is_correct": True},
                    {"text": "doctors", "is_correct": False},
                    {"text": "medicine", "is_correct": False},
                    {"text": "medical", "is_correct": False},
                ],
            },
            {
                "text": "We have many ___ in our city.",
                "order": 8,
                "choices": [
                    {"text": "schools", "is_correct": True},
                    {"text": "school", "is_correct": False},
                    {"text": "schooling", "is_correct": False},
                    {"text": "scholar", "is_correct": False},
                ],
            },
            {
                "text": "___ is a famous restaurant.",
                "order": 9,
                "choices": [
                    {"text": "That", "is_correct": True},
                    {"text": "This", "is_correct": False},
                    {"text": "These", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
            {
                "text": "___ are beautiful flowers.",
                "order": 10,
                "choices": [
                    {"text": "These", "is_correct": True},
                    {"text": "That", "is_correct": False},
                    {"text": "This", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
            {
                "text": "___ are my friends.",
                "order": 11,
                "choices": [
                    {"text": "These", "is_correct": True},
                    {"text": "That", "is_correct": False},
                    {"text": "This", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
            {
                "text": "___ is my brother.",
                "order": 12,
                "choices": [
                    {"text": "This", "is_correct": True},
                    {"text": "These", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                    {"text": "That", "is_correct": False},
                ],
            },
            {
                "text": "___ are in the classroom now.",
                "order": 13,
                "choices": [
                    {"text": "We", "is_correct": True},
                    {"text": "They", "is_correct": False},
                    {"text": "I", "is_correct": False},
                    {"text": "He", "is_correct": False},
                ],
            },
            {
                "text": "Take… bags into the kitchen.",
                "order": 14,
                "choices": [
                    {"text": "those", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "that", "is_correct": False},
                    {"text": "these", "is_correct": False},
                ],
            },
            {
                "text": "Is …. a red flower?",
                "order": 15,
                "choices": [
                    {"text": "that", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "these", "is_correct": False},
                    {"text": "those", "is_correct": False},
                ],
            },
            {
                "text": "Is this a television? Yes, …is.",
                "order": 16,
                "choices": [
                    {"text": "it", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "that", "is_correct": False},
                    {"text": "these", "is_correct": False},
                ],
            },
            {
                "text": "Look at …. man, over there!",
                "order": 17,
                "choices": [
                    {"text": "that", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "these", "is_correct": False},
                    {"text": "those", "is_correct": False},
                ],
            },
            {
                "text": "____ is the place over there where I live.",
                "order": 18,
                "choices": [
                    {"text": "That", "is_correct": True},
                    {"text": "This", "is_correct": False},
                    {"text": "These", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
            {
                "text": "……bottle over there is empty.",
                "order": 19,
                "choices": [
                    {"text": "That", "is_correct": True},
                    {"text": "This", "is_correct": False},
                    {"text": "These", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 4 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 4",
        "description": "English language test questions - Variant 4",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "……are my parents.",
                "order": 0,
                "choices": [
                    {"text": "These", "is_correct": True},
                    {"text": "This", "is_correct": False},
                    {"text": "That", "is_correct": False},
                    {"text": "Those", "is_correct": False},
                ],
            },
            {
                "text": "My father bought …. toys for me.",
                "order": 1,
                "choices": [
                    {"text": "those", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "that", "is_correct": False},
                    {"text": "these", "is_correct": False},
                ],
            },
            {
                "text": "Look at …. birds in the sky.",
                "order": 2,
                "choices": [
                    {"text": "those", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "that", "is_correct": False},
                    {"text": "these", "is_correct": False},
                ],
            },
            {
                "text": "Is …hotel nice?",
                "order": 3,
                "choices": [
                    {"text": "that", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "these", "is_correct": False},
                    {"text": "those", "is_correct": False},
                ],
            },
            {
                "text": "Who is…. man, over there?",
                "order": 4,
                "choices": [
                    {"text": "that", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "these", "is_correct": False},
                    {"text": "those", "is_correct": False},
                ],
            },
            {
                "text": "Why are …. boxes here?",
                "order": 5,
                "choices": [
                    {"text": "these", "is_correct": True},
                    {"text": "this", "is_correct": False},
                    {"text": "that", "is_correct": False},
                    {"text": "those", "is_correct": False},
                ],
            },
            {
                "text": "(Your aunt Rita) … works for a large company.",
                "order": 6,
                "choices": [
                    {"text": "She", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "They", "is_correct": False},
                    {"text": "It", "is_correct": False},
                ],
            },
            {
                "text": "My hobby is ___ books.",
                "order": 7,
                "choices": [
                    {"text": "reading", "is_correct": True},
                    {"text": "read", "is_correct": False},
                    {"text": "reads", "is_correct": False},
                    {"text": "to read", "is_correct": False},
                ],
            },
            {
                "text": "I like ___ football on weekends.",
                "order": 8,
                "choices": [
                    {"text": "playing", "is_correct": True},
                    {"text": "play", "is_correct": False},
                    {"text": "plays", "is_correct": False},
                    {"text": "to play", "is_correct": False},
                ],
            },
            {
                "text": "She enjoys ___ music.",
                "order": 9,
                "choices": [
                    {"text": "listening to", "is_correct": True},
                    {"text": "listen to", "is_correct": False},
                    {"text": "listens to", "is_correct": False},
                    {"text": "to listen", "is_correct": False},
                ],
            },
            {
                "text": "Their hobby is ___ photos.",
                "order": 10,
                "choices": [
                    {"text": "taking", "is_correct": True},
                    {"text": "take", "is_correct": False},
                    {"text": "takes", "is_correct": False},
                    {"text": "to take", "is_correct": False},
                ],
            },
            {
                "text": "We love ___ movies at home.",
                "order": 11,
                "choices": [
                    {"text": "watching", "is_correct": True},
                    {"text": "watch", "is_correct": False},
                    {"text": "watches", "is_correct": False},
                    {"text": "to watch", "is_correct": False},
                ],
            },
            {
                "text": "I like my brother. I love ___.",
                "order": 12,
                "choices": [
                    {"text": "him", "is_correct": True},
                    {"text": "her", "is_correct": False},
                    {"text": "them", "is_correct": False},
                    {"text": "it", "is_correct": False},
                ],
            },
            {
                "text": "She is my friend. I can call ___ anytime.",
                "order": 13,
                "choices": [
                    {"text": "her", "is_correct": True},
                    {"text": "him", "is_correct": False},
                    {"text": "them", "is_correct": False},
                    {"text": "it", "is_correct": False},
                ],
            },
            {
                "text": "This is my father. I help ___ every day.",
                "order": 14,
                "choices": [
                    {"text": "him", "is_correct": True},
                    {"text": "her", "is_correct": False},
                    {"text": "them", "is_correct": False},
                    {"text": "it", "is_correct": False},
                ],
            },
            {
                "text": "They are my friends. I often meet ___.",
                "order": 15,
                "choices": [
                    {"text": "them", "is_correct": True},
                    {"text": "him", "is_correct": False},
                    {"text": "her", "is_correct": False},
                    {"text": "it", "is_correct": False},
                ],
            },
            {
                "text": "I have a cat. I feed ___ every morning.",
                "order": 16,
                "choices": [
                    {"text": "it", "is_correct": True},
                    {"text": "him", "is_correct": False},
                    {"text": "her", "is_correct": False},
                    {"text": "them", "is_correct": False},
                ],
            },
            {
                "text": "(John and I) . . . have a favorite restaurant.",
                "order": 17,
                "choices": [
                    {"text": "We", "is_correct": True},
                    {"text": "They", "is_correct": False},
                    {"text": "You", "is_correct": False},
                    {"text": "I", "is_correct": False},
                ],
            },
            {
                "text": "Is this ice-cream for ...... or for you?",
                "order": 18,
                "choices": [
                    {"text": "me", "is_correct": True},
                    {"text": "I", "is_correct": False},
                    {"text": "my", "is_correct": False},
                    {"text": "mine", "is_correct": False},
                ],
            },
            {
                "text": "(Sardor's motorbike) . . . has a very noisy engine.",
                "order": 19,
                "choices": [
                    {"text": "It", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "They", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 5 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 5",
        "description": "English language test questions - Variant 5",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "Malik has a dog. . . . . is white.",
                "order": 0,
                "choices": [
                    {"text": "It", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "They", "is_correct": False},
                ],
            },
            {
                "text": "(Jim, Aziz, and Harry) . . .. went biking together.",
                "order": 1,
                "choices": [
                    {"text": "They", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "We", "is_correct": False},
                ],
            },
            {
                "text": "(Our parents) . . .... live in a sweet home.",
                "order": 2,
                "choices": [
                    {"text": "They", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "We", "is_correct": False},
                ],
            },
            {
                "text": "(My friend, Rick) . . .. was honored by the president.",
                "order": 3,
                "choices": [
                    {"text": "He", "is_correct": True},
                    {"text": "She", "is_correct": False},
                    {"text": "They", "is_correct": False},
                    {"text": "It", "is_correct": False},
                ],
            },
            {
                "text": "She took ........",
                "order": 4,
                "choices": [
                    {"text": "it", "is_correct": True},
                    {"text": "him", "is_correct": False},
                    {"text": "her", "is_correct": False},
                    {"text": "them", "is_correct": False},
                ],
            },
            {
                "text": "My cousins are visiting us. . . . . are very nice.",
                "order": 5,
                "choices": [
                    {"text": "They", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "It", "is_correct": False},
                ],
            },
            {
                "text": "(The cute girl) . . .. is the youngest student.",
                "order": 6,
                "choices": [
                    {"text": "She", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "They", "is_correct": False},
                    {"text": "It", "is_correct": False},
                ],
            },
            {
                "text": "My mother has a car. ........ is a Lacetti.",
                "order": 7,
                "choices": [
                    {"text": "It", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "They", "is_correct": False},
                ],
            },
            {
                "text": "(The city - Delhi) . . .. is the capital city of India.",
                "order": 8,
                "choices": [
                    {"text": "It", "is_correct": True},
                    {"text": "He", "is_correct": False},
                    {"text": "She", "is_correct": False},
                    {"text": "They", "is_correct": False},
                ],
            },
            {
                "text": "At ten we go _____ bed.",
                "order": 9,
                "choices": [
                    {"text": "to", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "on", "is_correct": False},
                ],
            },
            {
                "text": "He picks up the apples _____ the tree.",
                "order": 10,
                "choices": [
                    {"text": "from", "is_correct": True},
                    {"text": "of", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                ],
            },
            {
                "text": "She lives _____ Switzerland.",
                "order": 11,
                "choices": [
                    {"text": "in", "is_correct": True},
                    {"text": "at", "is_correct": False},
                    {"text": "on", "is_correct": False},
                    {"text": "from", "is_correct": False},
                ],
            },
            {
                "text": "There's a letter _____ you.",
                "order": 12,
                "choices": [
                    {"text": "for", "is_correct": True},
                    {"text": "to", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "from", "is_correct": False},
                ],
            },
            {
                "text": "Tourists come _____ the boat.",
                "order": 13,
                "choices": [
                    {"text": "by", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "on", "is_correct": False},
                    {"text": "from", "is_correct": False},
                ],
            },
            {
                "text": "He speaks to people _____ the radio.",
                "order": 14,
                "choices": [
                    {"text": "on", "is_correct": True},
                    {"text": "by", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                ],
            },
            {
                "text": "The books are ___ the table.",
                "order": 15,
                "choices": [
                    {"text": "on", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
            {
                "text": "The cat is ___ the chair.",
                "order": 16,
                "choices": [
                    {"text": "on", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
            {
                "text": "The picture is ___ the wall.",
                "order": 17,
                "choices": [
                    {"text": "on", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
            {
                "text": "The keys are ___ my bag.",
                "order": 18,
                "choices": [
                    {"text": "in", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
            {
                "text": "The ball is ___ the box.",
                "order": 19,
                "choices": [
                    {"text": "in", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 6 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 6",
        "description": "English language test questions - Variant 6",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "The lamp is ___ the table.",
                "order": 0,
                "choices": [
                    {"text": "on", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "under", "is_correct": False},
                ],
            },
            {
                "text": "There is a garden ___ the house.",
                "order": 1,
                "choices": [
                    {"text": "behind", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                ],
            },
            {
                "text": "The shoes are ___ the door.",
                "order": 2,
                "choices": [
                    {"text": "near", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "behind", "is_correct": False},
                ],
            },
            {
                "text": "The school is ___ the park.",
                "order": 3,
                "choices": [
                    {"text": "near", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "behind", "is_correct": False},
                ],
            },
            {
                "text": "The dog is ___ the sofa.",
                "order": 4,
                "choices": [
                    {"text": "under", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "behind", "is_correct": False},
                ],
            },
            {
                "text": "He drives the children _____ school.",
                "order": 5,
                "choices": [
                    {"text": "to", "is_correct": True},
                    {"text": "at", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "from", "is_correct": False},
                ],
            },
            {
                "text": "She goes skiing _____ her free time.",
                "order": 6,
                "choices": [
                    {"text": "in", "is_correct": True},
                    {"text": "at", "is_correct": False},
                    {"text": "on", "is_correct": False},
                    {"text": "during", "is_correct": False},
                ],
            },
            {
                "text": "He works _____ an undertaker.",
                "order": 7,
                "choices": [
                    {"text": "as", "is_correct": True},
                    {"text": "like", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "for", "is_correct": False},
                ],
            },
            {
                "text": "Does she live in Australia? No, she _____.",
                "order": 8,
                "choices": [
                    {"text": "doesn't", "is_correct": True},
                    {"text": "don't", "is_correct": False},
                    {"text": "isn't", "is_correct": False},
                    {"text": "aren't", "is_correct": False},
                ],
            },
            {
                "text": "We _____ _____ watching television.",
                "order": 9,
                "choices": [
                    {"text": "don't like", "is_correct": True},
                    {"text": "doesn't like", "is_correct": False},
                    {"text": "aren't like", "is_correct": False},
                    {"text": "isn't like", "is_correct": False},
                ],
            },
            {
                "text": "He lives _____ his family.",
                "order": 10,
                "choices": [
                    {"text": "with", "is_correct": True},
                    {"text": "to", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                ],
            },
            {
                "text": "We are _____ Uzbekistan.",
                "order": 11,
                "choices": [
                    {"text": "from", "is_correct": True},
                    {"text": "in", "is_correct": False},
                    {"text": "at", "is_correct": False},
                    {"text": "to", "is_correct": False},
                ],
            },
            {
                "text": "Smoking is a _____ habit.",
                "order": 12,
                "choices": [
                    {"text": "bad", "is_correct": True},
                    {"text": "good", "is_correct": False},
                    {"text": "nice", "is_correct": False},
                    {"text": "great", "is_correct": False},
                ],
            },
            {
                "text": "___ your neighbors friendly?",
                "order": 13,
                "choices": [
                    {"text": "Are", "is_correct": True},
                    {"text": "Is", "is_correct": False},
                    {"text": "Do", "is_correct": False},
                    {"text": "Does", "is_correct": False},
                ],
            },
            {
                "text": "___ your neighbor a teacher?",
                "order": 14,
                "choices": [
                    {"text": "Is", "is_correct": True},
                    {"text": "Are", "is_correct": False},
                    {"text": "Do", "is_correct": False},
                    {"text": "Does", "is_correct": False},
                ],
            },
            {
                "text": "Where ___ your neighbors live?",
                "order": 15,
                "choices": [
                    {"text": "do", "is_correct": True},
                    {"text": "does", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "is", "is_correct": False},
                ],
            },
            {
                "text": "How ___ your neighbors?",
                "order": 16,
                "choices": [
                    {"text": "are", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "do", "is_correct": False},
                    {"text": "does", "is_correct": False},
                ],
            },
            {
                "text": "___ you like your neighbors?",
                "order": 17,
                "choices": [
                    {"text": "Do", "is_correct": True},
                    {"text": "Does", "is_correct": False},
                    {"text": "Are", "is_correct": False},
                    {"text": "Is", "is_correct": False},
                ],
            },
            {
                "text": "They have a ___ dog.",
                "order": 18,
                "choices": [
                    {"text": "big", "is_correct": True},
                    {"text": "biggest", "is_correct": False},
                    {"text": "bigger", "is_correct": False},
                    {"text": "biger", "is_correct": False},
                ],
            },
            {
                "text": "My neighbor has a ___ garden.",
                "order": 19,
                "choices": [
                    {"text": "beautiful", "is_correct": True},
                    {"text": "beautifull", "is_correct": False},
                    {"text": "beauty", "is_correct": False},
                    {"text": "beautify", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 7 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 7",
        "description": "English language test questions - Variant 7",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "I have a ___ car.",
                "order": 0,
                "choices": [
                    {"text": "new", "is_correct": True},
                    {"text": "news", "is_correct": False},
                    {"text": "newly", "is_correct": False},
                    {"text": "newer", "is_correct": False},
                ],
            },
            {
                "text": "Our neighbors live in a ___ house.",
                "order": 1,
                "choices": [
                    {"text": "big", "is_correct": True},
                    {"text": "biggest", "is_correct": False},
                    {"text": "bigger", "is_correct": False},
                    {"text": "biger", "is_correct": False},
                ],
            },
            {
                "text": "She has a ___ cat.",
                "order": 2,
                "choices": [
                    {"text": "cute", "is_correct": True},
                    {"text": "cutely", "is_correct": False},
                    {"text": "cuter", "is_correct": False},
                    {"text": "cutest", "is_correct": False},
                ],
            },
            {
                "text": "The team played _____ and lost the match.",
                "order": 3,
                "choices": [
                    {"text": "badly", "is_correct": True},
                    {"text": "bad", "is_correct": False},
                    {"text": "worse", "is_correct": False},
                    {"text": "baddly", "is_correct": False},
                ],
            },
            {
                "text": "Please listen _____.",
                "order": 4,
                "choices": [
                    {"text": "carefully", "is_correct": True},
                    {"text": "careful", "is_correct": False},
                    {"text": "careless", "is_correct": False},
                    {"text": "carfully", "is_correct": False},
                ],
            },
            {
                "text": "The homework was the _____.",
                "order": 5,
                "choices": [
                    {"text": "easiest", "is_correct": True},
                    {"text": "easy", "is_correct": False},
                    {"text": "easier", "is_correct": False},
                    {"text": "most easy", "is_correct": False},
                ],
            },
            {
                "text": "Peter's very _____ at tennis. He won the game.",
                "order": 6,
                "choices": [
                    {"text": "good", "is_correct": True},
                    {"text": "well", "is_correct": False},
                    {"text": "best", "is_correct": False},
                    {"text": "better", "is_correct": False},
                ],
            },
            {
                "text": "I know the Prime Minister _____.",
                "order": 7,
                "choices": [
                    {"text": "personally", "is_correct": True},
                    {"text": "personal", "is_correct": False},
                    {"text": "person", "is_correct": False},
                    {"text": "personaly", "is_correct": False},
                ],
            },
            {
                "text": "My husband's a _____ cook.",
                "order": 8,
                "choices": [
                    {"text": "good", "is_correct": True},
                    {"text": "well", "is_correct": False},
                    {"text": "best", "is_correct": False},
                    {"text": "better", "is_correct": False},
                ],
            },
            {
                "text": "He is a…. man.",
                "order": 9,
                "choices": [
                    {"text": "tall", "is_correct": True},
                    {"text": "taller", "is_correct": False},
                    {"text": "tallest", "is_correct": False},
                    {"text": "tally", "is_correct": False},
                ],
            },
            {
                "text": "The road is…. It is 400 km.",
                "order": 10,
                "choices": [
                    {"text": "long", "is_correct": True},
                    {"text": "longer", "is_correct": False},
                    {"text": "longest", "is_correct": False},
                    {"text": "shortly", "is_correct": False},
                ],
            },
            {
                "text": "This is a ….girl.",
                "order": 11,
                "choices": [
                    {"text": "beautiful", "is_correct": True},
                    {"text": "beauty", "is_correct": False},
                    {"text": "beautifully", "is_correct": False},
                    {"text": "beautified", "is_correct": False},
                ],
            },
            {
                "text": "In summer we like to drink…. water.",
                "order": 12,
                "choices": [
                    {"text": "cold", "is_correct": True},
                    {"text": "hot", "is_correct": False},
                    {"text": "colder", "is_correct": False},
                    {"text": "coldly", "is_correct": False},
                ],
            },
            {
                "text": "We wear …. clothes in winter.",
                "order": 13,
                "choices": [
                    {"text": "warm", "is_correct": True},
                    {"text": "cool", "is_correct": False},
                    {"text": "warmer", "is_correct": False},
                    {"text": "warmly", "is_correct": False},
                ],
            },
            {
                "text": "I _______ many friends.",
                "order": 14,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "is", "is_correct": False},
                ],
            },
            {
                "text": "The beggar _______ a stick.",
                "order": 15,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "I _______ no sister.",
                "order": 16,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "is", "is_correct": False},
                ],
            },
            {
                "text": "My parents _____ a beautiful house.",
                "order": 17,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "My father ___ a new job now.",
                "order": 18,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "My brother ___ a lot of friends now.",
                "order": 19,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 8 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 8",
        "description": "English language test questions - Variant 8",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "I ___ a new bike.",
                "order": 0,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "is", "is_correct": False},
                ],
            },
            {
                "text": "She ___ a cat.",
                "order": 1,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "We ___ two sisters.",
                "order": 2,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "He ___ a big house.",
                "order": 3,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "They ___ a garden.",
                "order": 4,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "This is my bag. ___ bag is red.",
                "order": 5,
                "choices": [
                    {"text": "My", "is_correct": True},
                    {"text": "His", "is_correct": False},
                    {"text": "Her", "is_correct": False},
                    {"text": "Their", "is_correct": False},
                ],
            },
            {
                "text": "He is my friend. ___ name is Tom.",
                "order": 6,
                "choices": [
                    {"text": "His", "is_correct": True},
                    {"text": "Her", "is_correct": False},
                    {"text": "My", "is_correct": False},
                    {"text": "Their", "is_correct": False},
                ],
            },
            {
                "text": "We have a dog. ___ dog is friendly.",
                "order": 7,
                "choices": [
                    {"text": "Our", "is_correct": True},
                    {"text": "Their", "is_correct": False},
                    {"text": "My", "is_correct": False},
                    {"text": "His", "is_correct": False},
                ],
            },
            {
                "text": "She has a pencil. ___ pencil is blue.",
                "order": 8,
                "choices": [
                    {"text": "Her", "is_correct": True},
                    {"text": "His", "is_correct": False},
                    {"text": "My", "is_correct": False},
                    {"text": "Our", "is_correct": False},
                ],
            },
            {
                "text": "I have a brother. ___ brother is tall.",
                "order": 9,
                "choices": [
                    {"text": "My", "is_correct": True},
                    {"text": "His", "is_correct": False},
                    {"text": "Her", "is_correct": False},
                    {"text": "Our", "is_correct": False},
                ],
            },
            {
                "text": "I do not _______ any bad manners.",
                "order": 10,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "My cousin ___ a new girlfriend.",
                "order": 11,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "The pupil ___ an old pencil box.",
                "order": 12,
                "choices": [
                    {"text": "has", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "You ____ different names.",
                "order": 13,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "Last year, we _______ no difficulty at school.",
                "order": 14,
                "choices": [
                    {"text": "had", "is_correct": True},
                    {"text": "have", "is_correct": False},
                    {"text": "has", "is_correct": False},
                    {"text": "were", "is_correct": False},
                ],
            },
            {
                "text": "He does not _______ any control over his juniors.",
                "order": 15,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "had", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "My bicycle too, did not _______ brakes.",
                "order": 16,
                "choices": [
                    {"text": "have", "is_correct": True},
                    {"text": "has", "is_correct": False},
                    {"text": "had", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "My mother is my ___.",
                "order": 17,
                "choices": [
                    {"text": "parent", "is_correct": True},
                    {"text": "child", "is_correct": False},
                    {"text": "sibling", "is_correct": False},
                    {"text": "spouse", "is_correct": False},
                ],
            },
            {
                "text": "He is my father. I am his ___.",
                "order": 18,
                "choices": [
                    {"text": "son", "is_correct": True},
                    {"text": "daughter", "is_correct": False},
                    {"text": "child", "is_correct": False},
                    {"text": "sibling", "is_correct": False},
                ],
            },
            {
                "text": "This is my sister. She is my ___.",
                "order": 19,
                "choices": [
                    {"text": "sibling", "is_correct": True},
                    {"text": "parent", "is_correct": False},
                    {"text": "child", "is_correct": False},
                    {"text": "spouse", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 9 ────────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 9",
        "description": "English language test questions - Variant 9",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "I am their ___.",
                "order": 0,
                "choices": [
                    {"text": "child", "is_correct": True},
                    {"text": "parent", "is_correct": False},
                    {"text": "sibling", "is_correct": False},
                    {"text": "spouse", "is_correct": False},
                ],
            },
            {
                "text": "My uncle is my father's ___.",
                "order": 1,
                "choices": [
                    {"text": "brother", "is_correct": True},
                    {"text": "son", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "nephew", "is_correct": False},
                ],
            },
            {
                "text": "My sister is tall. My brother is ___.",
                "order": 2,
                "choices": [
                    {"text": "short", "is_correct": True},
                    {"text": "tall", "is_correct": False},
                    {"text": "long", "is_correct": False},
                    {"text": "big", "is_correct": False},
                ],
            },
            {
                "text": "This book is new. That book is ___.",
                "order": 3,
                "choices": [
                    {"text": "old", "is_correct": True},
                    {"text": "new", "is_correct": False},
                    {"text": "young", "is_correct": False},
                    {"text": "fresh", "is_correct": False},
                ],
            },
            {
                "text": "My house is big. My friend's house is ___.",
                "order": 4,
                "choices": [
                    {"text": "small", "is_correct": True},
                    {"text": "big", "is_correct": False},
                    {"text": "large", "is_correct": False},
                    {"text": "huge", "is_correct": False},
                ],
            },
            {
                "text": "The weather is hot. Yesterday it was ___.",
                "order": 5,
                "choices": [
                    {"text": "cold", "is_correct": True},
                    {"text": "hot", "is_correct": False},
                    {"text": "warm", "is_correct": False},
                    {"text": "cool", "is_correct": False},
                ],
            },
            {
                "text": "The movie was interesting. The book was ___.",
                "order": 6,
                "choices": [
                    {"text": "boring", "is_correct": True},
                    {"text": "interesting", "is_correct": False},
                    {"text": "exciting", "is_correct": False},
                    {"text": "fun", "is_correct": False},
                ],
            },
            {
                "text": "My mother's daughter is my……",
                "order": 7,
                "choices": [
                    {"text": "sister", "is_correct": True},
                    {"text": "brother", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "niece", "is_correct": False},
                ],
            },
            {
                "text": "My mother's mother is my…….",
                "order": 8,
                "choices": [
                    {"text": "grandmother", "is_correct": True},
                    {"text": "aunt", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "mother", "is_correct": False},
                ],
            },
            {
                "text": "My father's son is my…….",
                "order": 9,
                "choices": [
                    {"text": "brother", "is_correct": True},
                    {"text": "sister", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "nephew", "is_correct": False},
                ],
            },
            {
                "text": "My step-mother's son is my……",
                "order": 10,
                "choices": [
                    {"text": "step-brother", "is_correct": True},
                    {"text": "brother", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "half-brother", "is_correct": False},
                ],
            },
            {
                "text": "My brother's daughter is my……",
                "order": 11,
                "choices": [
                    {"text": "niece", "is_correct": True},
                    {"text": "nephew", "is_correct": False},
                    {"text": "cousin", "is_correct": False},
                    {"text": "sister", "is_correct": False},
                ],
            },
            {
                "text": "My grandpa's father is my…..",
                "order": 12,
                "choices": [
                    {"text": "great-grandfather", "is_correct": True},
                    {"text": "grandfather", "is_correct": False},
                    {"text": "great-uncle", "is_correct": False},
                    {"text": "grand-uncle", "is_correct": False},
                ],
            },
            {
                "text": "My dad's brother is my….",
                "order": 13,
                "choices": [
                    {"text": "uncle", "is_correct": True},
                    {"text": "cousin", "is_correct": False},
                    {"text": "nephew", "is_correct": False},
                    {"text": "brother", "is_correct": False},
                ],
            },
            {
                "text": "My female spouse is my….",
                "order": 14,
                "choices": [
                    {"text": "wife", "is_correct": True},
                    {"text": "husband", "is_correct": False},
                    {"text": "partner", "is_correct": False},
                    {"text": "girlfriend", "is_correct": False},
                ],
            },
            {
                "text": "Antonym: leave",
                "order": 15,
                "choices": [
                    {"text": "arrive", "is_correct": True},
                    {"text": "go", "is_correct": False},
                    {"text": "depart", "is_correct": False},
                    {"text": "exit", "is_correct": False},
                ],
            },
            {
                "text": "Antonym: high",
                "order": 16,
                "choices": [
                    {"text": "low", "is_correct": True},
                    {"text": "tall", "is_correct": False},
                    {"text": "big", "is_correct": False},
                    {"text": "up", "is_correct": False},
                ],
            },
            {
                "text": "Antonym: brave",
                "order": 17,
                "choices": [
                    {"text": "cowardly", "is_correct": True},
                    {"text": "fearless", "is_correct": False},
                    {"text": "bold", "is_correct": False},
                    {"text": "daring", "is_correct": False},
                ],
            },
            {
                "text": "Antonym: Ill",
                "order": 18,
                "choices": [
                    {"text": "healthy", "is_correct": True},
                    {"text": "sick", "is_correct": False},
                    {"text": "unwell", "is_correct": False},
                    {"text": "tired", "is_correct": False},
                ],
            },
            {
                "text": "My grandparents ____________ in Italy.",
                "order": 19,
                "choices": [
                    {"text": "live", "is_correct": True},
                    {"text": "lives", "is_correct": False},
                    {"text": "living", "is_correct": False},
                    {"text": "lived", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 10 ───────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 10",
        "description": "English language test questions - Variant 10",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "We _____________ films on TV every day.",
                "order": 0,
                "choices": [
                    {"text": "watch", "is_correct": True},
                    {"text": "watches", "is_correct": False},
                    {"text": "watching", "is_correct": False},
                    {"text": "watched", "is_correct": False},
                ],
            },
            {
                "text": "Kate and Peter ___________ to the same college.",
                "order": 1,
                "choices": [
                    {"text": "go", "is_correct": True},
                    {"text": "goes", "is_correct": False},
                    {"text": "going", "is_correct": False},
                    {"text": "went", "is_correct": False},
                ],
            },
            {
                "text": "What ________ you ______ at noon?",
                "order": 2,
                "choices": [
                    {"text": "do / do", "is_correct": True},
                    {"text": "does / does", "is_correct": False},
                    {"text": "are / doing", "is_correct": False},
                    {"text": "did / do", "is_correct": False},
                ],
            },
            {
                "text": "To be / they / teachers →",
                "order": 3,
                "choices": [
                    {"text": "They are teachers", "is_correct": True},
                    {"text": "They is teachers", "is_correct": False},
                    {"text": "They be teachers", "is_correct": False},
                    {"text": "They were teachers", "is_correct": False},
                ],
            },
            {
                "text": "she / to be / nurse / a →",
                "order": 4,
                "choices": [
                    {"text": "She is a nurse", "is_correct": True},
                    {"text": "She are a nurse", "is_correct": False},
                    {"text": "She be a nurse", "is_correct": False},
                    {"text": "She was a nurse", "is_correct": False},
                ],
            },
            {
                "text": "My favorite color ___ blue.",
                "order": 5,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "I have ___ brother and sister.",
                "order": 6,
                "choices": [
                    {"text": "a", "is_correct": True},
                    {"text": "an", "is_correct": False},
                    {"text": "the", "is_correct": False},
                    {"text": "some", "is_correct": False},
                ],
            },
            {
                "text": "I go to school ___ bus.",
                "order": 7,
                "choices": [
                    {"text": "by", "is_correct": True},
                    {"text": "on", "is_correct": False},
                    {"text": "in", "is_correct": False},
                    {"text": "with", "is_correct": False},
                ],
            },
            {
                "text": "It ___ raining now.",
                "order": 8,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "The weather ___ cold in winter.",
                "order": 9,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "It ___ windy outside.",
                "order": 10,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "I like it when it ___ warm.",
                "order": 11,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "It ___ cloudy in the morning.",
                "order": 12,
                "choices": [
                    {"text": "was", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "were", "is_correct": False},
                ],
            },
            {
                "text": "In summer, it usually ___ hot.",
                "order": 13,
                "choices": [
                    {"text": "is", "is_correct": True},
                    {"text": "am", "is_correct": False},
                    {"text": "are", "is_correct": False},
                    {"text": "be", "is_correct": False},
                ],
            },
            {
                "text": "Sometimes it ___ snow in December.",
                "order": 14,
                "choices": [
                    {"text": "does", "is_correct": True},
                    {"text": "do", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "are", "is_correct": False},
                ],
            },
            {
                "text": "Last summer I ___ to Paris.",
                "order": 15,
                "choices": [
                    {"text": "went", "is_correct": True},
                    {"text": "go", "is_correct": False},
                    {"text": "goes", "is_correct": False},
                    {"text": "gone", "is_correct": False},
                ],
            },
            {
                "text": "I ______ playing computer games in my free time.",
                "order": 16,
                "choices": [
                    {"text": "like", "is_correct": True},
                    {"text": "likes", "is_correct": False},
                    {"text": "liking", "is_correct": False},
                    {"text": "liked", "is_correct": False},
                ],
            },
            {
                "text": "I ______ winter.",
                "order": 17,
                "choices": [
                    {"text": "like", "is_correct": True},
                    {"text": "likes", "is_correct": False},
                    {"text": "liking", "is_correct": False},
                    {"text": "liked", "is_correct": False},
                ],
            },
            {
                "text": "Her daughters don't _______ to school.",
                "order": 18,
                "choices": [
                    {"text": "go", "is_correct": True},
                    {"text": "goes", "is_correct": False},
                    {"text": "going", "is_correct": False},
                    {"text": "gone", "is_correct": False},
                ],
            },
            {
                "text": "My father _____ an honest man. He _______ lies.",
                "order": 19,
                "choices": [
                    {"text": "is / never tells", "is_correct": True},
                    {"text": "is / always tells", "is_correct": False},
                    {"text": "are / never tells", "is_correct": False},
                    {"text": "is / never tell", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 11 ───────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 11",
        "description": "English language test questions - Variant 11",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "What _____ your mother _____? — She is a doctor.",
                "order": 0,
                "choices": [
                    {"text": "does / do", "is_correct": True},
                    {"text": "do / do", "is_correct": False},
                    {"text": "does / does", "is_correct": False},
                    {"text": "is / do", "is_correct": False},
                ],
            },
            {
                "text": "We … our teacher a question about the test.",
                "order": 1,
                "choices": [
                    {"text": "asked", "is_correct": True},
                    {"text": "ask", "is_correct": False},
                    {"text": "asks", "is_correct": False},
                    {"text": "asking", "is_correct": False},
                ],
            },
            {
                "text": "Last summer I ___ to Paris.",
                "order": 2,
                "choices": [
                    {"text": "went", "is_correct": True},
                    {"text": "go", "is_correct": False},
                    {"text": "goes", "is_correct": False},
                    {"text": "gone", "is_correct": False},
                ],
            },
            {
                "text": "She ___ a beautiful city last year.",
                "order": 3,
                "choices": [
                    {"text": "visited", "is_correct": True},
                    {"text": "visit", "is_correct": False},
                    {"text": "visits", "is_correct": False},
                    {"text": "visiting", "is_correct": False},
                ],
            },
            {
                "text": "We ___ a museum yesterday.",
                "order": 4,
                "choices": [
                    {"text": "visited", "is_correct": True},
                    {"text": "visit", "is_correct": False},
                    {"text": "visits", "is_correct": False},
                    {"text": "visiting", "is_correct": False},
                ],
            },
            {
                "text": "They ___ their grandparents last weekend.",
                "order": 5,
                "choices": [
                    {"text": "visited", "is_correct": True},
                    {"text": "visit", "is_correct": False},
                    {"text": "visits", "is_correct": False},
                    {"text": "visiting", "is_correct": False},
                ],
            },
            {
                "text": "I ___ many photos during my trip.",
                "order": 6,
                "choices": [
                    {"text": "took", "is_correct": True},
                    {"text": "take", "is_correct": False},
                    {"text": "takes", "is_correct": False},
                    {"text": "taking", "is_correct": False},
                ],
            },
            {
                "text": "I ___ my homework yesterday.",
                "order": 7,
                "choices": [
                    {"text": "did", "is_correct": True},
                    {"text": "do", "is_correct": False},
                    {"text": "does", "is_correct": False},
                    {"text": "doing", "is_correct": False},
                ],
            },
            {
                "text": "She ___ a letter to her friend last night.",
                "order": 8,
                "choices": [
                    {"text": "wrote", "is_correct": True},
                    {"text": "write", "is_correct": False},
                    {"text": "writes", "is_correct": False},
                    {"text": "writing", "is_correct": False},
                ],
            },
            {
                "text": "We ___ in the park last Sunday.",
                "order": 9,
                "choices": [
                    {"text": "played", "is_correct": True},
                    {"text": "play", "is_correct": False},
                    {"text": "plays", "is_correct": False},
                    {"text": "playing", "is_correct": False},
                ],
            },
            {
                "text": "They ___ a cake for the party.",
                "order": 10,
                "choices": [
                    {"text": "made", "is_correct": True},
                    {"text": "make", "is_correct": False},
                    {"text": "makes", "is_correct": False},
                    {"text": "making", "is_correct": False},
                ],
            },
            {
                "text": "He ___ to music in the evening.",
                "order": 11,
                "choices": [
                    {"text": "listened", "is_correct": True},
                    {"text": "listen", "is_correct": False},
                    {"text": "listens", "is_correct": False},
                    {"text": "listening", "is_correct": False},
                ],
            },
            {
                "text": "Gulnoza ..… go to work yesterday but she was sick.",
                "order": 12,
                "choices": [
                    {"text": "didn't", "is_correct": True},
                    {"text": "don't", "is_correct": False},
                    {"text": "doesn't", "is_correct": False},
                    {"text": "wasn't", "is_correct": False},
                ],
            },
            {
                "text": "They … to the park because they were very tired.",
                "order": 13,
                "choices": [
                    {"text": "didn't go", "is_correct": True},
                    {"text": "don't go", "is_correct": False},
                    {"text": "doesn't go", "is_correct": False},
                    {"text": "not went", "is_correct": False},
                ],
            },
            {
                "text": "Did you talk to your boss? — Yes, I ….",
                "order": 14,
                "choices": [
                    {"text": "did", "is_correct": True},
                    {"text": "do", "is_correct": False},
                    {"text": "does", "is_correct": False},
                    {"text": "was", "is_correct": False},
                ],
            },
            {
                "text": "I … twenty minutes for the bus yesterday.",
                "order": 15,
                "choices": [
                    {"text": "waited", "is_correct": True},
                    {"text": "wait", "is_correct": False},
                    {"text": "waits", "is_correct": False},
                    {"text": "waiting", "is_correct": False},
                ],
            },
            {
                "text": "… they fix their bicycles? — Yes, they ….",
                "order": 16,
                "choices": [
                    {"text": "Did / did", "is_correct": True},
                    {"text": "Do / do", "is_correct": False},
                    {"text": "Does / does", "is_correct": False},
                    {"text": "Were / were", "is_correct": False},
                ],
            },
            {
                "text": "Where … you go to school when you were young?",
                "order": 17,
                "choices": [
                    {"text": "did", "is_correct": True},
                    {"text": "do", "is_correct": False},
                    {"text": "does", "is_correct": False},
                    {"text": "were", "is_correct": False},
                ],
            },
            {
                "text": "We … go camping in a park when we were children.",
                "order": 18,
                "choices": [
                    {"text": "used to", "is_correct": True},
                    {"text": "use to", "is_correct": False},
                    {"text": "uses to", "is_correct": False},
                    {"text": "using to", "is_correct": False},
                ],
            },
            {
                "text": "I … dinner last night, so I couldn't watch TV.",
                "order": 19,
                "choices": [
                    {"text": "cooked", "is_correct": True},
                    {"text": "cook", "is_correct": False},
                    {"text": "cooks", "is_correct": False},
                    {"text": "cooking", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 12 ───────────────────────────────────────────────────────────
    {
        "title": "English Test - Variant 12",
        "description": "English language test questions - Variant 12",
        "duration_minutes": 20,
        "questions": [
            {
                "text": "Did you … the book? — No, I ….",
                "order": 0,
                "choices": [
                    {"text": "read / didn't", "is_correct": True},
                    {"text": "read / don't", "is_correct": False},
                    {"text": "read / doesn't", "is_correct": False},
                    {"text": "reads / didn't", "is_correct": False},
                ],
            },
            {
                "text": "Why … you wash the dirty dishes last week?",
                "order": 1,
                "choices": [
                    {"text": "didn't", "is_correct": True},
                    {"text": "don't", "is_correct": False},
                    {"text": "doesn't", "is_correct": False},
                    {"text": "weren't", "is_correct": False},
                ],
            },
            {
                "text": "My friend Munisa … see a dentist yesterday.",
                "order": 2,
                "choices": [
                    {"text": "had to", "is_correct": True},
                    {"text": "has to", "is_correct": False},
                    {"text": "have to", "is_correct": False},
                    {"text": "must", "is_correct": False},
                ],
            },
            {
                "text": "I … at work very late last night.",
                "order": 3,
                "choices": [
                    {"text": "was", "is_correct": True},
                    {"text": "is", "is_correct": False},
                    {"text": "am", "is_correct": False},
                    {"text": "were", "is_correct": False},
                ],
            },
            {
                "text": "Zuhra … for help when he fell in the water.",
                "order": 4,
                "choices": [
                    {"text": "called", "is_correct": True},
                    {"text": "call", "is_correct": False},
                    {"text": "calls", "is_correct": False},
                    {"text": "calling", "is_correct": False},
                ],
            },
            {
                "text": "She didn't answer because she … hear it ring.",
                "order": 5,
                "choices": [
                    {"text": "couldn't", "is_correct": True},
                    {"text": "can't", "is_correct": False},
                    {"text": "wasn't", "is_correct": False},
                    {"text": "didn't", "is_correct": False},
                ],
            },
            {
                "text": "I ... tennis yesterday because I don't know how.",
                "order": 6,
                "choices": [
                    {"text": "didn't play", "is_correct": True},
                    {"text": "don't play", "is_correct": False},
                    {"text": "doesn't play", "is_correct": False},
                    {"text": "wasn't playing", "is_correct": False},
                ],
            },
            {
                "text": "Mozart ___________ more than 600 pieces of music.",
                "order": 7,
                "choices": [
                    {"text": "wrote", "is_correct": True},
                    {"text": "write", "is_correct": False},
                    {"text": "writes", "is_correct": False},
                    {"text": "writing", "is_correct": False},
                ],
            },
            {
                "text": "We _______ our classmate in town a few days ago.",
                "order": 8,
                "choices": [
                    {"text": "saw", "is_correct": True},
                    {"text": "see", "is_correct": False},
                    {"text": "sees", "is_correct": False},
                    {"text": "seeing", "is_correct": False},
                ],
            },
            {
                "text": "It was cold, so I _____________ the window.",
                "order": 9,
                "choices": [
                    {"text": "closed", "is_correct": True},
                    {"text": "close", "is_correct": False},
                    {"text": "closes", "is_correct": False},
                    {"text": "closing", "is_correct": False},
                ],
            },
            {
                "text": "I ___________ to the cinema three times last week.",
                "order": 10,
                "choices": [
                    {"text": "went", "is_correct": True},
                    {"text": "go", "is_correct": False},
                    {"text": "goes", "is_correct": False},
                    {"text": "going", "is_correct": False},
                ],
            },
            {
                "text": "Which sentence is in the past simple tense?",
                "order": 11,
                "choices": [
                    {"text": "I played football yesterday", "is_correct": True},
                    {"text": "I play football", "is_correct": False},
                    {"text": "I am playing football", "is_correct": False},
                    {"text": "I will play football", "is_correct": False},
                ],
            },
            {
                "text": "How do you form the past simple of regular verbs?",
                "order": 12,
                "choices": [
                    {"text": "add -ed", "is_correct": True},
                    {"text": "add -ing", "is_correct": False},
                    {"text": "add -s", "is_correct": False},
                    {"text": "add -er", "is_correct": False},
                ],
            },
            {
                "text": "The correct past simple form of go?",
                "order": 13,
                "choices": [
                    {"text": "went", "is_correct": True},
                    {"text": "goed", "is_correct": False},
                    {"text": "gone", "is_correct": False},
                    {"text": "going", "is_correct": False},
                ],
            },
            {
                "text": "Negative sentence in past simple?",
                "order": 14,
                "choices": [
                    {"text": "I didn't go", "is_correct": True},
                    {"text": "I don't go", "is_correct": False},
                    {"text": "I not go", "is_correct": False},
                    {"text": "I wasn't go", "is_correct": False},
                ],
            },
            {
                "text": "Past simple form of eat?",
                "order": 15,
                "choices": [
                    {"text": "ate", "is_correct": True},
                    {"text": "eated", "is_correct": False},
                    {"text": "eaten", "is_correct": False},
                    {"text": "eating", "is_correct": False},
                ],
            },
            {
                "text": "Question in the past simple tense?",
                "order": 16,
                "choices": [
                    {"text": "Did you see that?", "is_correct": True},
                    {"text": "Do you see that?", "is_correct": False},
                    {"text": "Are you seeing that?", "is_correct": False},
                    {"text": "Have you seen that?", "is_correct": False},
                ],
            },
            {
                "text": "Dilobar _____ when she _____ the DVDs.",
                "order": 17,
                "choices": [
                    {"text": "was shopping / found", "is_correct": True},
                    {"text": "shopped / found", "is_correct": False},
                    {"text": "was shopping / was finding", "is_correct": False},
                    {"text": "shopped / was finding", "is_correct": False},
                ],
            },
            {
                "text": "While Aziz _____ a documentary, he _____ asleep.",
                "order": 18,
                "choices": [
                    {"text": "was watching / fell", "is_correct": True},
                    {"text": "watched / fell", "is_correct": False},
                    {"text": "was watching / was falling", "is_correct": False},
                    {"text": "watched / was falling", "is_correct": False},
                ],
            },
            {
                "text": "They _____ when you _____ for remote control.",
                "order": 19,
                "choices": [
                    {"text": "were sleeping / looked", "is_correct": True},
                    {"text": "slept / looked", "is_correct": False},
                    {"text": "were sleeping / were looking", "is_correct": False},
                    {"text": "slept / were looking", "is_correct": False},
                ],
            },
        ],
    },
    # ─── Variant 13 (10 questions) ────────────────────────────────────────────
    {
        "title": "English Test - Variant 13",
        "description": "English language test questions - Variant 13",
        "duration_minutes": 15,
        "questions": [
            {
                "text": "What ________? — I was watching TV.",
                "order": 0,
                "choices": [
                    {"text": "were you doing", "is_correct": True},
                    {"text": "are you doing", "is_correct": False},
                    {"text": "did you do", "is_correct": False},
                    {"text": "do you do", "is_correct": False},
                ],
            },
            {
                "text": "My mother was cooking dinner at 8 p.m. ___.",
                "order": 1,
                "choices": [
                    {"text": "yesterday", "is_correct": True},
                    {"text": "tomorrow", "is_correct": False},
                    {"text": "today", "is_correct": False},
                    {"text": "now", "is_correct": False},
                ],
            },
            {
                "text": "My son ..... ..... television when the lights went out.",
                "order": 2,
                "choices": [
                    {"text": "was watching", "is_correct": True},
                    {"text": "watched", "is_correct": False},
                    {"text": "is watching", "is_correct": False},
                    {"text": "watches", "is_correct": False},
                ],
            },
            {
                "text": "What _____ you _____ when it started hailing?",
                "order": 3,
                "choices": [
                    {"text": "were / doing", "is_correct": True},
                    {"text": "are / doing", "is_correct": False},
                    {"text": "did / do", "is_correct": False},
                    {"text": "was / doing", "is_correct": False},
                ],
            },
            {
                "text": "While the soup was boiling, my brother .... .... sweets.",
                "order": 4,
                "choices": [
                    {"text": "was eating", "is_correct": True},
                    {"text": "ate", "is_correct": False},
                    {"text": "is eating", "is_correct": False},
                    {"text": "eats", "is_correct": False},
                ],
            },
            {
                "text": "Our enemies _____ me when I was lost in the forest.",
                "order": 5,
                "choices": [
                    {"text": "were following", "is_correct": True},
                    {"text": "followed", "is_correct": False},
                    {"text": "are following", "is_correct": False},
                    {"text": "follow", "is_correct": False},
                ],
            },
            {
                "text": "Sardor _____ off the ladder while he _____ the ceiling.",
                "order": 6,
                "choices": [
                    {"text": "fell / was painting", "is_correct": True},
                    {"text": "was falling / painted", "is_correct": False},
                    {"text": "fell / painted", "is_correct": False},
                    {"text": "was falling / was painting", "is_correct": False},
                ],
            },
            {
                "text": "I _____ grammar when I _____ asleep.",
                "order": 7,
                "choices": [
                    {"text": "was studying / fell", "is_correct": True},
                    {"text": "studied / fell", "is_correct": False},
                    {"text": "was studying / was falling", "is_correct": False},
                    {"text": "studied / was falling", "is_correct": False},
                ],
            },
            {
                "text": "The scientists _____ in their lab when they _____ the new drug.",
                "order": 8,
                "choices": [
                    {"text": "were working / discovered", "is_correct": True},
                    {"text": "worked / discovered", "is_correct": False},
                    {"text": "were working / were discovering", "is_correct": False},
                    {"text": "worked / were discovering", "is_correct": False},
                ],
            },
            {
                "text": "My brother _____ on the phone when I ________.",
                "order": 9,
                "choices": [
                    {"text": "was talking / arrived", "is_correct": True},
                    {"text": "talked / arrived", "is_correct": False},
                    {"text": "was talking / was arriving", "is_correct": False},
                    {"text": "talked / was arriving", "is_correct": False},
                ],
            },
        ],
    },
]


async def login(username: str, password: str, client: httpx.AsyncClient) -> str:
    r = await client.post(f"{BASE}/auth/login", json={"username": username, "password": password})
    r.raise_for_status()
    return r.json()["access_token"]


async def create_quiz(quiz: dict, token: str, client: httpx.AsyncClient) -> str:
    r = await client.post(
        f"{BASE}/quizzes",
        json=quiz,
        headers={"Authorization": f"Bearer {token}"},
    )
    if r.status_code == 201:
        data = r.json()
        q_count = len(data.get("questions", []))
        return f"✓ '{quiz['title']}' created ({q_count} questions)"
    return f"✗ '{quiz['title']}' failed: {r.text}"


async def main():
    async with httpx.AsyncClient(timeout=60) as client:
        print("Logging in as Asliddin...")
        token = await login("Asliddin", "1234567", client)
        print("✓ Token received\n")

        total_quizzes = len(ENGLISH_QUIZZES)
        total_questions = sum(len(q["questions"]) for q in ENGLISH_QUIZZES)
        print(f"Adding {total_quizzes} variants with {total_questions} questions total...\n")

        for quiz in ENGLISH_QUIZZES:
            result = await create_quiz(quiz, token, client)
            print(result)

        print(f"\nDone! {total_quizzes} English test variants added.")


asyncio.run(main())
