#!/usr/bin/env python
# coding: utf-8

import smtplib
import email_util
from email.message import EmailMessage

# Mail server settings
SMTP_SERVER = "mail.medhavart.com"
SMTP_PORT = 465

USERNAME = "deep.narayan@medhavart.com"

# Read password from file
with open("password.txt", "r", encoding="utf-8") as f:
    PASSWORD = f.read().strip()

def send_email(to_email, subject, body):

    msg = EmailMessage()

    msg["From"] = USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content(body)

    with smtplib.SMTP_SSL(
        SMTP_SERVER,
        SMTP_PORT
    ) as smtp:

        smtp.login(
            USERNAME,
            PASSWORD
        )

        smtp.send_message(msg)

    print(f"Email sent successfully to {to_email}")

