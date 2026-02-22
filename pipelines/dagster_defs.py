import os
import glob
import pandas as pd
from dagster import asset, Definitions, job
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Program
from pipelines.utils import extract_provinces

DATA_DIR = "data/"
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@postgres:5432/carms"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

#embeddings for LLM search
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

@asset
def raw_program_data() -> pd.DataFrame:
    """
    Load all CSV files into a single DataFrame.
    
    Concatenates all files in the directory 
    (Though our example only has one file!)
    """

    all_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    dfs = [pd.read_csv(f) for f in all_files]
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


@asset
def cleaned_program_data(raw_program_data: pd.DataFrame) -> pd.DataFrame:
    if raw_program_data.empty:
        return raw_program_data

    #for this simple example I will only keep a few columns
    columns_to_keep = ["program_name", "document_id", "source"]
    df = raw_program_data[columns_to_keep].drop_duplicates()

    # document_id is in the form XXXX-YYYY
    # We will load as a string and remove the dash so we can use int XXXXYYYY as the ID
    df["document_id"] = df["document_id"].astype(str).str.replace("-", "", regex=False).astype(int)

    # Iterate over all the match_iteration_name entries to find the names of 
    # any provinces and territories mentioned 
    # (TODO: there will be faster ways to do this, but fine for small example)
    df["province_or_territory"] = [extract_provinces(x) for x in raw_program_data["match_iteration_name"]]
    print('province_or_territory added')

    #build the embedding from some of the string type columns
    strings = (
        raw_program_data["program_name"] + 
        raw_program_data["match_iteration_name"] + 
        raw_program_data["program_contracts"] + 
        raw_program_data["general_instructions"] + 
        raw_program_data["supporting_documentation_information"]
    ).astype(str).tolist()# convert Series to list of strings

    vectors = embeddings.embed_documents(strings)     # batch embedding
    df["vector"] = vectors

    return df


@asset
def programs_table(cleaned_program_data: pd.DataFrame):
    """Insert cleaned data into Postgres."""
    if cleaned_program_data.empty:
        return

    #This should ensure all the correct tables are in place before trying to add anything
    #Base is from SQLAlchemy and all the tables in app/models should be linked to it
    Base.metadata.create_all(engine)

    #starts the database session
    with SessionLocal() as session:
        #add the data one row at a time
        for _, row in cleaned_program_data.iterrows():
            program = Program(
                document_id=row.document_id,
                program_name=row.program_name,
                source=row.source,
                province_or_territory=row.province_or_territory,
                vector=row.vector,
            )
            
            # if a program with this ID already exists this updated the entry
            # if not it adds it
            session.merge(program)  # idempotent insert/update

        #execute the database construction
        session.commit()

    return f"Inserted {len(cleaned_program_data)} records."

# We always want this to run once at build. Dagster can then be used to re-run or schedule runs
@job
def materialize_all_assets():
    programs_table(cleaned_program_data(raw_program_data()))

defs = Definitions(
    assets=[
        raw_program_data,
        cleaned_program_data,
        programs_table,
    ],
    jobs=[
        materialize_all_assets,
    ]
)