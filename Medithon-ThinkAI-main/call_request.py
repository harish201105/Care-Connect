import serial
import requests

# Setup the serial port (adjust the 'COM3' to your port or '/dev/ttyUSB0' for Linux)
serial_port = 'COM11'  # Replace with the correct serial port
baud_rate = 9600  # Set the baud rate (match with your Arduino settings)
url = "http://192.168.207.173:8080/post"  # Replace with your actual server URL

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_post_request():
    try:
        # Data to be sent in the POST request
        data = {"status": "button_clicked"}

        # Send POST request
        response = requests.post(url, json=data)

        # Log the response status and content
        if response.status_code == 200:
            print("POST request successful!")
            print(f"Response: {response.text}")
        else:
            print(f"Failed to send POST request. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

def listen_for_button():
    while True:
        # Read the serial data
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Read and decode serial input
            print(f"Received from Serial: {line}")

            # Check if the button was clicked (assuming "button_clicked" is sent by the Arduino)
            if line == "clicked":
                print("Button click detected! Sending POST request...")
                send_post_request()

if __name__ == "__main__":
    print("Listening for button clicks on the serial port...")
    listen_for_button()
