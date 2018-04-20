import zlib
balls = open("tmp/poolballs.txt", "r").read()

words = []

for ball in balls:
    if ball == 'W':
        words.append('WHITE')
    elif ball == 'Y':
        words.append('YELLOW')
    elif ball == 'U':
        words.append('BLUE')
    elif ball == 'R':
        words.append('RED')
    elif ball == 'P':
        words.append('PURPLE')
    elif ball == 'O':
        words.append('ORANGE')
    elif ball == 'G':
        words.append('GREEN')
    elif ball == 'N':
        words.append('BROWN')
    elif ball == 'B':
        words.append('BLACK')
    elif ball == 'y':
        words.append('yellow')
    elif ball == 'u':
        words.append('blue')
    elif ball == 'r':
        words.append('red')
    elif ball == 'p':
        words.append('purple')
    elif ball == 'o':
        words.append('orange')
    elif ball == 'g':
        words.append('green')
    elif ball == 'n':
        words.append('brown')

text = "\n".join(words)

dat = open("tmp/secdsm_secret_image.png", "rb").read()
#offset = dat.find("IDAT")
offset = 33
pre = dat[:offset]
post = dat[offset:]

chunk = b"sdSm" + bytes(text, 'utf-8')
csum = zlib.crc32(chunk)


sz = len(text)
size = bytes([(sz >> 24) & 0xff,
        (sz >> 16) & 0xff,  
        (sz >> 8) & 0xff,
        sz & 0xff])

checksum = bytes([(csum >> 24) & 0xff,
        (csum >> 16) & 0xff,  
        (csum >> 8) & 0xff,
        csum & 0xff])

dat = pre + size + chunk + checksum + post

open("tmp/secdsm_secret_image_2.png", "wb").write(dat)
