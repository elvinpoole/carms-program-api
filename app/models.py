from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Program(Base):
    __tablename__ = "programs"

    document_id = Column(Integer, primary_key=True, index=True)
    program_name = Column(Text)
    source = Column(Text)