# Kafka Callback Consumer

A simple Kafka consumer that forwards messages to callback URLs.

## Project Structure

```
.
├── requirements.txt
├── README.md
├── config.py          # Configuration settings
├── consumer.py        # Kafka consumer implementation
├── demo_producer.py   # Demo message producer
└── mock_server.py     # Mock callback server
```

## Features

- Consumes messages from Kafka using confluent-kafka
- Forwards responses to callback URLs
- Simple error handling and logging
- Configurable through environment variables
- Includes demo producer and mock server

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following configuration:
```
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=demo-topic
KAFKA_GROUP_ID=consumer-group
```

## Running the Demo

1. Start the mock callback server:
```bash
python mock_server.py
```

2. Start the Kafka consumer:
```bash
python consumer.py
```

3. In a new terminal, start the demo producer:
```bash
python demo_producer.py
```

The demo will:
1. Generate random messages with callback URLs
2. Send them to Kafka
3. Consumer will read messages and forward to mock server
4. Mock server will log received callbacks

## Message Format

The consumer expects messages in the following JSON format:
```json
{
    "callback": "https://api.example.com/callback/{uuid}",
    "response": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@example.com",
        "timestamp": "2024-03-14T12:00:00Z",
        "data": {
            "value": 123,
            "status": "success"
        }
    }
}
```

## Error Handling

The consumer includes error handling for:
- Invalid JSON messages
- Missing callback URLs or responses
- Failed HTTP requests to callback URLs
- Kafka connection issues

All errors are logged for debugging purposes. 