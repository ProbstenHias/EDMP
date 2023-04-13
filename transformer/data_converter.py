from to_universal.data_to_json import DataToJsonConverter
from from_universal.json_to_data import JsonToData


class DataConverter:
    def __init__(self):
        self.data_to_json_registry = {}
        self.json_to_data_registry = {}

    def register_data_to_json(self, db_type, converter_class):
        assert issubclass(converter_class, DataToJsonConverter)
        self.data_to_json_registry[db_type] = converter_class

    def register_json_to_data(self, db_type, converter_class):
        assert issubclass(converter_class, JsonToData)
        self.json_to_data_registry[db_type] = converter_class

    def convert(self, source_db, target_db, *args, **kwargs):
        # Instantiate source and target converter classes
        source_converter = self.data_to_json_registry[source_db]()
        target_converter = self.json_to_data_registry[target_db]()

        # Fetch data from source database and convert to JSON
        json_data = source_converter.export_to_json(*args, **kwargs)

        # Import JSON data into the target database
        target_converter.import_from_json(json_data, *args, **kwargs)

    def convert_to_universal(self, source_db, *args, **kwargs):
        # Instantiate source converter class
        source_converter = self.data_to_json_registry[source_db]()

        # Fetch data from source database and convert to JSON
        json_data = source_converter.export_to_json(*args, **kwargs)

        return json_data

    def convert_to_data(self, target_db, json_data, *args, **kwargs):
        # Instantiate target converter class
        target_converter = self.json_to_data_registry[target_db]()

        # Import JSON data into the target database
        target_converter.import_from_json(json_data, *args, **kwargs)
