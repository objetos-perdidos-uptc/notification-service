import aio_pika
import json
import os
from app.application.use_cases.send_notification import SendHighMatchNotificationUseCase
from app.main import EMAILS_SENT, EMAILS_FAILED

class RabbitMQConsumer:
    def __init__(self, use_case: SendHighMatchNotificationUseCase):
        self.use_case = use_case
        self.amqp_url = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")

    async def start_consuming(self):
        connection = await aio_pika.connect_robust(self.amqp_url)
        channel = await connection.channel()
        
        # Declaramos la misma cola que usa el Matching Service
        queue = await channel.declare_queue("match_notifications", durable=True)
        print("[RABBITMQ] Escuchando eventos de coincidencias...")

        async def process_message(message: aio_pika.IncomingMessage):
            
            async with message.process():
                body = json.loads(message.body.decode())
                user_id = body["user_id"]
                score = body["match_data"]["score"]
                
                email_destino = os.getenv("TEST_EMAIL_DESTINATION")
                nombre_usuario = f"Estudiante {user_id}"

                print(f"[EVENTO RECIBIDO] Match para usuario {user_id} (Score: {score}%)")
                
                # Ejecutamos el caso de uso
                await self.use_case.execute(
                    to_email=email_destino, 
                    user_name=nombre_usuario, 
                    score=score
                )
                try:
                    await self.use_case.execute(
                        to_email=email_destino,
                        user_name=nombre_usuario,
                        score=score
                    )
                    EMAILS_SENT.inc() # <-- Suma 1 si fue exitoso
                except Exception as e:
                    print(f"Error enviando correo: {e}")
                    EMAILS_FAILED.inc() # <-- Suma 1 si falló

                

        # Empezamos a escuchar
        await queue.consume(process_message)