from http.server import HTTPServer, BaseHTTPRequestHandler
import RPi.GPIO as GPIO
import signal
import sys
import time

# Set up GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
DOOR_SENSOR_PIN = 18
DOOR_RELAY_PIN = 4
PORT_NUMBER = 8000
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOOR_RELAY_PIN, GPIO.OUT)

def toggle():
    GPIO.output(DOOR_RELAY_PIN, False)
    time.sleep(1)
    GPIO.output(DOOR_RELAY_PIN, True)

def open():
    if GPIO.input(DOOR_SENSOR_PIN):
        print("Door is already open")
        return
    toggle()

def close():
    if GPIO.input(DOOR_SENSOR_PIN) == False:
        print("Door is already closed")
        return
    toggle()

def noop():
    pass

def cleanUp(signal, frame):
    print("")
    print(f"Ensuring pin {DOOR_RELAY_PIN} is set high...")
    GPIO.output(DOOR_RELAY_PIN, True)
    print("Cleaning up...")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, cleanUp)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Received request")
        self.send_response(200)
        self.end_headers()
        message = "The path is {}".format(self.path)
        action = noop
        if self.path == "/open":
            print("Opening the door...")
            message = "1"
            action = open
        elif self.path == "/close":
            print("Closing the door...")
            message = "1"
            action = close
        elif self.path == "/state-inverse":
            if GPIO.input(DOOR_SENSOR_PIN):
                # Door is open
                message = "1"
            else:
                # Door is closed
                message = "0"
        elif self.path == "/state":
            if GPIO.input(DOOR_SENSOR_PIN):
                # Door is open
                message = "0"
            else:
                # Door is closed
                message = "1"
    
        self.wfile.write(bytes(message, "utf-8"))
        action()

print(f"Turning on pin {DOOR_RELAY_PIN} to ensure relay is off...")
GPIO.output(DOOR_RELAY_PIN, True)
print(f"Creating server on port {PORT_NUMBER}...")
httpd = HTTPServer(('', PORT_NUMBER), SimpleHTTPRequestHandler)
print("Serving...")
httpd.serve_forever()
