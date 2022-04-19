import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    token = os.environ.get("BOT_TOKEN")
    db_host = os.environ.get("HOST")

