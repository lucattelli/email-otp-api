import os
import dotenv

settings = {
    'GMAIL_USER': os.getenv('GMAIL_USER', ''),
    'GMAIL_PASSWORD': os.getenv('GMAIL_PASSWORD', ''),
    'GMAIL_URL': os.getenv('GMAIL_URL', ''),
    'GMAIL_PORT': os.getenv('GMAIL_PORT', ''),
}


def load_settings():
    dotenv.load_dotenv(dotenv_path='src/.env', verbose=True)
    settings['GMAIL_USER'] = os.getenv('GMAIL_USER', '')
    settings['GMAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD', '')
    settings['GMAIL_URL'] = os.getenv('GMAIL_URL', '')
    settings['GMAIL_PORT'] = os.getenv('GMAIL_PORT', '')


load_settings()
