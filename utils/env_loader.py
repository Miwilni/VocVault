# utils/env_loader.py
import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    return {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_NAME": os.getenv("DB")
    }
