import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from matplotlib.animation import FuncAnimation
import seaborn as sns
import itertools
import requests  # Import requests for API call
from flask import Flask, request, jsonify

# Load your dataset (assuming you're working with a CSV file, but can be adjusted for Excel)
file_path = r"C:\Users\HP\Downloads\archive\May_2022.csv"  # Update with your actual file path
df = pd.read_csv(file_path)

# Columns for anomaly detection
columns_to_use = ['PVPCS_Active_Power', 'Receiving_Point_AC_Voltage', 'MG-LV-MSB_Frequency',
                  'Island_mode_MCCB_AC_Voltage', 'Outlet_Temperature']

# Feature extraction and scaling
X = df[columns_to_use]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit Isolation Forest model
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(X_scaled)

# Define API endpoint for anomaly notification
ANOMALY_ALERT_URL = "http://localhost:5000/alert"  # Local server for testing

# Function to send API alert for anomalies
def send_anomaly_alert(anomaly_type, anomaly_count):
    try:
        payload = {
            "type": anomaly_type,
            "count": anomaly_count,
            "message": f"Anomaly detected: {anomaly_type} with {anomaly_count} consecutive occurrences."
        }
        response = requests.post(ANOMALY_ALERT_URL, json=payload)
        if response.status_code == 200:
            print(f"Alert sent successfully for {anomaly_type}!")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")

# Real-time data simulation
def get_real_time_data():
    voltage = np.random.uniform(210, 240)
    frequency = np.random.uniform(48.8, 51.2)
    power = np.random.uniform(0, 100)
    island_voltage = np.random.uniform(210, 240)
    outlet_temp = np.random.uniform(27, 31)
    input_power = np.random.uniform(100, 150)
    return voltage, frequency, power, island_voltage, outlet_temp, input_power

# Visualization and real-time anomaly detection
def visualize_simulation():
    sns.set(style="whitegrid")

    # Data lists
    time_steps = []
    voltage_vals, frequency_vals = [], []
    power_vals, island_voltage_vals = [], []
    outlet_temp_vals = []
    power_imbalance_vals, efficiency_ratios = [], []
    voltage_diff_vals, frequency_stability_vals = [], []

    # Anomaly counters
    voltage_anomaly_counter = frequency_anomaly_counter = 0
    efficiency_anomaly_counter = imbalance_anomaly_counter = 0
    consecutive_anomaly_threshold = 3  # Number of consecutive anomalies to trigger alert

    # Max data points on plot
    max_data_points = 50
    fig, axs = plt.subplots(6, 1, figsize=(14, 22))

    # Update function for animation
    def update_plot(frame):
        nonlocal voltage_anomaly_counter, efficiency_anomaly_counter, imbalance_anomaly_counter

        # Fetch real-time data
        voltage, frequency, power, island_voltage, outlet_temp, input_power = get_real_time_data()
        power_imbalance = input_power - power
        efficiency_ratio = power / input_power if input_power != 0 else 0
        voltage_diff = abs(voltage - island_voltage)
        frequency_stability = np.std(frequency_vals[-10:]) if len(frequency_vals) >= 10 else 0

        # Store real-time data
        time_steps.append(frame)
        voltage_vals.append(voltage)
        frequency_vals.append(frequency)
        power_vals.append(power)
        island_voltage_vals.append(island_voltage)
        outlet_temp_vals.append(outlet_temp)
        power_imbalance_vals.append(power_imbalance)
        efficiency_ratios.append(efficiency_ratio)
        voltage_diff_vals.append(voltage_diff)
        frequency_stability_vals.append(frequency_stability)

        # Limit data points on the plot
        if len(time_steps) > max_data_points:
            time_steps.pop(0)
            voltage_vals.pop(0)
            frequency_vals.pop(0)
            power_vals.pop(0)
            island_voltage_vals.pop(0)
            outlet_temp_vals.pop(0)
            power_imbalance_vals.pop(0)
            efficiency_ratios.pop(0)
            voltage_diff_vals.pop(0)
            frequency_stability_vals.pop(0)

        # Detect anomalies
        voltage_anomaly = voltage < 206 or voltage > 236
        efficiency_anomaly = efficiency_ratio < 0.7 or efficiency_ratio > 1
        imbalance_anomaly = abs(power_imbalance) > 50

        # Update counters
        if voltage_anomaly:
            voltage_anomaly_counter += 1
        else:
            voltage_anomaly_counter = 0

        if efficiency_anomaly:
            efficiency_anomaly_counter += 1
        else:
            efficiency_anomaly_counter = 0

        if imbalance_anomaly:
            imbalance_anomaly_counter += 1
        else:
            imbalance_anomaly_counter = 0

        # Send API alert if consecutive anomalies exceed threshold
        if voltage_anomaly_counter >= consecutive_anomaly_threshold:
            send_anomaly_alert("Voltage Anomaly", voltage_anomaly_counter)
            voltage_anomaly_counter = 0

        if efficiency_anomaly_counter >= consecutive_anomaly_threshold:
            send_anomaly_alert("Efficiency Anomaly", efficiency_anomaly_counter)
            efficiency_anomaly_counter = 0

        if imbalance_anomaly_counter >= consecutive_anomaly_threshold:
            send_anomaly_alert("Power Imbalance Anomaly", imbalance_anomaly_counter)
            imbalance_anomaly_counter = 0

        # Plot updates
        axs[0].cla()
        axs[0].plot(time_steps, voltage_vals, color="blue")
        axs[0].set_title(f"Voltage - Anomalies Sent")

        axs[1].cla()
        axs[1].plot(time_steps, power_imbalance_vals, color="purple")
        axs[1].set_title("Power Imbalance")

        axs[2].cla()
        axs[2].plot(time_steps, efficiency_ratios, color="green")
        axs[2].set_title("Efficiency Ratios")

        axs[3].cla()
        axs[3].plot(time_steps, voltage_diff_vals, color="orange")
        axs[3].set_title("Voltage Difference")

        axs[4].cla()
        axs[4].plot(time_steps, frequency_stability_vals, color="red")
        axs[4].set_title("Frequency Stability")

        axs[5].cla()
        axs[5].plot(time_steps, outlet_temp_vals, color="black")
        axs[5].set_title("Outlet Temperature")

        plt.tight_layout()

    anim = FuncAnimation(fig, update_plot, frames=itertools.count(), interval=500, repeat=False)
    plt.show()

# Start the simulation
visualize_simulation()

# Flask server to handle anomaly alerts
app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    print("Received Anomaly Alert:")
    print(f"Type: {data['type']}, Count: {data['count']}, Message: {data['message']}")
    return jsonify({"status": "success", "message": "Alert received!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)