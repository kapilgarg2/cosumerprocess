from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/callback/<path:callback_id>', methods=['POST'])
def callback(callback_id):
    data = request.json
    logger.info(f"Received callback for ID: {callback_id}")
    logger.info(f"Response data: {data}")
    return jsonify({"status": "received", "callback_id": callback_id})

if __name__ == '__main__':
    app.run(port=5000) 