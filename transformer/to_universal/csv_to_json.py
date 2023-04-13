import csv
import json
from .data_to_json import DataToJsonConverter


class CsvDataToJson(DataToJsonConverter):
    def connect(self, *args, **kwargs):
        pass

    def disconnect(self):
        pass

    def fetch_data(self, file_path):
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            column_names = next(reader)  # Get the header row
            rows = [row for row in reader]
        return column_names, rows

    def convert_to_json(self, data):
        column_names, rows = data
        json_data = [dict(zip(column_names, row)) for row in rows]
        return json_data
