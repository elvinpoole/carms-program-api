from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import get_programs
from .models import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CaRMS Programs API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the CaRMS Programs API. Use /programs to see data."}

@app.get("/programs")
def read_programs(limit: int = 100, db: Session = Depends(get_db)):
    programs = get_programs(db, limit)
    return [{"document_id": p.document_id, "program_name": p.program_name, "source": p.source} for p in programs]