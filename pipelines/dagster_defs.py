import os
import glob
import pandas as pd
from dagster import asset, Definitions, job
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Program

DATA_DIR = "data/"
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@postgres:5432/carms"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


@asset
def raw_program_data() -> pd.DataFrame:
    """Load all CSV files into a single DataFrame."""
    all_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    dfs = [pd.read_csv(f) for f in all_files]
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


@asset
def cleaned_program_data(raw_program_data: pd.DataFrame) -> pd.DataFrame:
    if raw_program_data.empty:
        return raw_program_data

    columns_to_keep = ["program_name", "document_id", "source"]
    df = raw_program_data[columns_to_keep].drop_duplicates()

    # Convert document_id to string and remove dashes
    df["document_id"] = df["document_id"].astype(str).str.replace("-", "", regex=False).astype(int)

    return df


@asset
def programs_table(cleaned_program_data: pd.DataFrame):
    """Insert cleaned data into Postgres."""
    if cleaned_program_data.empty:
        return

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        for _, row in cleaned_program_data.iterrows():
            program = Program(
                document_id=row.document_id,
                program_name=row.program_name,
                source=row.source,
            )
            session.merge(program)  # idempotent insert/update

        session.commit()

    return f"Inserted {len(cleaned_program_data)} records."

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