import time, os, json, random 
from datetime import datetime
from data_generator import generate_message
from kafka import KafkaProducer, KafkaConsumer
import threading

kafka_url = os.getenv('KAFKA_URL')

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=[f'{kafka_url}'],
    value_serializer=serializer,
    max_block_ms=10000
)

consumer = KafkaConsumer(
    'controller_requests',
    bootstrap_servers=[f'{kafka_url}'],
    auto_offset_reset='latest',
    group_id='controller_group'
)

if __name__ == '__main__':
    for message in consumer:
        print(f'controller received update request: {message}')
        msg_json = json.loads(message.value.decode('utf-8'))
        node_topic = msg_json['node']
        print(f'Node topic: {node_topic}')
        update = generate_message(node_topic)
        print(f'Generated update: {update}')
        future = producer.send(node_topic, update)
        try:
            result = future.get(timeout=5)
            print(f'Update sent to {node_topic}: {update}')
        except Exception as e:
            print(f'Failed to send update to {node_topic}: {e}')