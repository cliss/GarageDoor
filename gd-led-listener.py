import datetime
import signal
import socket
import struct
import sys
import RPi.GPIO as GPIO

multicastGroup = '224.1.1.1'
serverAddress = ('', 10000)

# Set up socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(serverAddress)
group = socket.inet_aton(multicastGroup)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Set up IO
DOOR_SENSOR_PIN = 18
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.OUT)

# Logger
def log(message):
    print("{}> {}".format(datetime.datetime.now().strftime("%d-%b@%H:%M:%S"), message))

# Prepare to clean up
def cleanUp(signal, frame):
    print ""
    log("Cleaning up...")
    GPIO.cleanup()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, cleanUp)

log("Using pin {}. Waiting for multicast messages...".format(DOOR_SENSOR_PIN))
while True:
    data, address = sock.recvfrom(1024)
    if data == "closed":
        log("Door is now closed; LED off.")
        GPIO.output(DOOR_SENSOR_PIN, False)
    else:
        GPIO.output(DOOR_SENSOR_PIN, True)
        log("Door is now open; LED on.")
    try:
        sock.sendto('ack', address)
    except:
        print("ERROR: Could not send acknowledgement packet.")
