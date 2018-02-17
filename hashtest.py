#!/usr/bin/python3
from PIL import Image
import hashlib
import glob
import pickle

def get_hash_db(filename):
    with open (filename, 'rb') as f:
        return pickle.load(f)

def save_hash_db(filename, hashes):
    with open (filename, 'wb') as f:
        pickle.dump(hashes,f)

def create_image_hashes(images):
    return [hashlib.md5(image.tobytes()).hexdigest() for image in images]

originals = [i for i in glob.glob('images/*.[jJ][pP][gG]')]
images = [Image.open(i) for i in originals]

oldhashes = get_hash_db('hashes.py')
hashes = create_image_hashes(images)

for image in images:
    image.close()

for h in hashes:
    if h in oldhashes:
        print('Sorry, this image has already been labeled.')

save_hash_db('hashes.py', hashes)
