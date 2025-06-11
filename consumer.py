from confluent_kafka import Consumer, KafkaError
import json
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
from config import CONSUMER_TIMEOUT, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID, MAX_MESSAGES_PER_BATCH

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
        self.executor = ThreadPoolExecutor(max_workers=MAX_MESSAGES_PER_BATCH)

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
            
            futures = []
            # Submit each message in the batch to the thread pool
            for message_data in batch_data:
                future = self.executor.submit(self.process_single_message, message_data)
                futures.append(future)

            # Wait for all futures to complete and handle any errors
            for future in futures:
                try:
                    future.result(timeout=30)  # Add timeout to prevent hanging
                except TimeoutError:
                    logger.error("Message processing timed out after 30 seconds")
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

            #commit the message
            try:
                self.consumer.commit(asynchronous=True)
                logger.info(f"Committed message: {len(message)}")
            except Exception as e:
                logger.error(f"Error committing message: {str(e)}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message")
        except Exception as e:
            logger.error(f"Error processing batch message: {str(e)}")

    def start(self):
        try:
            logger.info(f"Starting consumer for topic: {KAFKA_TOPIC}")
            
            while True:
                messages = self.consumer.consume(num_messages=MAX_MESSAGES_PER_BATCH, timeout=CONSUMER_TIMEOUT)
                if not messages:
                    continue
                
                valid_messages = []
                for msg in messages:
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            logger.info(f"Reached end of partition {msg.partition()}")
                        else:
                            logger.error(f"Error: {msg.error()}")
                    else:
                        valid_messages.append(msg)

                if not valid_messages:
                    continue
                
                self.process_message(valid_messages)
                    
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        finally:
            self.executor.shutdown(wait=True)
            self.consumer.close()

if __name__ == '__main__':
    consumer = KafkaConsumer()
    consumer.start()