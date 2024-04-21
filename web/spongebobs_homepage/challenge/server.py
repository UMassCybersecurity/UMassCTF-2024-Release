import http.server
import socketserver
import urllib.parse
import subprocess
import os
import re
import base64

PORT = 1337

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """This class allows the server to handle requests in multiple threads."""
    daemon_threads = True  # Daemon threads will shut down on exit

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Route for the root `/`
        if self.path == '/':
            self.path = './files/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # Parse path and query
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Route for `/assets/image`
        if parsed_path.path == '/assets/image':
            # Extract the image name and size from the query parameters
            name = query_params.get('name', [None])[0]
            size = query_params.get('size', [None])[0]

            if name and size:
                
                if not name.isalnum():
                    self.send_error(400, "Invalid name parameter")
                    return
                
                if re.match(r'^\d+x\d+$', size):
                    # Split the string at 'x' to get both numbers
                    number1, number2 = map(int, size.split('x'))
                    
                    # Check if both numbers are less than 2000
                    if number1 >= 1000 or number2 >= 1000:
                        self.send_error(400, "Size too large, must be less than 1000x1000")
                        return

                image_path = f'./files/assets/{name}.png'
                if os.path.isfile(image_path):
                    # Run the ImageMagick convert command to resize the image
                    command = f"convert ./files/assets/{name}.png -resize {size}! png:-"
                    try:
                        # Execute the command using shell=True to make it vulnerable to injection
                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        output, errors = process.communicate()
                        if process.returncode == 0:
                            self.send_response(200)
                            self.send_header('Content-type', 'image/png')
                            self.end_headers()
                            self.wfile.write(output)
                            return
                        else:
                            self.send_error(500, f"Error resizing image: {errors.decode()}")
                            return
                    except Exception as e:
                        self.send_error(500, f"Internal server error: {str(e)}")
                        return
                else:
                    self.send_error(404, "Image not found")
                    return
            else:
                self.send_error(400, "Missing name or size parameters")
                return

        # Fallback to default file serving
        else:
            self.send_error(404, "File not found")
            return 

# Set up and start the server
with ThreadedHTTPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
