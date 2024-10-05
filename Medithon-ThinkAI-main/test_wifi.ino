#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Replace these with your network credentials
const char* ssid = "POCO X6 5G";       // SSID (Wi-Fi network name)
const char* password = "Sakthi@2005";   // Password

const char* serverIP = "http://192.168.216.227:8080/post";  // Replace with the IP address you want to send the POST request to

const int buttonPin = 2; // GPIO2 corresponds to D4
bool buttonState = HIGH;  // Initial button state
bool lastButtonState = HIGH;  // Last button state

WiFiClient client;
HTTPClient http;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Set button pin as input (using internal pull-up)
  pinMode(buttonPin, INPUT_PULLUP);

  // Connect to Wi-Fi
  connectToWiFi();
}

void loop() {
  // Read the button state
  int reading = digitalRead(buttonPin);

  // Detect if the button was pressed and then released (HIGH -> LOW -> HIGH)
  if (lastButtonState == HIGH && reading == LOW) {
    // Button was pressed (transition from HIGH to LOW)
    Serial.println("Button pressed...");
  }
  
  if (lastButtonState == LOW && reading == HIGH) {
    // Button was released (transition from LOW to HIGH)
    Serial.println("Button released, sending POST request.");
    sendPostRequest();  // Send the POST request
  }

  // Save the current state as the last state for the next loop
  lastButtonState = reading;
}

void connectToWiFi() {
  // Begin Wi-Fi connection
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Wait for the connection to be established
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  // Connected to Wi-Fi
  Serial.println();
  Serial.println("WiFi connected.");
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
}

void sendPostRequest() {
  // Check if connected to Wi-Fi
  if (WiFi.status() == WL_CONNECTED) {
    // Start the HTTP client
    http.begin(client, serverIP);  // Specify the destination for POST request
    http.addHeader("Content-Type", "application/json");  // Set the content type to JSON

    // Example JSON payload
    String payload = "{\"status\":\"button_clicked\"}";

    // Send POST request
    int httpResponseCode = http.POST(payload);  

    // Check and print the response
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    // End the HTTP request
    http.end();  
  } else {
    Serial.println("Not connected to Wi-Fi");
  }
}
