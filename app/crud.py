# Create, Read, Update, Delete
from sqlalchemy.orm import Session
from .models import Program

#embeddings for LLM search
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

def get_programs(db: Session, limit: int = 100):
    return db.query(Program).limit(limit).all()

def filter_programs_by_province(db: Session, input: str="", limit: int = 100):
    """
    Return all Program entries whose province_or_territory column
    contains the given input string
    input strings should be the canonical names used in pipeline/utils
    """
    if input=="":
        #return all provinces
        return db.query(Program).limit(limit).all()

    return ( 
        db.query(Program)
        .filter(Program.province_or_territory.ilike(f"%{input}%")) #ilike does case-insensitive matching
        .limit(limit)
        .all()
        )

def semantic_search(db: Session, prompt: str, limit: int = 5):
    query_embedding = embeddings.embed_query(prompt)

    return (
        db.query(Program)
        .order_by(Program.vector.l2_distance(query_embedding)) #return the closed 
        .limit(limit)
        .all()
    )