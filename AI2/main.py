from flask import Flask, request, jsonify, Response
import logging
from queue import Queue  # Import Queue from the queue module
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS globally for all routes (for testing or general use)
CORS(app, origins="http://localhost:3000")  # Allow React app on port 3000

# Set up logging for received alerts
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Store the list of connected clients (for sending alerts to multiple clients)
clients = []


# Function to handle anomaly alerts
def handle_alert(data):
    # Log the alert received for monitoring
    logging.info(f"Received Anomaly Alert: Type: {data['type']}, Count: {data['count']}, Message: {data['message']}")

    # Here you can add custom logic for what should happen after receiving the alert
    # For example, you could send an email, trigger a notification, or call another function
    if data['type'] == "Voltage Anomaly":
        logging.warning(f"Voltage anomaly detected with {data['count']} consecutive occurrences!")
        send_alert_to_clients(data)

    elif data['type'] == "Efficiency Anomaly":
        logging.warning(f"Efficiency anomaly detected with {data['count']} consecutive occurrences!")
        send_alert_to_clients(data)

    elif data['type'] == "Power Imbalance Anomaly":
        logging.warning(f"Power imbalance anomaly detected with {data['count']} consecutive occurrences!")
        send_alert_to_clients(data)


# Function to send alerts to all connected clients
def send_alert_to_clients(alert_data):
    for client in clients:
        try:
            client.put(alert_data)
        except Exception as e:
            logging.error(f"Error sending alert to client: {e}")


# SSE endpoint for pushing alerts to the frontend
@app.route('/events')
def events():
    def generate():
        # This is a simple generator to push events to the frontend
        # It will yield data whenever an alert is sent
        queue = Queue()  # Create a queue to hold alerts
        clients.append(queue)
        try:
            while True:
                # Wait for an alert and send it to the client
                alert_data = queue.get()  # This will block until there is data
                yield f"data: {alert_data}\n\n"
        except Exception as e:
            logging.error(f"Error in SSE stream: {str(e)}")
        finally:
            clients.remove(queue)

    # Enable CORS explicitly for the /events endpoint
    response = Response(generate(), content_type='text/event-stream')
    # Allow the frontend (React) to access this route
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # Optional if using credentials
    return response


# Define API endpoint to receive alerts
@app.route('/alert', methods=['POST'])
def alert():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # If the data doesn't contain the expected fields, return an error
        if 'type' not in data or 'count' not in data or 'message' not in data:
            return jsonify({"status": "error", "message": "Invalid data received"}), 400

        # Handle the alert (custom action based on alert type)
        handle_alert(data)

        # Return a success message after processing the alert
        return jsonify({"status": "success", "message": "Alert received and processed!"}), 200

    except Exception as e:
        # Log the error if any occurs
        logging.error(f"Error processing the alert: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred"}), 500


# Start the Flask server on port 5000
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
