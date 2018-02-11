#!/usr/bin/python3
from PIL import Image

image = Image.open('images/imageone.jpg')
imageCopy = image.copy()
date = imageCopy._getexif()[36867]
print (date)
