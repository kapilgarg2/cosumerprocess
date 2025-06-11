import json
import time
import threading
import requests
from faker import Faker

fake = Faker()

# In-memory queue to simulate Kafka
message_queue = []

# Mock producer
def produce_messages():
    while True:
        message = {
            "callback": f"http://localhost:5000/callback/{fake.uuid4()}",
            "response": {
                "id": fake.uuid4(),
                "name": fake.name(),
                "email": fake.email(),
                "timestamp": fake.iso8601(),
                "data": {
                    "value": fake.random_number(digits=3),
                    "status": fake.random_element(elements=('success', 'pending', 'failed'))
                }
            }
        }
        message_queue.append(message)
        print(f"Produced: {json.dumps(message, indent=2)}")
        time.sleep(2)

# Mock consumer
def consume_messages():
    while True:
        if message_queue:
            message = message_queue.pop(0)
            callback_url = message["callback"]
            response = message["response"]
            try:
                r = requests.post(callback_url, json=response)
                print(f"Sent callback to {callback_url}, status: {r.status_code}")
            except Exception as e:
                print(f"Failed to send callback: {e}")
        else:
            time.sleep(1)

if __name__ == "__main__":
    # Start producer and consumer threads
    producer_thread = threading.Thread(target=produce_messages, daemon=True)
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    producer_thread.start()
    consumer_thread.start()
    print("Mocked demo running. Start mock_server.py to receive callbacks.")
    while True:
        time.sleep(10) 