from abc import ABC, abstractmethod

class IEmailSender(ABC):
    @abstractmethod
    async def send_high_match_email(self, to_email: str, subject: str, body: str) -> None:
        """Contrato para enviar un correo de alta coincidencia."""
        pass