from pydantic import BaseModel


class ChoiceCreate(BaseModel):
    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    text: str
    order: int = 0
    choices: list[ChoiceCreate]


class QuizCreate(BaseModel):
    title: str
    description: str | None = None
    duration_minutes: int = 10
    questions: list[QuestionCreate]


class ChoicePublicResponse(BaseModel):
    id: int
    text: str

    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    id: int
    text: str
    order: int
    choices: list[ChoicePublicResponse]

    model_config = {"from_attributes": True}


class QuizResponse(BaseModel):
    id: int
    title: str
    description: str | None
    duration_minutes: int
    is_active: bool
    question_count: int = 0

    model_config = {"from_attributes": True}


class QuizDetailResponse(BaseModel):
    id: int
    title: str
    description: str | None
    duration_minutes: int
    is_active: bool
    questions: list[QuestionResponse]

    model_config = {"from_attributes": True}


class AnswerSubmit(BaseModel):
    question_id: int
    choice_id: int | None = None


class SessionStartResponse(BaseModel):
    session_id: int
    quiz_id: int
    duration_minutes: int
