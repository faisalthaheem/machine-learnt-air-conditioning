/***************************************************
  Adafruit MQTT Library ESP8266 Example

  Must use ESP8266 Arduino from:
    https://github.com/esp8266/Arduino

  Works great with Adafruit's Huzzah ESP board & Feather
  ----> https://www.adafruit.com/product/2471
  ----> https://www.adafruit.com/products/2821

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Tony DiCola for Adafruit Industries.
  MIT license, all text above must be included in any redistribution
 ****************************************************/
#include <ESP8266WiFi.h>
//#include "Adafruit_MQTT.h"
//#include "Adafruit_MQTT_Client.h"
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <PubSubClient.h>

IRsend irsend(2);
/************************* WiFi Access Point *********************************/

#define WLAN_SSID       ""
#define WLAN_PASS       ""

/************************* Adafruit.io Setup *********************************/

#define AIO_SERVER      "192.168.100.100"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    ""
#define AIO_KEY         ""

/************ Global State (you don't need to change this!) ******************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// or... use WiFiFlientSecure for SSL
//WiFiClientSecure client;

PubSubClient mqClient(client);

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
//Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

/****************************** Feeds ***************************************/

// Setup a feed called 'onoff' for subscribing to changes.
//Adafruit_MQTT_Subscribe lounge_ac = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/lounge/ac/commands");

/*************************** Sketch Code ************************************/

void reconnect() {
  // Loop until we're reconnected
  while (!mqClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqClient.connect("lounge_ac_commands")) {
      Serial.println("connected");
      mqClient.subscribe("/lounge/ac/commands");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
    yield();
  }
}

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();

void setup() {
  Serial.begin(115200);
  delay(10);

  irsend.begin();
  yield();
  irsend.calibrate();

  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  mqClient.setServer("192.168.100.100", 1883);
  mqClient.setCallback(callback);
}

uint32_t x=0;
const size_t irBufferSize = 512;
uint16_t irBuffer[irBufferSize];

void loop() {

  if (!mqClient.connected()) {
    reconnect();
  }
  mqClient.loop();

  yield();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  processCommand((char*)payload, length);
}


//int khz = 38; // 38kHz carrier frequency for the NEC protocol

void processCommand(char *buffer, unsigned int len){

  //convert the string to ints
  //https://arduino.stackexchange.com/questions/44996/string-to-int-array
  char *tok = strtok(buffer, ",");
  size_t index = 0;

  memset(irBuffer,0,sizeof(irBufferSize));
  //char* pointer;
  
  while (tok != nullptr && index < irBufferSize) {
    //irBuffer[index++] = strtoul(tok, &pointer, 10);
    irBuffer[index++] = atoi(tok);
    tok = strtok(NULL, ",");
  }
  //let wdt do it's job
  yield();

  Serial.print("Sending command...");
  irsend.sendRaw(irBuffer, index, 38);
  Serial.printf("[%d] tokens sent.\n",index);
  
}
