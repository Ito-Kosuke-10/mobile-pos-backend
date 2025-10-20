import os
from dotenv import load_dotenv

load_dotenv()

# データベースURLの設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pos_app.db")

# CORS設定
CORS_ORIGINS = ["http://localhost:3000"]
