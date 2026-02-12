# pipelines/ingest_data.py
import os
import glob
import pandas as pd
from sqlalchemy import create_engine, text

# Constants
DATA_DIR = "data/"  # where the csv scraped file(s) live
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/carms")


def load_csv_files(directory=DATA_DIR):
    """
    Load any CSV files in a directory into pandas DataFrames
    and concatenate them into a single DataFrame.

    In practice we only have one file in this example,
    but we allow for more to allow scalability
    """
    all_files = glob.glob(os.path.join(directory, "*.csv"))
    dfs = []
    for f in all_files:
        df = pd.read_csv(f)
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()


def preprocess_programs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal processing: just select a few key columns.
    """
    if df.empty:
        return df
    columns_to_keep = ["program_name", "document_id", "source"]
    return df[columns_to_keep].drop_duplicates()


def insert_into_db(df: pd.DataFrame, db_url=DB_URL):
    """
    Insert the processed DataFrame into PostgreSQL.
    Creates the table if it does not exist.
    """
    engine = create_engine(db_url)

    # Use SQLAlchemy text to execute a simple CREATE TABLE if not exists
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS programs (
        document_id INT PRIMARY KEY,
        program_name TEXT,
        source TEXT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()

    # Insert data
    df.to_sql("programs", engine, if_exists="replace", index=False)
    print(f"Inserted {len(df)} records into 'programs' table.")


def main():
    df_raw = load_csv_files()
    df_clean = preprocess_programs(df_raw)
    if df_clean.empty:
        print("No data to load!")
        return
    insert_into_db(df_clean)


if __name__ == "__main__":
    main()