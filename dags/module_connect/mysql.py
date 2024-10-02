import pymysql
from urllib.parse import quote_plus
from module_connect.config_conn import settings

def connect_mysql():
    conn = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=int(settings.MYSQL_PORT),
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
    )
    return conn

def mysql_engine():
    return settings.MYSQL_URL_CONNECT.format(
        user=settings.MYSQL_USER,
        password=quote_plus(settings.MYSQL_PASSWORD), # for special characters
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DATABASE
    )
