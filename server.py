from http.server import HTTPServer, BaseHTTPRequestHandler
import json

COMMUNICATIONFILENAME = "communication.json"
MOVE_READY = "move_ready"

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Signal that a request has been received
        print("Received API request")
        self.send_response(200)
        self.end_headers()
        update_communication(MOVE_READY, True)
        

def run_server():
    server_address = ('', 8000)  # Listen on all interfaces, port 8000
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting HTTP server")
    httpd.serve_forever()

def check_communication():
    with open(COMMUNICATIONFILENAME, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    
def set_communication(data):
    with open(COMMUNICATIONFILENAME, 'w', encoding='utf-8') as file:
        json.dump(data, file)  
        return data

def update_communication(key, value):
    data = check_communication() 
    data[key] = value 
    set_communication(data) 