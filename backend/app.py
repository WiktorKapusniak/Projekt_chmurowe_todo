from flask import Flask, request, jsonify
import pika
import json
import os
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')

client = MongoClient(f'mongodb://{MONGO_HOST}:27017/')
db = client.todo_db
tasks_collection = db.tasks

@app.route('/task', methods=['POST'])
def add_task():
    task = request.json
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps(task))
    connection.close()
    return jsonify({'message': 'Task queued successfully'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find({}, {'_id': 0}))
    return jsonify(tasks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)