from flask import Flask, request, jsonify
import json
import pika
app = Flask(__name__)

RABBITMQ_HOST = 'rabbitmq' #nazwa kontenera rabbitmq
QUEUE_NAME = 'tasks'

def send_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(task_data)
    )

    connection.close()

@app.route('/task', methods=['POST'])
def add_task():
    task = request.get_json()
    if not task or 'title' not in task:
        return jsonify({'error': 'Invalid task data'}), 400
    send_to_queue(task)
    return jsonify({'status': 'Task added to queue'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)