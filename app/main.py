import asyncio
from prometheus_client import start_http_server, Counter  # <-- NUEVO IMPORT
from app.infrastructure.services.email_sender import BrevoEmailSender
from app.application.use_cases.send_notification import SendHighMatchNotificationUseCase
from app.infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer

EMAILS_SENT = Counter('notification_emails_sent_total', 'Total de correos enviados exitosamente')
EMAILS_FAILED = Counter('notification_emails_failed_total', 'Total de correos fallidos')

async def main():
    print("Iniciando Notification Service...")

    # Iniciar servidor de métricas en el puerto 8001 (corre en un hilo en segundo plano)
    start_http_server(8001)
    print("Servidor Prometheus escuchando en http://0.0.0.0:8001/metrics")

    email_sender = BrevoEmailSender()
    use_case = SendHighMatchNotificationUseCase(email_sender)
    consumer = RabbitMQConsumer(use_case)

    await consumer.start_consuming()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())