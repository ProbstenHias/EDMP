import psycopg2
from .generate_login import GenerateLogin

class GenerateLoginPostgres(GenerateLogin):

    def __init__(self, admin_user, admin_password, host, port):
        self.connection = psycopg2.connect(
            dbname='postgres', user=admin_user, password=admin_password, host=host, port=port
        )
        self.cursor = self.connection.cursor()

    def generate_login(self, new_username, new_password, new_dbname):
        self.cursor.execute("CREATE USER %s WITH PASSWORD %s", (new_username, new_password))
        self.cursor.execute("CREATE DATABASE %s WITH OWNER %s", (new_dbname, new_username))

        # Commit the changes and close the connection
        self.connection.commit()
        self.cursor.close()
        self.connection.close()