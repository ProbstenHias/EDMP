import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from dotenv import load_dotenv
import os


def send_email(
    receiver_email, db_type, new_user, new_password, new_dbname
):
    load_dotenv()
    # Create a message object
    sender_email = os.getenv("SENDER_MAIL_ADRESS")
    password = os.getenv("SENDER_MAIL_PASSWORD")
    smtp_host = os.getenv("SENDER_MAIL_HOST")
    smtp_port = os.getenv("SENDER_MAIL_PORT")
    body = f"Your {db_type} credentials are: \nUsername: {new_user} \nPassword: {new_password} \nDatabase: {new_dbname}"
    message = MIMEText(body)
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = db_type + " credentials"

    try:
        smtp_session = smtplib.SMTP(smtp_host, smtp_port)
        smtp_session.starttls()
        smtp_session.login(sender_email, password)

        smtp_session.send_message(message)
        smtp_session.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email could not be sent due to an error: ", e)
