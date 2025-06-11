FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV KAFKA_TOPIC=demo-topic
ENV KAFKA_GROUP_ID=consumer-group
ENV MAX_MESSAGES_PER_BATCH=10
ENV CONSUMER_TIMEOUT=5

# Run the consumer
CMD ["python", "consumer.py"]