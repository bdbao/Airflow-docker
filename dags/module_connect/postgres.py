# import psycopg2
from urllib.parse import quote_plus
from module_connect.config_conn import settings

# def connect_postgres():
#     conn = psycopg2.connect(
#         host="192.168.1.188",
#         port="5432",
#         user="postgres",
#         password="admin#1234",
#         database="sales",
#     )
#     return conn


def postgres_engine():
    return settings.URL_CONNECT % quote_plus(settings.KEY)
