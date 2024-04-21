
"""
A script for helping in the build process.

- We need to place a large hex string into the loader.c source file, so
this script performs textual replacement on the string !COPY_PAYLOAD_HERE!

- The decryption key and IV are kept in the source file, so this program
also obfuscates them by XORing with the 16-byte string "C++ IS GARBAGE!!"
"""



KEY = b"YELLOW SUBMARINE"
IV = b"*CHICKEN NUGGET*"
MASK = b"C++ IS GARBAGE!!"

def XOR(x:bytes, y:bytes) -> str:
    assert len(x) == len(y)
    res = bytes([x[i] ^ y[i] for i in range(len(x))])

    # Escape the result so it's a valid C string
    encoded_string = ''.join([rf'\x{char:02x}' for char in res])
    return encoded_string


# Read encrypted payload
payload = ""
with open("../build/payload.txt", "r") as fd:
    payload = fd.read()

if len(payload) == 0:
    raise ValueError("payload.txt contains no data")


# Read in C source
code = ""
with open("loader_base.c", "r+") as fd:
    code = fd.read()

# Perform replacement
with open("../build/loader_final.c", "w") as fd:
    code = code.replace("!COPY_PAYLOAD_HERE!", payload)
    code = code.replace("!COPY_KEY_HERE!", XOR(KEY, MASK))
    code = code.replace("!COPY_IV_HERE!", XOR(IV, MASK))
    fd.seek(0)
    fd.write(code)
    fd.close()