p0 = int(input(("0" * 128 + "f" * 128) * 1 + "\n"), 16)
p1 = int(input(("0" * 64 + "f" * 64) * 2 + "\n"), 16)
p2 = int(input(("0" * 32 + "f" * 32) * 4 + "\n"), 16)
p3 = int(input(("0" * 16 + "f" * 16) * 8 + "\n"), 16)
p4 = int(input(("0" * 8 + "f" * 8) * 16 + "\n"), 16)
p5 = int(input(("0" * 4 + "f" * 4) * 32 + "\n"), 16)
p6 = int(input(("0" * 2 + "f" * 2) * 64 + "\n"), 16)
p7 = int(input("0f" * 128 + "\n"), 16)
p8 = int(input("33" * 128 + "\n"), 16)
p9 = int(input("55" * 128 + "\n"), 16)
p = [p9, p8, p7, p6, p5, p4, p3, p2, p1, p0]
all_bits = (1 << 1024) - 1
permutation = [0] * 1024
for i in range(1024):
    current = all_bits
    for shift in range(10):
        if ((i >> shift) & 1) == 0:
            current &= p[shift]
        else:
            current &= all_bits ^ p[shift]
    permutation[i] = len(bin(current)) - 3
cip = int(input("cipher text: \n"), 16)
plain = 0
for i in range(1024):
    plain ^= ((cip >> permutation[i]) & 1) << i
print(hex(plain))
print(plain.to_bytes(length=128, byteorder='big'))
