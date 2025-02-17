import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))
load_dotenv(os.path.join(BASE_DIR, ".env"))
print("BASE_DIR:", BASE_DIR)

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

        self.MONGO_URL_CONNECT = os.getenv("MONGO_URL_CONNECT", "")
        self.MONGO_HOST = os.getenv("MONGO_HOST", "")
        self.MONGO_PORT = os.getenv("MONGO_PORT", "")
        self.MONGO_USER = os.getenv("MONGO_USER", "")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
        self.MONGO_DATABASE = os.getenv("MONGO_DATABASE", "")

settings = Settings()
