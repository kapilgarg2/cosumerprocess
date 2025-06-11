# Kafka Callback Consumer

A simple Kafka consumer that forwards messages to callback URLs.

## Project Structure

```
.
├── requirements.txt
├── README.md
├── config.py          # Configuration settings
├── consumer.py        # Kafka consumer implementation
├── demo_mocked.py     # Mocked demo (no Kafka required)
├── mock_server.py     # Mock callback server
└── env.example        # Environment variables template
```

## Features

- Consumes messages from Kafka using confluent-kafka
- Forwards responses to callback URLs
- Simple error handling and logging
- Configurable through environment variables
- Includes mocked demo (no Kafka required)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd kafka-callback-consumer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

## Running the Demo

1. Start the mock callback server:
```bash
python mock_server.py
```

2. In a new terminal, run the mocked demo:
```bash
python demo_mocked.py
```

The demo will:
1. Generate random messages every 2 seconds
2. Simulate consuming these messages
3. Send callbacks to the mock server
4. Mock server will log received callbacks

## Running with Real Kafka

If you have Kafka running:

1. Update `.env` with your Kafka configuration
2. Start the consumer:
```bash
python consumer.py
```

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

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Make your changes and commit:
```bash
git add .
git commit -m "Your commit message"
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 