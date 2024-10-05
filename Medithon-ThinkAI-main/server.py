import socket
from fastapi import FastAPI
from twilio.rest import Client

app = FastAPI()

# Twilio setup
account_sid = 'AC3edf1e6a7837d91840397346c11fde0c'
auth_token = 'e161376415d8f593cd837f63b06a700b'
client = Client(account_sid, auth_token)
twilio_number = '+19566254382'
to_number = '+919042264608'

# Get the local IP address of the server
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

local_ip = get_local_ip()

@app.post("/post")
def trigger_emergency():
    location_link = "https://maps.app.goo.gl/opEMh2nXLXN2Ankz6?g_st=ic"
    message_body = f"Your patient is in emergency. Track their location here: {location_link}"

    # Perform the SMS and Call in one operation
    try:
        # Make emergency call
        call = client.calls.create(
            twiml='<Response><Say>Your patient has initiated an emergency alert. Please check on them.</Say></Response>',
            to=to_number,
            from_=twilio_number
        )
        print(f"Call initiated: {call.sid}")

        # Send emergency SMS
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=to_number
        )
        print(f"SMS sent: {message.sid}")

        # Write to the emergency alert file
        with open("emergency_alert.txt", "w") as file:
            file.write("Emergency Alert: User is in a danger zone!\n")

        return {
            "status": "success",
            "call_sid": call.sid,
            "sms_sid": message.sid
        }
    except Exception as e:
        print(e)
        return {"status": "error", "message": str(e)}


# To run the server and expose it on the local network
if __name__ == "__main__":
    import uvicorn
    print(f"Serving at http://{local_ip}:8080")
    uvicorn.run(app, host=local_ip, port=8080)
