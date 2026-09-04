from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = ""

class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    progress: float
    model_config = {"from_attributes": True}

class MaterialOut(BaseModel):
    id: int
    course_id: int
    title: str
    original_filename: str
    mime_type: str
    status: str
    chunk_count: int
    error_message: str | None
    model_config = {"from_attributes": True}
