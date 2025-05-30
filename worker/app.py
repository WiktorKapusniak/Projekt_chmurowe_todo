import pika
import json
import os
import time
from pymongo import MongoClient
from datetime import datetime

# Konfiguracja
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')
QUEUE_NAME = 'tasks'

def save_to_mongo(task):
    client = MongoClient(f'mongodb://{MONGO_HOST}:27017/')
    db = client.todo_db  # nazwa bazy danych
    tasks_collection = db.tasks  # nazwa kolekcji

    # Dodajemy timestamp do taska
    task['created_at'] = datetime.utcnow()

    # Wstawiamy task do kolekcji
    result = tasks_collection.insert_one(task)
    print(f"Task inserted with id: {result.inserted_id}")

def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"Received task: {task}")
    save_to_mongo(task)

def main():
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
