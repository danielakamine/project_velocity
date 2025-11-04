# -*- coding: utf-8 -*-
"""
Envío de correos con adjunto (PDF del reporte).
Usa SMTP, compatible con Gmail, Outlook, etc.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_report_email(subject, body, recipients, attachment_path=None):
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender_email or not password:
        raise ValueError("⚠️ Faltan las variables de entorno EMAIL_USER o EMAIL_PASS")

    msg = MIMEMultipart()
    alias = "dakamine@rlfenergy.com"
    msg["From"] = f"{alias} <{sender_email}>"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    print("✅ Correo enviado correctamente.")