import pika
import json


def enviar_mensaje(username: str, placa: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5678,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='user_registration', durable=True)

    mensaje = {
        'username': username,
        'placa': placa,
        'message': f'Cliente {username} registrado con placa {placa}'
    }

    channel.basic_publish(
        exchange='',
        routing_key='user_registration',
        body=json.dumps(mensaje)
    )
    connection.close()