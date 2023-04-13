from abc import ABC, abstractmethod


class DataToJsonConverter(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        """Connect to the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""
        pass

    @abstractmethod
    def fetch_data(self, *args, **kwargs):
        """Fetch data"""
        pass

    @abstractmethod
    def convert_to_json(self, data):
        """Convert the fetched data to JSON format."""
        pass

    def export_to_json(self, *args, **kwargs):
        """Export data from the database to a JSON file."""
        self.connect(*args, **kwargs)
        data = self.fetch_data(*args, **kwargs)
        json_data = self.convert_to_json(data)
        self.disconnect()

        # return JSON data
        return json_data
