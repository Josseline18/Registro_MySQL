#!/usr/bin/env python
#se queda escuchando la cola de RabbitMQ y muestra en terminal cada mensaje que llega
import pika
import json


def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Mensaje recibido:")
    print(f"     Evento: {message.get('event')}")
    print(f"     Usuario ID: {message.get('user_id')}")
    print(f"     Username: {message.get('username')}")
    print(f"     Mensaje: {message.get('message')}")
    print("-" * 50)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5678,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='user_registration', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='user_registration',
        on_message_callback=callback
    )

    print(' [*] Esperando mensajes de registro. CTRL+C para salir')
    channel.start_consuming()


if __name__ == '__main__':
    main()