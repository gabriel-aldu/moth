from libnetat import main
import time

while True:
    response = main("eth0", "AT+RSSI")
    print(response)
    time.sleep(1)
    
"""
+RSSI:4
OK

"""
