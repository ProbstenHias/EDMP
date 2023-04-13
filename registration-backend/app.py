from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from postgres_template import postgres_dag
import requests
import json
from dotenv import load_dotenv
import os
app = Flask(__name__)
CORS(app)


@app.route("/register-db", methods=["POST"])
def register_db():
    db_info = request.json

    # Validate the input
    if not all(
        key in db_info for key in ("host", "port", "username", "password", "db_name")
    ):
        return jsonify({"message": "Invalid input"}), 400

    # Generate the DAG file for the provided PostgreSQL database
    register_db_superset(db_info)
    message, status_code = generate_dag_file(db_info)

    return jsonify(message), status_code


def generate_dag_file(db_info):
    # Use the provided information to generate a DAG file
    dag_id = f"{db_info['db_name']}_to_amundsen"
    dag_file_name = f"{dag_id}.py"
    dag_file_path = os.path.join("./dags", dag_file_name)

    # Check if the DAG file already exists, if so, return an error message
    if os.path.exists(dag_file_path):
        return {
            "message": f"DAG for database '{db_info['db_name']}' already exists"
        }, 400

    # Create a new DAG file with the provided database information
    with open(dag_file_path, "w") as dag_file:
        # Generate the DAG file cont'@daily',ent based on the provided database information
        new_dag = postgres_dag % (
            db_info["username"],
            db_info["password"],
            db_info["host"],
            db_info["port"],
            db_info["db_name"],
            dag_id,
        )

        dag_file.write(new_dag)

    return {
        "message": f"Successfully created DAG for database '{db_info['db_name']}'"
    }, 200


def register_db_superset(db_info):
    load_dotenv()
    SUP_BASE_URL = os.getenv("SUP_BASE_URL")
    SUP_USERNAME = os.getenv("SUP_USERNAME")
    SUP_PASSWORD = os.getenv("SUP_PASSWORD")
    db_name = db_info["db_name"]
    db_username = db_info["username"]
    db_password= db_info["password"]
    db_host = db_info["host"]
    db_port = db_info["port"]

    database_payload = {
        "database_name": db_name,
        "sqlalchemy_uri": f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}",
        "cache_timeout": 86400,
    }
    auth_payload = {
    'username': SUP_USERNAME,
    'provider': "db",
    "refresh": True,
    'password': SUP_PASSWORD
    }
    auth_response = requests.post(f'{SUP_BASE_URL}/security/login', json=auth_payload)
    
    if auth_response.status_code == 200:
        access_token = json.loads(auth_response.text)['access_token']
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        database_response = requests.post(f'{SUP_BASE_URL}/database', headers=headers, json=database_payload)
        if database_response.status_code == 201:
            print(f'{db_name} database registered successfully in Superset.')
        else:
            print(f'Failed to register {db_name} database in Superset. Error: {database_response.text}')
    else:
        print(f'Authentication failed. Error: {auth_response.text}')


if __name__ == "__main__":
    app.run(port=5002, debug=True, host="0.0.0.0")
