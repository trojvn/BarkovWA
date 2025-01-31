import os

from dotenv import load_dotenv

load_dotenv("настройки.txt")

SLEEP_END = int(os.getenv("SLEEP_END", "15"))
USER = os.getenv("USER", "trojvn")
HIDE = os.getenv("HIDE")
DATE = os.getenv("DATE")
