import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv("OAUTHLIB_INSECURE_TRANSPORT", "0")

class FileConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    DISHES_FILE = DATA_DIR / "dishes.csv"
    INGREDIENTS_FILE = DATA_DIR / "ingredients.csv"
    DIETARY_FILE = DATA_DIR / "dietary.csv"
    COUNTRY_FILE = DATA_DIR / "country.csv"
    NUTRIENTS_FILE = DATA_DIR / "nutrients.csv"