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
from pathlib import Path

def send_report_email(subject, body, recipients, attachment_path=None):
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    alias = "dakamine@rlfenergy.com"  # alias visible

    # Debug
    print("DEBUG: EMAIL_USER set?", sender_email is not None)
    print("DEBUG: EMAIL_PASS set?", password is not None)

    if not sender_email or not password:
        raise ValueError("⚠️ Faltan las variables de entorno EMAIL_USER o EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = f"{alias} <{sender_email}>"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Adjuntar PDF
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=Path(attachment_path).name)
        part["Content-Disposition"] = f'attachment; filename="{Path(attachment_path).name}"'
        msg.attach(part)

    # Enviar por Gmail SMTP usando SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("✅ Correo enviado correctamente.")
    except smtplib.SMTPAuthenticationError as e:
        print("❌ Error de autenticación SMTP:", e)
        raise
    except Exception as e:
        print("❌ Error enviando correo:", e)
        raise
