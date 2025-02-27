from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    Task: str

    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    id: int
    Task: str

    model_config = ConfigDict(from_attributes=True)