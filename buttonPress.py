import serial
import time

try:
    ser = serial.Serial('/dev/cu.usbserial-210', 9600)
    time.sleep(2)

    while True:
        command = input("Enter command (H for ON, L for OFF, Q to quit): ").upper()
        if command == 'H' or command == 'L':
            ser.write(command.encode())
            response = ser.readline().decode().strip()
            print(f"Arduino says: {response}")
        elif command == 'Q':
            break
        else:
            print("Invalid command.")

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()