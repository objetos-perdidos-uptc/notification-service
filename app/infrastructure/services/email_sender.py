import httpx
import os
from app.domain.ports import IEmailSender
from dotenv import load_dotenv

load_dotenv()

class BrevoEmailSender(IEmailSender):
    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")
        self.api_url = "https://api.brevo.com/v3/smtp/email"
        self.sender_email = "notificaciones@seeker-uptc.com"
        self.sender_name = "Seeker UPTC"

    async def send_high_match_email(self, to_email: str, subject: str, body: str) -> None:
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json"
        }
        
        payload = {
            "sender": {"name": self.sender_name, "email": self.sender_email},
            "to": [{"email": to_email}],
            "subject": subject,
            "textContent": body,
            "replyTo": {"email": "nicolasdavid.lizarazo@gmail.com", "name": "Soporte Seeker UPTC"}
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status() # Lanza error si Brevo rechaza el correo
                print(f"📧 [BREVO] Correo enviado exitosamente a {to_email}")
            except Exception as e:
                print(f"❌ [ERROR BREVO] No se pudo enviar a {to_email}: {e}")