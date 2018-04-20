import sys
from Crypto.Cipher import AES

with open("key.bin", "rb") as f:
    key = f.read()

with open("iv.bin", "rb") as f:
    iv = f.read()

with open(sys.argv[1], "rb") as f:
    dat = f.read()

c = AES.new(key, AES.MODE_CBC, iv)
enc = c.encrypt(dat)

with open(sys.argv[2], "wb") as f:
    f.write(enc)
