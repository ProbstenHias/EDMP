import psycopg2
from .json_to_data import JsonToData


class JsonToPostgres(JsonToData):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def prepare_data(self, json_data, table_name):
        column_names = json_data[0].keys()
        columns = ", ".join(column_names)
        placeholders = ", ".join(["%s"] * len(column_names))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        data = [tuple(item.values()) for item in json_data]
        return insert_query, data

    def create_table(self, json_data, table_name):
        column_defs = ", ".join(
            [f"{key} {value}" for key, value in json_data[0].items()]
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs});"
        self.cursor.execute(create_table_query)

    def insert_data(self, data):
        insert_query, records = data
        self.cursor.executemany(insert_query, records)
