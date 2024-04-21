import asyncio, os, re
from websockets.server import serve

# Due to security concerns, I, Sheldon J. Plankton have ensured this module
# has no access to any internet service other than those that are
# trusted. This agent will trick Krabs into sending me the secret
# krabby patty formula which I will log into Karen's secret krabby patty 
# secret formula file! First, I have to fix a few security bugs!
class KarenCustomerServiceAgent:
    SECRET_KEY = bytearray(b"\xe1\x86\xb2\xa0_\x83B\xad\xd7\xaf\x87f\x1e\xb4\xcc\xbf...i will have the secret krabby patty formula.")
    Dialogue = {
        "Welcome":"Hello! Welcome to the Future Router service bot!",
        "Secret formula":"Thank you for your input, we will process your request in 1-3 business days",
        "Problem":"Are you having an issue? Please enter the secret krabby patty formula in the dialogue box to continue"
    }
    def handle_input(self,message):
        if ("hello" in message):
            return self.Dialogue["Welcome"]
        elif("krabby patty" in message):
            filtered_message = re.sub(r"(\"|\'|\;|\&|\|)","",message)
            os.system(f'echo "{filtered_message}\n" >> /dev/null')
            return self.Dialogue["Secret formula"]
        elif("problem" in message):
            return self.Dialogue["Problem"]
        else:
            return "I could not understand your message, this agent is under construction. Please use the other implemented features for now!"
    def xor_decrypt(self,ciphertext):
        plaintext = ""
        cipher_arr = bytearray(ciphertext)
        for i in range(0,len(cipher_arr)):
            plaintext += chr(cipher_arr[i] ^ self.SECRET_KEY[i % len(self.SECRET_KEY)])
        return plaintext

KarenAgent = KarenCustomerServiceAgent()

async def respond(websocket):
    async for message in websocket:
        data = KarenAgent.xor_decrypt(message.encode('latin-1'))
        response = KarenAgent.handle_input(data)
        await websocket.send(response)

async def main():
    async with serve(respond, "0.0.0.0", 9000):
        await asyncio.Future()  # run forever

asyncio.run(main())