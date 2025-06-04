from libnetat import main
import time
import csv
import os
from datetime import datetime

log_time = datetime.now().isoformat()
csv_file = f"{log_time}_rssi_log.csv"
data_folder = "data_logs"

if not os.path.exists(os.path.join(os.getcwd(), data_folder)):
    os.makedirs(os.path.join(os.getcwd(), data_folder))

logs_path = os.path.join(os.getcwd(), data_folder, csv_file) 
with open(logs_path, "x", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "rssi"])

while True:
    try:
    	response = main("eth0", "AT+RSSI")
    	# Parse RSSI value
    	rssi_line = response.split("\n")[0]
    	if rssi_line:
            rssi_value = rssi_line.split(":")[1].strip()
            timestamp = datetime.now().isoformat()
            print(f"{timestamp}: RSSI = {rssi_value}")
            with open(csv_file, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, rssi_value])
        time.sleep(1)
    except KeyboardInterrupt:
	pass
