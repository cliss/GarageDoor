#####################################
##         BOOTSTRAPPING           ##
#####################################

import datetime
import signal
import RPi.GPIO as GPIO
from paho.mqtt import client as mqttClient

broker = '192.168.17.200'
port = 1883
topic = "statusboard/garage"

LED_PIN = 18
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def log(message):
    print("{}> {}".format(datetime.datetime.now().strftime("%d-%b@%H:%M:%S"), message))

#####################################
##             SHUTDOWN            ##
#####################################
def cleanUp(signal, frame):
    log("Cleaning up...")
    GPIO.cleanup()
    sys.exit(0)

#####################################
##          MQTT CLIENT            ##
#####################################

def connectMqtt(): 
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log("Connected to broker {}".format(broker))
        else:
            log("Failed to connect; return code {}".format(rc))

    client = mqttClient.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        log("Received `{}` from `{}` topic".format(msg.payload.decode(), msg.topic))
        if msg.payload.decode() == "1":
            # Garage is open
            GPIO.output(LED_PIN, True)
        else: 
            # Garage is closed
            GPIO.output(LED_PIN, False)
    
    client.subscribe(topic)
    client.on_message = on_message


#####################################
##             ENTRY               ##
#####################################

def run():
    # Start MQTT client
    client = connectMqtt()
    subscribe(client)
    client.loop_forever()
    
signal.signal(signal.SIGINT, cleanUp)

if __name__ == '__main__':
    log("Starting garage LED listener...")
    run()
    
