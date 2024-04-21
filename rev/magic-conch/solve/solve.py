from pwn import *

HOST = "127.0.0.1"
PORT = 32937


def XOR(x:bytes, y:bytes) -> bytes:
    assert len(x) == len(y)
    return bytes([x[i] ^ y[i] for i in range(len(x))])

target = b"A"*16
q1 = b"B"*16 + XOR(target, b"B"*16)
q2 = b"C"*16 + XOR(target, b"C"*16)



conn = remote(HOST, PORT)
print(conn.recvline().decode())
print(conn.recvuntil(b": ").decode())

# Query 1
conn.sendline(q1)
print(f"[SENT] {q1}")
print(conn.recvline().decode())

# Query 2
conn.sendline(q2)
print(f"[SENT] {q2}")
print(conn.recvline().decode())

print(conn.recvline().decode())