from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from auth_handler.auth_email import send_email
from auth_handler.generate_login_mysql import GenerateLoginMysql
from auth_handler.generate_user_credentials import generate_user_credentials

from data_converter import DataConverter
from from_universal.json_to_mysql import JsonToMySQL
from to_universal.postgres_to_json import PostgresDataToJson

load_dotenv()

app = Flask(__name__)

dc = DataConverter()
dc.register_data_to_json("postgres", PostgresDataToJson)
dc.register_json_to_data("mysql", JsonToMySQL)


@app.route("/")
def conversion_form():
    # Create a list of target database options
    db_options = [
        ("mysql", "MySQL"),
        ("postgres", "PostgreSQL"),
        ("mongodb", "MongoDB"),
    ]
    # Get default values for the source database parameters from the query string
    source_db_type = request.args.get("db_type", default="postgres")
    source_db = request.args.get("source_db", default="mydatabase")
    source_table = request.args.get("source_table", default="mytable")
    source_schema = request.args.get("source_schema", default="myschema")
    # Render the HTML template and pass in the form data
    return render_template(
        "index.html",
        db_options=db_options,
        source_db_type=source_db_type,
        source_db=source_db,
        source_schema=source_schema,
        source_table=source_table,
    )


@app.route("/convert", methods=["POST"])
def convert():
    # Get request data
    data = request.get_json()
    print(data)

    json = dc.convert_to_universal(
        source_db=data["source_db_type"],
        dbname=data["source_db"],
        table_name=data["source_table"],
        schema=data["source_schema"],
    )

    target_db_type = data["target_db_type"]
    new_user, new_password, new_dbname = generate_user_credentials()
    print(new_user, new_password, new_dbname)

    login_generator = None
    if target_db_type == "mysql":
        login_generator = GenerateLoginMysql()

    login_generator.generate_login(new_user, new_password, new_dbname)

    dc.convert_to_data(
        target_db=target_db_type,
        json_data=json,
        dbname=new_dbname,
        user=new_user,
        password=new_password,
        table_name=data["source_table"],
    )
    print("Data converted successfully")

    send_email(data["email"], target_db_type, new_user, new_password, new_dbname)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(port=5006, host="0.0.0.0")
