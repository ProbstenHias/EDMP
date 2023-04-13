from dotenv import load_dotenv
from flask import Flask, jsonify, request
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

@app.route('/convert', methods=['POST'])
def convert():
    # Get request data
    data = request.get_json()
    
    json = dc.convert_to_universal(
        source_db=data['source_db_type'],
        dbname=data['source_db'],
        user=data['source_user'],
        password=data['source_pwd'],
        host=data['source_host'],
        port=data['source_port'],
        table_name=data['source_table'],
    )
    
    
    target_db_type = data['target_db_type']
    new_user, new_password, new_dbname = generate_user_credentials()
    print(new_user, new_password, new_dbname)
    
    login_generator = None
    if target_db_type == 'mysql':
        login_generator = GenerateLoginMysql()
    
    login_generator.generate_login(new_user, new_password, new_dbname)
    
    dc.convert_to_data(
        target_db=target_db_type,
        json_data=json,
        dbname=new_dbname,
        user=new_user,
        password=new_password,
        table_name=data['source_table'],
    )
    print("Data converted successfully")
    
    send_email(
        data['email'],
        target_db_type,
        new_user,
        new_password,
        new_dbname
    )
    print("Email sent successfully")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")