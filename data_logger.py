from libnetat import send_at_command
import time
import csv
import sys
import os
from datetime import datetime

def main(interface, filename, test_time):

    init_time = time.time()

    log_time = datetime.now().strftime("%H:%M:%S")
    csv_file = f"{filename}_rssi_log.csv"
    data_folder = "data_logs"

    if not os.path.exists(os.path.join(os.getcwd(), data_folder)):
        os.makedirs(os.path.join(os.getcwd(), data_folder))

    logs_path = os.path.join(os.getcwd(), data_folder, csv_file) 
    with open(logs_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "rssi"])

    rssi_data = []


    try:
        while True:
            response = send_at_command(interface, "AT+RSSI")
            if response != None:
                rssi_line = response.split("\n")[0]
                if rssi_line:
                    rssi_value = rssi_line.split(":")[1].strip()
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"{timestamp}: RSSI = {rssi_value}")
                    rssi_data.append([timestamp, rssi_value])
                    time.sleep(0.1)
            if time.time() - init_time >= test_time + 5:
                print("Saving data before exit...")
                with open(logs_path, "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(rssi_data)
                print("Data saved. Exiting.")
                return 0



    except (KeyboardInterrupt) as e:
        print("Saving data before exit...")
        with open(logs_path, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rssi_data)
        print("Data saved. Exiting.")
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 3:
        interface = sys.argv[1]
        filename = sys.argv[2]
        test_time = float(sys.argv[3])
        main(interface, filename, test_time)
