from abc import ABC, abstractmethod

class GenerateLogin(ABC):

    @abstractmethod
    def generate_login(self, new_username, new_password, new_dbname):
        pass
