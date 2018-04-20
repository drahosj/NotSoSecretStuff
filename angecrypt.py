import zlib
import sys
import binascii
from Crypto.Cipher import AES

with open("tmp/secdsm_secret_image_2.png", "rb") as f:
    t = f.read()

with open("outer_image.png", "rb") as f:
    s = f.read()

with open("key.bin", "rb") as kf:
    key = kf.read()

zeros = binascii.unhexlify("00000000000000000000000000000000")

original_magic = t[0:8]

s = s + ((16 - len(s) % 16) * b"\x00")

# Get rid of magic
t = t[8:]

c = AES.new(key, AES.MODE_ECB)
enc_s = c.encrypt(s)
pad = zeros * 2
wrap_size = len(enc_s) + len(pad) - 16

# Can't do wrapper because of pesky PNG spec saying IHDR must
# be first

# Prepare c0 (PNG magic and beginning of wrapper)
# Add the wrapper (nonsense chunk of length len(s + pad))
c0 = original_magic[0:8] + bytes([
        (wrap_size >> 24) & 0xff,
        (wrap_size >> 16) & 0xff,
        (wrap_size >> 8) & 0xff,
        wrap_size & 0xff
])
# Begin wrapper block
c0 = c0 + b"sdSm"

#c0 = b"Very close now.."

# Get magic IV
c0_dec = c.decrypt(c0)
new_iv = bytearray(16)
for i in range(len(c0_dec)):
    new_iv[i] = s[i] ^ c0_dec[i]
iv = bytes(new_iv)

# Actually encrypt S now, with the right IV
c = AES.new(key, AES.MODE_CBC, iv)
enc_s = c.encrypt(s)

# Prepend checksum (of wrapper) to remainder of t
csum = zlib.crc32(enc_s[12:] + pad)
checksum = bytes([
        (csum >> 24) & 0xff,
        (csum >> 16) & 0xff,
        (csum >> 8) & 0xff,
        csum & 0xff
])
t = checksum + t

f2 = enc_s + pad + t + ((16 - (len(t) % 16)) * b"\x00")
c = AES.new(key, AES.MODE_CBC, iv)
f1 = c.decrypt(f2)

with open("tmp/f2.png", "wb") as f:
    f.write(f2)

with open("tmp/f1.png", "wb") as f:
    f.write(f1)

with open("tmp/iv.bin", "wb") as f:
    f.write(iv)
