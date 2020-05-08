from http.server import HTTPServer, BaseHTTPRequestHandler
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
DOOR_SENSOR_PIN = 18
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        if GPIO.input(DOOR_SENSOR_PIN):
            self.wfile.write(b'1')
        else:
            self.wfile.write(b'0')

httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
