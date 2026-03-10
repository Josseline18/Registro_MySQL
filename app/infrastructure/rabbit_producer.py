import pika
import json


def send_message(message: dict):
    """Envía un mensaje a la cola de RabbitMQ"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5678,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='user_registration', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='user_registration',
        body=json.dumps(message, ensure_ascii=False),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type='application/json'
        )
    )

    print(f" [x] Mensaje enviado a RabbitMQ: {message}")
    connection.close()