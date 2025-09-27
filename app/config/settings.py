import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    BITHUMB_API_KEY = os.getenv("BITHUMB_API_KEY")
    BITHUMB_SECRET_KEY = os.getenv("BITHUMB_SECRET_KEY")

settings = Settings()
