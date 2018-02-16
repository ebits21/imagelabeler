#!/usr/bin/python3
from PIL import Image
import hashlib
import glob
import pickle

originals = [i for i in glob.glob('images/*.[jJ][pP][gG]')]
images = [Image.open(i) for i in originals]

with open ('hashes.py', 'rb') as f:
    oldhashes = pickle.load(f)

hashes = [hashlib.md5(image.tobytes()).hexdigest() for image in images]

for image in images:
    image.close()

for h in hashes:
    if h in oldhashes:
        print('Sorry, this image has already been labeled.')

with open('hashes.py', 'wb') as f:
    pickle.dump(hashes, f)
