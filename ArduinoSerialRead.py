import os
import time
import serial
import serial.tools.list_ports

NUM_RETRIES = 10
PORT = 0
BAUD_RATE = 0
BAUD_RATE_SET = {50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200}
PORT_SET = set()


print("\033[46mSearching for ports...\033[m \n")

for retry in range(NUM_RETRIES):
    ports = serial.tools.list_ports.comports(include_links=False)
    if ports: break
    time.sleep(0.1)

if not ports: 
    print("\033[41mNo devices detected\033[m ")
    exit()

print("Available devices: ", end='')
for p in ports:
    print(f"{p.device}\t", end='')
    PORT_SET.add(p.device)
print()

# select port if multiple ports
if len(ports) == 1: PORT = ports[0].device
else:
    while (PORT == 0):
        q = input("Select port: ")
        PORT = q if q in PORT_SET else 0

# input baud rate
while (BAUD_RATE == 0):
    b = input("Select baud rate: ")
    BAUD_RATE = b if int(b) in BAUD_RATE_SET else 0

# attempt to connect to device with specified port and baud rate
for i in range(NUM_RETRIES):
    try:
        ser = serial.Serial(PORT, BAUD_RATE)
        if ser: break
    except:
        time.sleep(0.1)
# if fails, print error message
else: print(f"Could not connect to device at {PORT} using baud rate {BAUD_RATE}\n")

print("\n\033[42mDevice connected!\033[m")
print("Processing data...\n")
time.sleep(0.2)

for i in range(10):
    try:
        data = ser.readline().decode('utf-8').strip()
    except UnicodeDecodeError:
        data = ser.readline().decode('utf-8').strip()
    print(data)
print("...")




