from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import psycopg2

DATABASE_URL = "postgresql://postgres:3891123@my_db:5432/my_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI(debug=True)

class User(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Task = Column(String, nullable=False)
Base.metadata.create_all(engine)

class UserCreate(BaseModel):
    Task: str

class UserResponse(BaseModel):
    id: int
    Task: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_new_user(db: Session, user_data: UserCreate):
    new_user = User(
        Task=user_data.Task,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.Task = user_data.Task
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()
    db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "Все задачи успешно удалены"}

@app.post("/tasks/create_task", response_model=UserResponse)
def create_user_route(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(db=db, user_data=user_data)

@app.get("/tasks/get_all_tasks", response_model=list[UserResponse])
def get_users_route(db: Session = Depends(get_db)):
    return get_users(db=db)

@app.get("/tasks/get_task_by_id", response_model=UserResponse)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.put("/tasks/update_task_by_id", response_model=UserResponse)
def update_user_route(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db=db, user_id=user_id, user_data=user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user

@app.delete("/tasks/delete_task_by_id", response_model=UserResponse)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return deleted_user

@app.delete("/users/delete_all_tasks", response_model=dict)
def delete_all_users_route(db: Session = Depends(get_db)):
    return delete_all_users(db=db)