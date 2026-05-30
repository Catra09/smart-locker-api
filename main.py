from fastapi import FastAPI 
from database import engine, Base 
import models 
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Delivery, Locker, Package, User
from schemas import UserResponse


# Create the database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()
def get_db():
    db = Session(bind=engine.connect())
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def home():
    return {"message": "Smart Locker API is running"}

@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all() 

@app.get("/lockers")
def get_lockers(db: Session = Depends(get_db)):
    return db.query(Locker).all() 

@app.get("/packages") 
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()

@app.get("/deliveries")
def get_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all() 

@app.get("/lockers/{locker_id}")
def get_locker(locker_id: int, db: Session = Depends(get_db)):
    return db.query(Locker).filter(
        Locker.locker_id == locker_id
    ).first() 
    
@app.put("/lockers/{locker_id}")
def update_locker(
    locker_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    locker = db.query(Locker).filter(
        Locker.locker_id == locker_id
    ).first()

    if not locker:
        return {"error": "Locker not found"}

    locker.status = status

    db.commit()
    db.refresh(locker)

    return locker 

