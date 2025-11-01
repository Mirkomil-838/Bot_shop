import os
from dotenv import load_dotenv

# .env fayldan o‘qish
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
