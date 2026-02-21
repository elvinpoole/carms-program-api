from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# This is one table in our database 
# we can make more tables my making new classes in this file that inherit from Base
class Program(Base):
    __tablename__ = "programs"

    document_id = Column(Integer, primary_key=True, index=True)
    program_name = Column(Text)
    source = Column(Text)