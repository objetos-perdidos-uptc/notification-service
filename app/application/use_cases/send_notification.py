from app.domain.ports import IEmailSender

class SendHighMatchNotificationUseCase:
    def __init__(self, email_sender: IEmailSender):
        self.email_sender = email_sender

    async def execute(self, to_email: str, user_name: str, score: float) -> None:
        # Aquí aplicamos la lógica de negocio (qué dice el correo)
        subject = "¡Encontramos una coincidencia para tu objeto perdido!"
        body = (
            f"Hola {user_name},\n\n"
            f"¡Buenas noticias! El sistema Seeker UPTC ha encontrado un objeto "
            f"que coincide en un {score}% con tu reporte de pérdida.\n\n"
            f"Por favor, ingresa a la plataforma para revisar los detalles y reclamarlo.\n\n"
            f"Atentamente,\nEl equipo de Seeker UPTC."
        )
        
        # Llamamos al puerto (la infraestructura real)
        await self.email_sender.send_high_match_email(to_email, subject, body)