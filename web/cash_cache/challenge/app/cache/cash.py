import socketserver
import socket
import redis
import os
import pickle
import base64
from cash_classes import *

REDIS_CLIENT = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=6379,
    charset="utf-8",
    decode_responses=True
)

def log(msg):
    print(msg,flush=True)


# The CASH a customer must spend before they can make a new request
# HTTP requests don't grow on trees!
MINIMUM_CASH = 10000000.0

def parseCash(stream_text):
    spent = 0
    body = ""
    while (spent < MINIMUM_CASH):
        cur, _, stream_text = stream_text.partition("\r\n")
        amount, units = cur.split(' ')
        if (units == "DOLLARS"):
            amount = float(amount)
        elif (units == "CENTS"):
            amount = float(amount)/100
        else:
            raise Exception("I can't understand the units!")
        # Dear Reader,
        #   I wrote this Ternary Operator today because I learned it
        #   in boating school. For some reason it sometimes cuts off
        #   the end of requests. But it probably is not a big deal.
        # From,
        # Patrick Star
        index = round(amount) if amount <= len(
            stream_text) else len(stream_text) - len(cur)
        cur = stream_text[:index]
        stream_text = stream_text[index:]
        if (len(cur) < amount or amount < 0):
            raise Exception("Are you trying to steal from me?")
        spent += amount
        body += cur
    return body, stream_text, spent


def parseHTTPReq(text):
    try:
        Requests = []
        stream_text = text.decode()
        spent = 0
        while (stream_text):
            cur, _, stream_text = stream_text.partition("\r\n")
            method, route, version = cur.split(' ')
            Headers = {}
            while (True):
                cur, _, stream_text = stream_text.partition("\r\n")
                if (cur == ''):
                    break
                key, _, val = cur.partition(':')
                Headers[key] = val.replace(' ', '')
            if ("Cash-Encoding" in Headers and Headers["Cash-Encoding"] == "Money!"):
                body, stream_text, spent = parseCash(stream_text)
            else:
                body = stream_text
                stream_text = ""
            Headers['Content-Length'] = len(body)
            req = HTTPReq(method, route, version, Headers, body)
            Requests.append(req)
        return Requests, spent
    except Exception as e:
        log(e)
        return None, None


def parseHTTPResp(raw_req):
    try:
        stream_text = raw_req
        cur, sep, stream_text = stream_text.partition(b"\r\n")
        cur = cur.decode()
        version, _, cur = cur.partition(' ')
        status_code, _, cur = cur.partition(' ')
        reason = cur
        Headers = {}
        while (True):
            cur, _, stream_text = stream_text.partition(b"\r\n")
            if (cur == b''):
                break
            cur = cur.decode()
            key, _, val = cur.partition(':')
            Headers[key] = val.replace(' ', '')
        body = stream_text
        Headers['Content-Length'] = len(body)
        req = HTTPResp(version, status_code, reason, Headers, body)
        return req
    except Exception as e:
        log(e)
        return None


class CashTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096).strip()
        http_reqs, spent = parseHTTPReq(self.data)

        if (http_reqs is None):
            data = 'ARGHHHH this request be badly formed!'
            self.request.send(
                f"HTTP/1.1 400 Bad Request\r\nConnection:close\r\nContent-Type: text/html\r\nContent-Length: {len(data)}\r\n\r\n{data}".encode())
        else:
            RESP = b""
            for request in http_reqs:
                cookies = request.get_cookies()
                if (cookies and 'uid' in cookies and REDIS_CLIENT.exists(cookies['uid'])):
                    cash_elem = pickle.loads(base64.b64decode(
                        REDIS_CLIENT.get(cookies['uid'])))
                    cached = cash_elem.get_resp(request.route)
                    if (cached):
                        cached.headers['X-Cache-Hit'] = "HIT!"
                        cached.headers['X-CashSpent'] = cash_elem.spent
                        cached.headers['X-CachedRoutes'] = len(cash_elem.resps)
                        RESP += cached.get_raw_resp()
                        continue
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(("localhost", 3000))
                raw_req = request.get_raw_req()
                sock.sendall(raw_req.encode())
                raw_data = sock.recv(4096)
                while (raw_data != b''):
                    RESP += raw_data
                    raw_data = sock.recv(4096)
                sock.close()
            resp = parseHTTPResp(RESP)
            
            if ("X-Cache-UID" in resp.headers and "X-Cache-Hit" not in resp.headers):
                resp.headers['X-Cache-Hit'] = "MISSED!"
                UID = resp.headers['X-Cache-UID']
                if (REDIS_CLIENT.exists(UID)):
                    cash_elem = pickle.loads(
                        base64.b64decode(REDIS_CLIENT.get(UID)))
                    cash_elem.spent += spent
                    cash_elem.set_resp(request.route, resp)
                    REDIS_CLIENT.set(UID, base64.b64encode(
                        pickle.dumps(cash_elem)))
                else:
                    cash_elem = CashElement()
                    cash_elem.spent += spent
                    cash_elem.set_resp(request.route, resp)
                    REDIS_CLIENT.set(UID, base64.b64encode(
                        pickle.dumps(cash_elem)))
                resp.headers['X-CashSpent'] = cash_elem.spent
                resp.headers['X-CachedRoutes'] = len(cash_elem.resps)
            self.request.send(resp.get_raw_resp())


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9000

    with socketserver.ForkingTCPServer((HOST, PORT), CashTCPHandler) as server:
        server.serve_forever()
