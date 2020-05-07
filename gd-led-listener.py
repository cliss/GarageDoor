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

# Prepare to clean up
def cleanUp(signal, frame):
    print ""
    GPIO.cleanup()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, cleanUp)

while True:
    print "Waiting..."
    data, address = sock.recvfrom(1024)
    print datetime.datetime.now(), "> ", data
    if data == "closed":
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)
    sock.sendto('ack', address)
