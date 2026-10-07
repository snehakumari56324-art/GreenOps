import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# ----------------------------------------
# PATHS
# ----------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "data" / "public_greenops_data.csv"

ENV_FILE = PROJECT_ROOT / "backend" / ".env"

# ----------------------------------------
# LOAD DATABASE SETTINGS
# ----------------------------------------

load_dotenv(ENV_FILE)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME
]):
    raise Exception(
        "Database configuration missing in backend/.env"
    )

# ----------------------------------------
# DATABASE CONNECTION
# ----------------------------------------

password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ----------------------------------------
# READ PUBLIC DATASET
# ----------------------------------------

print("Reading public dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Records found: {len(df)}")

# ----------------------------------------
# IMPORT TO MYSQL
# ----------------------------------------

print("Importing data into MySQL...")

df.to_sql(
    "cloud_resources",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("----------------------------------------")
print("IMPORT SUCCESSFUL")
print("----------------------------------------")
print(f"Records imported: {len(df)}")
print("Table: cloud_resources")
print("----------------------------------------")