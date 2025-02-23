from pydantic import BaseModel

class TaskCreate(BaseModel):
    Task: str

class TaskResponse(BaseModel):
    id: int
    Task: str

    class Config:
        from_attributes = True