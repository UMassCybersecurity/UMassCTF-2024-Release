
class HTTPReq:
    def __init__(self, method, route, version, headers, body):
        self.method = method
        self.route = route
        self.version = version
        self.headers = headers
        self.body = body

    def get_raw_req(self):
        header_string = ""
        for key in self.headers.keys():
            header_string += f"{key}:{self.headers[key]}\r\n"
        return f"{self.method} {self.route} {self.version}\r\n" + header_string + f"\r\n{self.body}"

    def get_cookies(self):
        try:
            if "Cookie" in self.headers:
                cookies = {}
                for cookie in self.headers['Cookie'].split(';'):
                    key, val = cookie.split('=')
                    cookies[key] = val

                return cookies
        except:
            ""
        return None


class HTTPResp:
    def __init__(self, version, status_code, reason, headers, body):
        self.version = version
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.body = body

    def get_raw_resp(self):
        header_string = ""
        for key in self.headers.keys():
            header_string += f"{key}:{self.headers[key]}\r\n"
        return f"{self.version} {self.status_code} {self.reason}\r\n".encode() + header_string.encode() + b"\r\n" + self.body


class CashElement:
    def __init__(self):
        self.resps = {}
        self.spent = 0

    def set_resp(self, route, cached):
        self.resps[route] = cached

    def get_resp(self, route):
        return self.resps[route] if route in self.resps else None
