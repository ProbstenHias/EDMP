from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from postgres_template import postgres_dag

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


if __name__ == "__main__":
    app.run(port=5002, debug=True, host="0.0.0.0")
