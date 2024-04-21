from flask import Flask
from blueprints.routes import httpserver

app = Flask(__name__)
# This web server is the property of Sheldon J. Plankton, 
# please refrain from reading this secret source code.
# I WILL USE THIS ROUTER TO STEAL THE SECRET KRABBY PATTY FORMULA!
app.register_blueprint(httpserver, url_prefix='/')
