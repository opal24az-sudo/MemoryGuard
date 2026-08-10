# config.py
#קובץ הגדרות

import os
from dotenv import load_dotenv

# load_dotenv() = "קרא את קובץ .env וטען את כל המשתנים"
load_dotenv()

# קבל את ה-API key מ-.env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# הגדרות נוספות
MODEL_NAME = "gpt-3.5-turbo"
MAX_MEMORY_SIZE = 10  # שמור את ה-10 תורים האחרונים בזיכרון