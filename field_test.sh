read -p "Choose filename " FILENAME
read -p "Choose interface " INTERFACE
read -p "Choose length in time " TIME

echo "Get out of the way!"

sleep 1 #Delay to get out of the way

echo "Starting Python data logger..."
# Use ./ to explicitly run the script from the current directory
python3 ./data_logger.py "$INTERFACE" "$FILENAME" "$TIME" &
PYTHON_PID=$! # Store the Process ID (PID) of the Python script

echo "Starting iperf3 client test..."
iperf3 -c 192.168.1.254 -u -b 0 -t "$TIME" -R --timestamps=%H:%M:%S --logfile data_logs/"$FILENAME".log &
IPERF_PID=$! # Store the Process ID (PID) of the iperf3 test

echo "Scripts started in parallel. PIDs: Python=${PYTHON_PID}, iperf3=${IPERF_PID}"

# --- Synchronization ---

# Wait for both background processes to finish
wait $PYTHON_PID
echo "Python logger finished."

wait $IPERF_PID
# Check the exit status of iperf3 for basic error handling
if [ $? -eq 0 ]; then
    echo "iperf3 test finished successfully."
else
    echo "⚠️ iperf3 test failed or encountered an error. Check server status (192.168.1.254)."
fi

echo "Done"
