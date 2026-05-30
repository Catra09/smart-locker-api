from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    student_id: str
    full_name: str
    email: str

    class Config:
        from_attributes = True