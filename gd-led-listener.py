import datetime
import socket
import struct
import RPi.GPIO as GPIO

message = "Hello world!"
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

try:
    while True:
        print "Waiting..."
        data, address = sock.recvfrom(1024)
        print datetime.datetime.now(), "> ", data
        if data == "closed":
            GPIO.output(18, False)
        else:
            GPIO.output(18, True)
        sock.sendto('ack', address)
except (KeyboardInterrupt, SystemExit):
    print ""
    pass
finally:
    print("Cleaning up...")
    GPIO.cleanup()
