import mysql.connector
from .generate_login import GenerateLogin
import os
from dotenv import load_dotenv

class GenerateLoginMysql(GenerateLogin):

    def __init__(self):
        load_dotenv()
        self.admin_user = os.getenv('ADMIN_MYSQL_USER')
        self.admin_pw = os.getenv('ADMIN_MYSQL_PASSWORD')
        self.host = os.getenv('ADMIN_MYSQL_HOST')
        self.port = os.getenv('ADMIN_MYSQL_PORT')
        self.connection = mysql.connector.connect(
            user=self.admin_user, password=self.admin_pw, host=self.host, port=self.port
        )
        self.cursor = self.connection.cursor()

    def generate_login(self, new_username, new_password, new_dbname):
        self.cursor.execute(f"CREATE USER \'{new_username}\'@\'%\' IDENTIFIED WITH mysql_native_password BY \'{new_password}\';")
        self.cursor.execute(f"CREATE DATABASE {new_dbname};")
        self.cursor.execute(f"GRANT ALL PRIVILEGES ON {new_dbname}.* TO \'{new_username}\'@\'%\';")
        print(f"User: {new_username} Password: {new_password} Database: {new_dbname} Host: {self.host} created successfully")

        # Commit the changes and close the connection
        self.connection.commit()
        self.cursor.close()
        self.connection.close()