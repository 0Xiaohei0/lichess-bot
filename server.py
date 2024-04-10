from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import threading
import time

COMMUNICATIONFILENAME = "communication.json"
DEFAULT_COMMUNICATIONFILENAME = "communication_default.json"
ENGINE_LOG_FILENAME = "log.txt"

MOVE_READY = "move_ready"

# opponent data
OPPONENT_NAME = "opponent_name"
JOINED = "joined"

SIDE = "side"

CURRENT_SIDE = "current_side"

running = False
class RequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        #print(f"Received API POST request {self.path}")
        if self.path == '/make_move':
            self.handle_make_move()
        elif self.path == '/start_game':
            self.handle_start_game()
        else:
            self.handle_not_found()
            return
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        #print(f"Received API GET request {self.path}")
        if self.path == '/engine_log':
            self.handle_engine_log()
        elif self.path == '/game_state':
            self.handle_game_state()
        else:
            self.handle_not_found()
            return
        
    def handle_make_move(self):
        update_communication(MOVE_READY, True)
        
    def handle_start_game(self):
        global running
        if(not running):
            script_thread = threading.Thread(target=self.run_chess_bot)
            script_thread.start()
            running = True
        else:
            print(f"lichess-bot.py is already running")
            
    def handle_game_state(self):
        self.send_response(200)  # Move the response initiation here
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        try:
            with open(COMMUNICATIONFILENAME, 'r', encoding='utf-8') as file:
                data = file.read()
                self.wfile.write(data.encode('utf-8'))  # Write the file content to the response
        except FileNotFoundError:
            self.wfile.write('Engine log file not found.'.encode('utf-8'))
                
    def handle_engine_log(self):
        self.send_response(200)  # Move the response initiation here
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        try:
            with open(ENGINE_LOG_FILENAME, 'r', encoding='utf-8') as file:
                data = file.read()
                self.wfile.write(data.encode('utf-8'))  # Write the file content to the response
        except FileNotFoundError:
            self.wfile.write('Engine log file not found.'.encode('utf-8'))
        
    def handle_not_found(self):
        print(f"Request path {self.path} not found")
        self.send_response(400)
        self.end_headers()
    
        
    def run_chess_bot(self):
        # Replace 'path/to/your_script.py' with the actual path to your script
        subprocess.run(['python', './lichess-bot.py'])
        

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting HTTP server")
    httpd.serve_forever()

def reset_communication():
    with open(DEFAULT_COMMUNICATIONFILENAME, 'r', encoding='utf-8') as default:
        data = json.load(default)
    with open(COMMUNICATIONFILENAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        
def check_communication():
    with open(COMMUNICATIONFILENAME, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    
def set_communication(data):
    with open(COMMUNICATIONFILENAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)  
        return data

def update_communication(key, value):
    data = check_communication() 
    data[key] = value 
    set_communication(data) 
    
if __name__ == "__main__":
    reset_communication()
    run_server()