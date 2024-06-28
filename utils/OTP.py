import os
import random
import string

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USERNAME"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_FROM"),
    MAIL_PORT=int(os.getenv("SMTP_PORT")),
    MAIL_SERVER=os.getenv("SMTP_SERVER"),
    MAIL_STARTTLS=os.getenv("SMTP_TLS").lower() == "true",
    MAIL_SSL_TLS=os.getenv("SMTP_SSL").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_FROM_NAME="Foodricion"
)


# Function to Generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# Function to send OTP email
async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="Password Reset OTP",
        recipients=[email],
        body=f"Your OTP for password reset is: {otp}. This code will expire in 3 minutes.",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
