from pydantic import BaseModel

class FlashcardOut(BaseModel):
    id: int
    question: str
    answer: str
    box: int
    model_config = {"from_attributes": True}

class FlashcardReview(BaseModel):
    known: bool

class QuizQuestionOut(BaseModel):
    id: int
    question: str
    options: list[str]

class QuizOut(BaseModel):
    id: int
    title: str
    questions: list[QuizQuestionOut]

class QuizSubmit(BaseModel):
    answers: dict[int, int]

class QuizResult(BaseModel):
    score: int
    total: int
    xp_awarded: int
    explanations: list[str]

class BadgeOut(BaseModel):
    code: str
    name: str
    description: str
    icon: str

class ProgressOut(BaseModel):
    xp: int
    level: int
    level_progress: float
    streak: int
    next_level_xp: int
    badges: list[BadgeOut]
