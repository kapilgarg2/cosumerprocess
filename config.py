import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'your-topic-name')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'consumer-group') 
MAX_MESSAGES_PER_BATCH = int(os.getenv('MAX_MESSAGES_PER_BATCH', '10'))
CONSUMER_TIMEOUT = int(os.getenv('CONSUMER_TIMEOUT', '5'))