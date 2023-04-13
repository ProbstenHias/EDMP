import psycopg2
import json
from .data_to_json import DataToJsonConverter


class PostgresDataToJson(DataToJsonConverter):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, dbname, user, password, host, port, **kwargs):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def disconnect(self, **kwargs):
        self.cursor.close()
        self.conn.close()

    def fetch_data(self, table_name, **kwargs):
        self.cursor.execute(f"SELECT * FROM \"{table_name}\";")
        column_names = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        return column_names, rows

    def convert_to_json(self, data, **kwargs):
        column_names, rows = data
        json_data = [dict(zip(column_names, row)) for row in rows]
        return json_data
