import subprocess
import requests
import json
import time

# Define the osquery query
osquery_query = "SELECT * FROM users;"

# Define the API endpoint where you want to send the data
endpoint_url = "https://api.vistar.cloud/api/v1/computers/osquery_log_data/"

# Specify the interval (in seconds) between data sends (e.g., every 1 hour)
interval_seconds = 30  # 1 hour

while True:
    # Run the osquery command and capture the output
    try:
        osquery_output = subprocess.check_output(["C:/Program Files/osquery/osqueryd/osqueryi", "--json", osquery_query])
        osquery_data = json.loads(osquery_output.decode())
    except subprocess.CalledProcessError as e:
        print("Error running osquery:", e)
        osquery_data = []

    # Prepare the data to send (you may need to format it based on your endpoint requirements)
    data_to_send = {
        "query": osquery_query,
        "results": osquery_data
    }

    # Send the data to the endpoint using the requests library
    try:
        response = requests.post(endpoint_url, json=data_to_send)
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)

    # Sleep for the specified interval before the next run
    time.sleep(interval_seconds)
