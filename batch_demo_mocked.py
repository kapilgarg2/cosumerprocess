import json
import time
import threading
import requests
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Thread %(thread)d - %(message)s'
)
logger = logging.getLogger(__name__)

fake = Faker()

# In-memory queue to simulate Kafka
message_queue = []

# Mock producer
def produce_batch_messages():
    while True:
        # Generate a batch of 5-10 random messages
        batch_size = fake.random_int(min=5, max=10)
        batch = []
        
        for _ in range(batch_size):
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
            batch.append(message)
        
        message_queue.append(batch)
        # logger.info(f"Produced batch of {batch_size} messages")
        # logger.info(f"Sample message from batch: {json.dumps(batch[0], indent=2)}")
        time.sleep(3)  # Produce a new batch every 3 seconds

# Mock consumer with thread pool
def consume_batch_messages():
    # Create a thread pool with 10 workers
    executor = ThreadPoolExecutor(max_workers=10)
    
    def process_single_message(message):
        thread_id = threading.get_ident()
        callback_url = message["callback"]
        response = message["response"]
        
        # Simulate some processing time
        processing_time = fake.random_int(min=1, max=3)
        
        logger.info(f"Thread {thread_id} - Starting to process message {response['id']}")
        time.sleep(processing_time)  # Simulate work being done
        
        try:
            r = requests.post(callback_url, json=response)
            logger.info(f"Thread {thread_id} - Completed message {response['id']} - Status: {r.status_code}")
        except Exception as e:
            logger.error(f"Thread {thread_id} - Failed to process message {response['id']}: {e}")
    
    while True:
        if message_queue:
            batch = message_queue.pop(0)
            logger.info(f"Processing batch of {len(batch)} messages")
            
            # Submit each message in the batch to the thread pool
            for message in batch:
                executor.submit(process_single_message, message)
        else:
            time.sleep(1)

if __name__ == "__main__":
    # Start producer and consumer threads
    producer_thread = threading.Thread(target=produce_batch_messages, daemon=True)
    consumer_thread = threading.Thread(target=consume_batch_messages, daemon=True)
    
    producer_thread.start()
    consumer_thread.start()
    
    print("\nBatch Mocked Demo Running")
    print("------------------------")
    print("1. Start mock_server.py to receive callbacks")
    print("2. This demo will generate batches of 5-10 messages every 3 seconds")
    print("3. Messages will be processed in parallel using a thread pool")
    print("4. You'll see different thread IDs processing messages simultaneously")
    print("5. Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopping batch demo...") 