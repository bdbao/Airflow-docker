from urllib.parse import quote_plus
from module_connect.config_conn import settings

def postgres_engine():
    return settings.URL_CONNECT.format(
        user=settings.MYUSER,
        password=quote_plus(settings.PASSWORD), # for special characters
        host=settings.HOST,
        port=settings.PORT,
        database=settings.DATABASE
    )
