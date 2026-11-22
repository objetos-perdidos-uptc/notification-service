import asyncio
from app.infrastructure.services.email_sender import BrevoEmailSender # <-- Cambiado
from app.application.use_cases.send_notification import SendHighMatchNotificationUseCase
from app.infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer

async def main():
    print("🚀 Iniciando Notification Service...")
    
    email_sender = BrevoEmailSender() # <-- Cambiado
    use_case = SendHighMatchNotificationUseCase(email_sender)
    consumer = RabbitMQConsumer(use_case)

    await consumer.start_consuming()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())