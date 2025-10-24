import serial
import csv
import time

x = 1

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace 'COM4' with your serial port and 9600 with your baud rate
time.sleep(2)  # Allow time for the serial connection to establish


with open(f'ExperimentA_{x}.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Time" , "Temperature"])

        while True:
            #time.sleep(0.3)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                # Assuming your serial data is comma-separated (e.g., "value1,value2")
                data = line.split(',')
                csv_writer.writerow([time.strftime("%M:%S")] + data)
                csvfile.flush() # Ensure data is written to disk immediately
