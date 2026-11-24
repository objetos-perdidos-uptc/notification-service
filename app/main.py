import asyncio
from prometheus_client import start_http_server
from app.infrastructure.services.email_sender import BrevoEmailSender
from app.application.use_cases.send_notification import SendHighMatchNotificationUseCase
from app.infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer

async def main():
    print("Iniciando Notification Service...")

    # Iniciar servidor de métricas en el puerto 8001 (corre en un hilo)
    start_http_server(8001)
    print("Servidor Prometheus escuchando en http://0.0.0.0:8001/metrics")

    email_sender = BrevoEmailSender()
    use_case = SendHighMatchNotificationUseCase(email_sender)
    consumer = RabbitMQConsumer(use_case)

    await consumer.start_consuming()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())