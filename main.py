import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Delivery, Locker, Package, User
from schemas import (
    UserResponse,
    LockerResponse,
    LockerUpdate,
    PackageResponse,
    DeliveryResponse,
)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thu hẹp lại trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Smart Locker API is running"}


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/lockers", response_model=list[LockerResponse])
def get_lockers(db: Session = Depends(get_db)):
    return db.query(Locker).all()


@app.get("/packages", response_model=list[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()


@app.get("/deliveries", response_model=list[DeliveryResponse])
def get_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all()


@app.get("/lockers/{locker_id}", response_model=LockerResponse)
def get_locker(locker_id: int, db: Session = Depends(get_db)):
    locker = db.query(Locker).filter(Locker.locker_id == locker_id).first()
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    return locker


@app.put("/lockers/{locker_id}", response_model=LockerResponse)
def update_locker(
    locker_id: int,
    data: LockerUpdate,
    db: Session = Depends(get_db),
):
    locker = db.query(Locker).filter(Locker.locker_id == locker_id).first()

    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")

    locker.status = data.status

    db.commit()
    db.refresh(locker)

    return locker


# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

@app.get("/web")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)