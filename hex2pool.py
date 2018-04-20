from PIL import Image
from sys import argv
import re
import math

if len(argv) != 2:
    print("Usage: hex2pool.py <output file name>")
    exit()

WIDTH = 60
HEIGHT = 60
COLS = 10

balls = {}

for i in range(16):
    ball = Image.open("balls/" + str(i) + ".png")
    balls["%x" % i] = ball

inp = re.search('[0-9a-f]*', raw_input().lower()).group(0)

nrows = int(math.ceil(float(len(inp)) / float(COLS)))
new_im = Image.new('RGB', (WIDTH * COLS, HEIGHT * nrows), "white")

for i in range(len(inp)):
    b = balls[inp[i]]
    new_im.paste(b, 
        (WIDTH * (i % COLS) + 5, 
            ((HEIGHT - b.height) / 2) + (HEIGHT * (i / COLS))),
        mask=b)

new_im.save(argv[1])
