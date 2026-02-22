from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

# This is one table in our database 
# we can make more tables my making new classes in this file that inherit from Base
class Program(Base):
    __tablename__ = "programs"

    document_id = Column(Integer, primary_key=True, index=True)
    program_name = Column(Text)
    source = Column(Text)
    province_or_territory = Column(Text)
    vector = Column(Vector(1536)) #embedding for the LLM search