import pymysql
from urllib.parse import quote_plus
from module_connect.config_conn import settings

def connect_mysql():
    conn = pymysql.connect(
        host=settings.MYSQL_HOTS,
        port=int(settings.MYSQL_PORT),
        user=settings.MYSQL_USER,
        password=settings.MYSQL_KEY,
        database=settings.MYSQL_DB,
    )
    return conn
