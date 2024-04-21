import base64

input = "AzE9Omd0eG8XHhEcHTx1Nz0dN2MjfzF2MDYdICE6fyMa"
XOR_string = b"SPONGEBOBSPONGEBOBSPONGEBOBSPONGEBOBSPONGEBOB"
a = base64.b64decode(input)
flag_part_1 = b''
for i in range(len(a)):
    flag_part_1 += (a[i] ^ XOR_string[i % len(XOR_string)]).to_bytes()
print(flag_part_1)
