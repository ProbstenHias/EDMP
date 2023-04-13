import mysql.connector
from .json_to_data import JsonToData
from dotenv import load_dotenv
import os


class JsonToMySQL(JsonToData):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, dbname, user, password, **kwargs):
        load_dotenv()
        host = os.getenv("ADMIN_MYSQL_HOST")
        port = os.getenv("ADMIN_MYSQL_PORT")
        self.conn = mysql.connector.connect(
            database=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def disconnect(self, **kwargs):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def prepare_data(self, json_data, table_name, **kwargs):
        column_names = json_data[0].keys()
        columns = ", ".join(column_names)
        placeholders = ", ".join(["%s"] * len(column_names))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        data = [tuple(item.values()) for item in json_data]
        return insert_query, data

    def create_table(self, json_data, table_name, **kwargs):
        column_defs = ", ".join(
            [f"{key} {self.sql_datatype_from_python_datatype(value)}" for key, value in json_data[0].items()]
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs});"
        self.cursor.execute(create_table_query)

    def insert_data(self, data, **kwargs):
        insert_query, records = data
        self.cursor.executemany(insert_query, records)

    def sql_datatype_from_python_datatype(self, value):
        # check the type of the value and return the appropriate SQL datatype, make it with switch case

        
        if isinstance(value, int):
            return "INT"
        elif isinstance(value, float):
            return "FLOAT"
        elif isinstance(value, str):
            return "VARCHAR(255)"
        elif isinstance(value, bool):
            return "TINYINT(1)"
        else:
            return "TEXT"
