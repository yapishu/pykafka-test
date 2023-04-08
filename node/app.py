import json, os, time
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
import threading

kafka_url = os.getenv('KAFKA_URL')
hostname = os.getenv('HOSTNAME')

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=[f'{kafka_url}'],
    value_serializer=serializer,
    max_block_ms=120000
)

consumer = KafkaConsumer(
    hostname,
    bootstrap_servers=[f'{kafka_url}'],
    auto_offset_reset='latest',
    group_id=f'{hostname}'
)

def consume_updates():
    for message in consumer:
        print('Consooooming:')
        msg = json.loads(message.value)
        for key in msg:
            val = msg[key]
            print(f'{key} is {val}')

def request_updates():
    while True:
        # Request an update from the controller
        print("Node requesting update")
        producer.send('controller_requests', {'node': hostname})
        time.sleep(10)

if __name__ == '__main__':
    consume_thread = threading.Thread(target=consume_updates)
    request_thread = threading.Thread(target=request_updates)
    consume_thread.start()
    request_thread.start()