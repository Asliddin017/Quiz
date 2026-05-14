from datetime import datetime

from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: int
    session_id: int
    quiz_id: int
    score: int
    total_questions: int
    correct_answers: int
    percentage: float
    created_at: datetime
    quiz_title: str = ""

    model_config = {"from_attributes": True}
