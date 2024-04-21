import socket

s = socket.socket()
s.connect(("localhost", 8080))
for i in range(101):
    s.send(b"GET /click HTTP/1.1\r\nHost: localhost\r\n\r\n")
    print(s.recv(256))
s.send(b"GET /flag HTTP/1.1\r\nHost: localhost\r\n\r\n")
print(s.recv(256))
