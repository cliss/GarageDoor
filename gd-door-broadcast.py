import socket
import struct
import RPi.GPIO as GPIO

# Set up socket
multicastGroup = "224.1.1.1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# TODO: Should this actually be pull up?
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        print("Waiting...")
        GPIO.wait_for_edge(24, GPIO.RISING)
        print("Door is now closed")
        sock.sendto("closed", (multicastGroup, 10000))
        
        GPIO.wait_for_edge(24, GPIO.FALLING)
        print("Door is now open")
        sock.sendto("open", (multicastGroup, 10000))
except (KeyboardInterrupt, SystemExit):
    print("")
    pass
finally:
    print("Cleaning up...")
    GPIO.cleanup()
    sock.close()

