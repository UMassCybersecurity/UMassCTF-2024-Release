from flask import Flask, request, render_template, Blueprint,send_from_directory
from io import BytesIO
import pycurl 

httpserver = Blueprint('httpserver', __name__)

#@httpserver.route("/docs",methods=["GET"])
#def docs():
#   return """<!doctype html>
#    <h1>Router Docs</h1>
#
#    <h2>Websocket API</h2>
#
#    <strong>TODO: Document how to talk to 
#   Karen's customer service module in ../karen/customerservice.py
#   Also figure out how to use supervisord better.</strong>
#"""
#
# Securely CURL URLs, absolutely no bugs here!

@httpserver.route("/static/<path:path>")
def static(path):
    return send_from_directory('static',path)

@httpserver.route("/cURL",methods=["GET","POST"])
def curl():
    if(request.method == "GET"):
        return render_template('curl.html')
    elif(request.method == "POST"):
        try:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, request.json['URL'])
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            DATA = buffer.getvalue()
            return {"success":DATA.decode('utf-8')}
        except Exception as e:
            return {"error":str(e.with_traceback(None))}

@httpserver.route("/customerservice",methods=["GET"])
def customerservice():
    return render_template('customerservice.html')

NETWORK = [
    {'hostname':'patricks-rock','ports':[{'service':'http','num':80}]},
    {'hostname':'spongebobs-spatula','ports':[{'service':'http','num':80}]},
    {'hostname':'squidwards-clarinet','ports':[{'service':'http','num':80}]},

]
@httpserver.route("/dash",methods=["GET"])
def dash():
    return render_template('dashboard.html',network=NETWORK)

@httpserver.route("/")
def hello_world():
    return render_template("index.html")