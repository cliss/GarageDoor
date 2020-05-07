import RPi.GPIO as GPIO
import datetime
import signal
import socket
import struct
import sys
import time

# Set up Socket
multicastGroup = "224.1.1.1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Set up GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
DOOR_SENSOR_PIN = 18
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Prepare to clean up
def cleanUp(signal, frame):
    GPIO.cleanup()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, cleanUp)

# Logger
def log(message):
    print("{}> {}".format(datetime.datetime.now().strftime("%d-%m@%H:%M:%S"), message))

oldIsOpen = None
isOpen = None
lastPulse = datetime.datetime.now()

# Do the work
while True:
    oldIsOpen = isOpen
    isOpen = GPIO.input(DOOR_SENSOR_PIN)

    if (datetime.datetime.now() - lastPulse).seconds >= 60:
        lastPulse = datetime.datetime.now()
        log("Sending periodic update...")
        oldIsOpen = None

    if (isOpen and (isOpen != oldIsOpen)):
        log("Door is open")
        sock.sendto("open", (multicastGroup, 10000))
    elif (isOpen != oldIsOpen):
        log("Door is closed")
        sock.sendto("closed", (multicastGroup, 10000))
    time.sleep(0.1)
    
