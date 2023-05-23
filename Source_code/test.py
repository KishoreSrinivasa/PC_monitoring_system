from http.server import BaseHTTPRequestHandler, HTTPServer
from socket import gethostname, gethostbyname
from psutil import cpu_percent, disk_usage, virtual_memory, boot_time
from datetime import datetime
#import serial
import json

#ser = serial.Serial('COM5', 9600, timeout=1)
PORT = 8080


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the index.html file
            with open('index.html', 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
        elif self.path == '/system-info':
            # Return the system information as JSON
            hostname = gethostname()
            ip_address = gethostbyname(hostname)
            cpu = cpu_percent()
            disk = disk_usage('/')
            memory = virtual_memory()
            boot = datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            

            #if cpu>1.5:
             #   ser.write(b'r')

            data = {
                'hostname': hostname,
                'ip_address': ip_address,
                'cpu': cpu,
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'free': memory.free,
                    'percent': memory.percent
                },
                'boot': boot
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            

httpd = HTTPServer(('localhost', PORT), RequestHandler)
print(f'Serving on http://localhost:{PORT}')
httpd.serve_forever()
