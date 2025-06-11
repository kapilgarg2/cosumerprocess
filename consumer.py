from confluent_kafka import Consumer, KafkaError
import json
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': KAFKA_GROUP_ID,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True
        })
        self.consumer.subscribe([KAFKA_TOPIC])
        # Create a thread pool with 10 workers
        self.executor = ThreadPoolExecutor(max_workers=10)

    def process_single_message(self, message_data):
        try:
            callback_url = message_data.get('callback')
            response = message_data.get('response')
            
            if not callback_url or not response:
                logger.error("Missing callback URL or response")
                return
            
            requests.post(callback_url, json=response)
            logger.info(f"Sent response to {callback_url}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def process_message(self, message):
        try:
            # Parse the message value as a list of dictionaries
            batch_data = json.loads(message.value().decode('utf-8'))
            
            if not isinstance(batch_data, list):
                logger.error("Message is not a list of dictionaries")
                return
            
            # Submit each message in the batch to the thread pool
            for message_data in batch_data:
                self.executor.submit(self.process_single_message, message_data)
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message")
        except Exception as e:
            logger.error(f"Error processing batch message: {str(e)}")

    def start(self):
        try:
            logger.info(f"Starting consumer for topic: {KAFKA_TOPIC}")
            
            while True:
                message = self.consumer.poll(1.0)
                
                if message is None:
                    continue
                
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(f"Reached end of partition {message.partition()}")
                    else:
                        logger.error(f"Error: {message.error()}")
                else:
                    self.process_message(message)
                    
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        finally:
            self.executor.shutdown(wait=True)
            self.consumer.close()

if __name__ == '__main__':
    consumer = KafkaConsumer()
    consumer.start() 