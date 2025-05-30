import pika
import json
import os
import time

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
QUEUE_NAME = 'tasks'


def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"Received task: {task}")
    
def main():
    # Retry połączenia (bo RabbitMQ może jeszcze nie wstać)
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(3)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print('Worker is waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()