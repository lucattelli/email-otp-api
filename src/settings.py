import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', verbose=True)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
GMAIL_URL = os.getenv("GMAIL_URL")
GMAIL_PORT = os.getenv("GMAIL_PORT")
