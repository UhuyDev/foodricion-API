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
    html_content = f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Foodricion Account Verification</title>
        <meta name="ROBOTS" content="NOINDEX, NOFOLLOW">
        <style>table td {{border-collapse:collapse;margin:0;padding:0;}}</style>
    </head>
    <body dir="ltr" lang="en-US">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" dir="ltr" lang="en-US">
            <tr>
                <td valign="top" width="50%"></td>
                <td valign="top">
                    <!-- Email Header -->
                    <table width="640" cellpadding="0" cellspacing="0" border="0" dir="ltr" lang="en-US" style="border-left:1px solid #e3e3e3;border-right: 1px solid #e3e3e3;">
                        <tr style="background-color: #39B19B;">
                            <td width="1" style="background:#39B19B; border-top:1px solid #e3e3e3;"></td>
                            <td width="24" style="border-top:1px solid #e3e3e3;border-bottom:1px solid #e3e3e3;">&nbsp;</td>
                            <td width="310" valign="middle" style="border-top:1px solid #e3e3e3; border-bottom:1px solid #e3e3e3;padding:12px 0;">
                                <h1 style="line-height:20pt;font-family:Segoe UI Light; font-size:18pt; color:#ffffff; font-weight:normal;"><font color="#FFFFFF">Password Reset</font></h1>
                            </td>
                            <td width="24" style="border-top: 1px solid #e3e3e3;border-bottom: 1px solid #e3e3e3;">&nbsp;</td>
                        </tr>
                    </table>
                    <!-- Email Content -->
                    <table width="640" cellpadding="0" cellspacing="0" border="0" dir="ltr" lang="en-US">
                        <tr>
                            <td width="1" style="background:#e3e3e3;"></td>
                            <td width="24">&nbsp;</td>
                            <td id="PageBody" width="640" valign="top" colspan="2" style="border-bottom:1px solid #e3e3e3;padding:10px 0 20px;border-bottom-style:hidden;">
                                <table cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td width="630" style="font-size:10pt; line-height:13pt; color:#000;">
                                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="" dir="ltr" lang="en-US">
                                                <tr>
                                                    <td>
                                                        <div style="font-family:'Segoe UI', Tahoma, sans-serif; font-size:14px; color:#333; font-weight: bold">
                                                            Your Foodricion account's one-time password is: {otp}
                                                        </div>
                                                        <br>
                                                        <div style="font-family:'Segoe UI', Tahoma, sans-serif; font-size:14px; color:#333;">
                                                            This code will expire in 3 minutes. If you did not request this, you can ignore this email.
                                                        </div>
                                                        <br>
                                                        <br>
                                                        <div style="font-family:'Segoe UI', Tahoma, sans-serif; font-size:14px; color:#333;">Best regards,</div>
                                                        <div style="font-family:'Segoe UI', Tahoma, sans-serif; font-size:14px; color:#333;">Foodricion</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                            <td width="1">&nbsp;</td>
                            <td width="1"></td>
                            <td width="1">&nbsp;</td>
                            <td width="1" valign="top"></td>
                            <td width="29">&nbsp;</td>
                            <td width="1" style="background:#e3e3e3;"></td>
                        </tr>
                        <tr>
                            <td width="1" style="background:#e3e3e3; border-bottom:1px solid #e3e3e3;"></td>
                            <td width="24" style="border-bottom:1px solid #e3e3e3;">&nbsp;</td>
                            <td id="PageFooterContainer" width="585" valign="top" colspan="6" style="border-bottom:1px solid #e3e3e3;padding:0px;">
                            </td>
                            <td width="29" style="border-bottom:1px solid #e3e3e3;">&nbsp;</td>
                            <td width="1" style="background:#e3e3e3; border-bottom:1px solid #e3e3e3;"></td>
                        </tr>
                    </table>
                </td>
                <td valign="top" width="50%"></td>
            </tr>
        </table>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Your Password Reset Code from Foodricion",  # Email subject
        recipients=[email],  # Recipient email address
        body=html_content,  # Email body
        subtype=MessageType.html  # Email content type
    )

    fm = FastMail(conf)  # Initialize FastMail with the configuration
    await fm.send_message(message)  # Send the email message