import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))
# print(BASE_DIR)

# Load environment variables from the .env file (if present)
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Settings:
    def __init__(self, **kwargs):
        self.URL_CONNECT = os.getenv("URL_CONNECT", "")
        self.PASSWORD = os.getenv("PASSWORD", "")
        self.HOST = os.getenv("HOST", "")
        self.PORT = os.getenv("PORT", "")
        self.MYUSER = os.getenv("MYUSER", "")
        self.DATABASE = os.getenv("DATABASE", "")

        self.MYSQL_URL_CONNECT = os.getenv("MYSQL_URL_CONNECT", "")
        self.MYSQL_HOST = os.getenv("MYSQL_HOST", "")
        self.MYSQL_PORT = os.getenv("MYSQL_PORT", "")
        self.MYSQL_USER = os.getenv("MYSQL_USER", "")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")


settings = Settings()
