from abc import ABC, abstractmethod


class JsonToData(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        """Connect to the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""
        pass

    @abstractmethod
    def prepare_data(self, json_data, *args, **kwargs):
        """Prepare JSON data for insertion into the database."""
        pass

    @abstractmethod
    def insert_data(self, data, *args, **kwargs):
        """Insert the prepared data into the database."""
        pass

    @abstractmethod
    def create_table(self, json_data, *args, **kwargs):
        """Create the table in the database."""
        pass

    def import_from_json(self, json_data, *args, **kwargs):
        """Import JSON data into the database."""
        self.connect(*args, **kwargs)
        data = self.prepare_data(json_data, *args, **kwargs)
        self.create_table(json_data, *args, **kwargs)
        self.insert_data(data, *args, **kwargs)
        self.disconnect()
