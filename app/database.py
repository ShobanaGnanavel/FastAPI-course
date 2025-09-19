from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import mysql.connector
from mysql.connector import Error
from .config import settings
import os

DATABASE_URL = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}?ssl_ca={os.path.join(os.getcwd(), 'ca.pem')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         database='mydb',
#         user='root',
#         password='testmysql'
#     )

#     if connection.is_connected():
#         print("connected to mysql databases")

#         cursor = connection.cursor()
# except Error as e:
#     print('Error while connecting to database ', e)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print('mysql connection is closed')