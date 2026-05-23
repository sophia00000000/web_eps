from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "dev-eps-secret-key"
    DATABASE = BASE_DIR / "eps.sqlite3"