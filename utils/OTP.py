import os
import random
import string

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables from .env file
load_dotenv()

# Email configuration settings
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USERNAME"),  # SMTP server username
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),  # SMTP server password
    MAIL_FROM=os.getenv("SMTP_FROM"),  # Sender email address
    MAIL_PORT=int(os.getenv("SMTP_PORT")),  # SMTP server port
    MAIL_SERVER=os.getenv("SMTP_SERVER"),  # SMTP server address
    MAIL_STARTTLS=os.getenv("SMTP_TLS").lower() == "true",  # Enable STARTTLS
    MAIL_SSL_TLS=os.getenv("SMTP_SSL").lower() == "true",  # Enable SSL/TLS
    USE_CREDENTIALS=True,  # Use SMTP credentials
    VALIDATE_CERTS=True,  # Validate SMTP server certificates
    MAIL_FROM_NAME="Foodricion"  # Sender name
)


# Function to generate a 6-digit OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# Function to send an OTP email to the user
async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="Password Reset OTP",  # Email subject
        recipients=[email],  # Recipient email address
        body=f"Your OTP for password reset is: {otp}. This code will expire in 3 minutes.",  # Email body
        subtype=MessageType.html  # Email content type
    )

    fm = FastMail(conf)  # Initialize FastMail with the configuration
    await fm.send_message(message)  # Send the email message
