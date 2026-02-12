from sqlalchemy.orm import Session
from .models import Program

def get_programs(db: Session, limit: int = 100):
    return db.query(Program).limit(limit).all()