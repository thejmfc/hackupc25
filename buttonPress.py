import serial
import subprocess
import skyscanner, gemini

groupcode = "test"

def run_script(script_name):

    try:
        print(f"Running {script_name}...")
        subprocess.run(["python3", script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def listen_to_arduino(port, baudrate=9600):

    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Listening for button press on {port} at {baudrate} baud...")

            while True:
                data = ser.readline().decode('utf-8').strip()

                if data == "BUTTON_PRESS":
                    print("Button press detected from Arduino!")
                    data = gemini.fetch_travel_recommendations(groupcode)

                    personal_data = data.get("original_data", {})
                    recommendations = data.get("recommendations", {})

                    if not recommendations or "outbound" not in recommendations or "inbound" not in recommendations:
                        raise ValueError(f"Invalid recommendations data: {recommendations}")

                    # Extract flight details
                    flight_details = []
                    for i in range(len(personal_data)):
                        print(personal_data)
                        # Validate input data
                        if "airport" not in personal_data[i]:
                            print(f"Error: Missing 'airport' in personal_data[{i}]")
                            continue

                        try:
                            flight_info = skyscanner.run(
                                personal_data[i].airport,
                                recommendations["outbound"],
                                recommendations["airport"],
                                recommendations["inbound"],
                                recommendations["locale"],
                                recommendations["home_currency"]
                            )
                            print("before flight info")
                            print(flight_info)
                            print("after flight info")
                            flight_details.append(flight_info)
                        except Exception as e:
                            print(f"Error fetching flight info for personal_data[{i}]: {e}")

                    # After the loop
                    if not flight_details:
                        flight_details.append({"error": "No flight details available at the moment."})

                    print("success")
                    print(recommendations)
                    print (flight_details)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    SERIAL_PORT = "/dev/cu.usbserial-210"
    BAUD_RATE = 9600             # Should match the baud rate set in your Arduino code

    listen_to_arduino(SERIAL_PORT, BAUD_RATE)