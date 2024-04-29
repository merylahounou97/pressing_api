from fastapi import  HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  src.config import Settings

settings = Settings()



async def send_email(to: str, subject: str, body: str):
    sender_email = settings.sender_email
    sender_password = settings.mail_password
    
    # Création du message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to
    message["Subject"] = subject
    
    # Ajout du corps du message
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connexion au serveur SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Active la sécurité TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, message.as_string())
            return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
