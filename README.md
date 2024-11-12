Anomaly Detection and Alerting System
Overview
This project implements a real-time anomaly detection and alerting system for power systems data. The system simulates the real-time collection of power system data, detects anomalies, and sends notifications through a Flask API to notify users of detected anomalies. The system uses machine learning techniques, such as Isolation Forest, to identify anomalies in various metrics, including voltage, power imbalance, efficiency, and frequency stability.

The project includes a simulation of data points, real-time anomaly detection, and a Flask server for sending and receiving anomaly alerts.

Features
Anomaly Detection: Uses Isolation Forest to detect anomalies in real-time power system data.
Real-time Data Simulation: Simulates data points for voltage, frequency, power, and other system parameters.
Visualization: Visualizes the system's behavior using matplotlib and seaborn, with animated plots to show real-time data trends.
Alert System: Sends API notifications (via POST requests) for anomalies like voltage fluctuations, efficiency issues, and power imbalance.
Flask API Server: A Flask server to handle anomaly alerts and stream events to the frontend via Server-Sent Events (SSE).
Cross-Origin Support: Enables a React frontend (on localhost:3000) to receive alerts from the backend using CORS.
Prerequisites
Python 3.7 or higher
Required Python packages:
pandas
numpy
matplotlib
sklearn
seaborn
flask
requests
flask-cors
Installation
Clone the repository or download the files.

bash
Copy code
git clone <repository-url>
cd <project-folder>
Create and activate a virtual environment.

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies.

bash
Copy code
pip install -r requirements.txt
Update the file path in the code to the location of your dataset:

python
Copy code
file_path = r"<path-to-your-dataset>.csv"
Usage
Step 1: Start the Flask server
Run the Flask server to handle alerts and SSE:

bash
Copy code
python app.py
The server will be accessible at http://localhost:5000.

Step 2: Visualize Data and Detect Anomalies
The system will simulate data, detect anomalies, and plot them in real-time. The detection thresholds for anomalies are set for voltage, efficiency, and power imbalance.

The system will send alerts for anomalies via POST requests to the Flask API, which can be processed for further actions.

Step 3: Frontend Integration
The server supports real-time alerts to the frontend through the /events endpoint using Server-Sent Events (SSE). For testing, you can build a React app or any frontend that listens to this stream.

Step 4: Anomaly Alerts
API Endpoint: /alert (POST)
Parameters:
type: Type of anomaly (e.g., "Voltage Anomaly", "Efficiency Anomaly")
count: Number of consecutive occurrences
message: Descriptive message of the anomaly
Example request:

json
Copy code
{
    "type": "Voltage Anomaly",
    "count": 5,
    "message": "Voltage anomaly detected with 5 consecutive occurrences!"
}
The Flask server will process the alert and log the details. You can add custom actions (such as email notifications) in the handle_alert function.

Files
app.py: Main file containing the Flask server, anomaly detection logic, and alert handling.
requirements.txt: List of Python dependencies.
May_2022.csv: Example dataset for power system parameters (please update with your actual dataset).
Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
