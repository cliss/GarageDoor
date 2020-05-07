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
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Logger
def log(message):
    print("{}> {}".format(datetime.datetime.now().strftime("%d-%m@%H:%M:%S"), message))

# Prepare to clean up
def cleanUp(signal, frame):
    print ""
    log("Cleaning up...")
    GPIO.cleanup()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, cleanUp)

log("Waiting...")
while True:
    data, address = sock.recvfrom(1024)
    if data == "closed":
        log("Door is now closed; LED off.")
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)
        log("Door is now open; LED on.")
    sock.sendto('ack', address)
