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
    # return settings.URL_CONNECT.format(
    #     user=settings.USER,
    #     password=quote_plus(settings.PASSWORD), # for special characters
    #     host=settings.HOST,
    #     port=settings.PORT,
    #     database=settings.DATABASE
    # )
    print("Entering postgres_engine()")  # Added for debugging
    print("settings.URL_CONNECT", settings.URL_CONNECT)
    url = settings.URL_CONNECT.format(
        user=settings.USER,
        password=quote_plus(settings.PASSWORD),
        host=settings.HOST,
        port=settings.PORT,
        database=settings.DATABASE
    )
    print("Postgres Engine URL: ", url)  # Print the URL
    return url
