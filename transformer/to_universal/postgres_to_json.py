import psycopg2
import json
import requests
from .data_to_json import DataToJsonConverter
import os


class PostgresDataToJson(DataToJsonConverter):
    def __init__(self):
        self.session = None
        self.headers = None
        self.database_id = None
        self.sup_base_url = os.environ.get("SUPERSET_URL")
        self.auth_endpoint = f"{self.sup_base_url}/api/v1/security/login"
        self.csrf_url = f"{self.sup_base_url}/api/v1/security/csrf_token/"
        self.database_endpoint = f"{self.sup_base_url}/api/v1/database/"
        self.execute_endpoint = f"{self.sup_base_url}/api/v1/sqllab/execute/"
        self.results_endpoint = f"{self.sup_base_url}/api/v1/sqllab/results/"

    def do_authentication(self, username: str, password: str) -> None:
            """
            Authenticates the user with Superset
            """
            # Authenticate the user with Superset
            payload = {
                "username": username,
                "provider": "db",
                "refresh": True,
                "password": password,
            }
            try:
                response = requests.post(
                    self.auth_endpoint, json=payload
                )

                if response.status_code == 200:
                    access_token = json.loads(response.text)["access_token"]
                    self.headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                    }
                else:
                    print(
                        "Encountered error authenticating with Superset: "
                        + str(response.status_code)
                    )
            except Exception as e:
                print("Encountered error authenticating with Superset: " + str(e))

    def get_csrf_token(self, session: requests.Session) -> str:
        """
        Returns the CSRF token from Superset
        """
        try:
            response = session.get(self.csrf_url)
            csrf_token = response.json()["result"]
            return csrf_token
        except Exception as e:
            print("Encountered error getting CSRF token: " + str(e))

    def connect(self, dbname, **kwargs):
        try:
            sup_user = os.environ.get("SUPERSET_USER")
            sup_pw = os.environ.get("SUPERSET_PASSWORD")
            self.do_authentication(sup_user, sup_pw)
            
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            csrf_token = self.get_csrf_token(self.session)
            self.headers["X-CSRFToken"] = csrf_token
            self.session.headers.update(self.headers)

            database_response = self.session.get(self.database_endpoint, headers=self.headers)
            databases = database_response.json()["result"]
            for db in databases:
                if db["database_name"] == dbname:
                    self.database_id = db["id"]
            print("Connected to Superset successfully!")
        except Exception as e:
            print("Encountered error connecting to superset: " + str(e))

            

    def disconnect(self, **kwargs):
        pass

    def fetch_data(self, table_name, schema, **kwargs):
        execute_payload = {
            "database_id": self.database_id,
            "sql": f'SELECT * FROM {schema}."{table_name}"',
            "runAsync": False,
        }
        return self.session.post(self.execute_endpoint, headers=self.headers, json=execute_payload)

    def convert_to_json(self, data, **kwargs):
        data_field = data.json()["data"]
        return data_field