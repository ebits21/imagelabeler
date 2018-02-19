#!/usr/bin/python3

"""Add date or text labels to images.

This module takes .jpg images in the current directory and adds text or date
labels to them.  Only images that have not been labeled before may be labeled.

The module uses the pillow (PIL) image library for image handling. The hashlib
module is used to create a fingerprint for each labeled image. If the
fingerprint has been seen before the module will not label the image. The
pickle module is used to save a list that acts as a database of previously
seen hashes.

Todo:
    * Have module create labeledImages and originalImages folders and move
      processed images to the correct location.
"""

import glob
#import hashlib
#import pickle
import LabeledImage
import os
import hashFunctions
import shutil
from PIL import Image, ImageDraw, ImageFont


def archive_images(filenames):
    """Move or copy original images to archive folder.

    Args:
        filenames(List): original list of filenames.

    """

    if not os.path.exists('archive'):
        try:
            os.mkdir('archive')
            print('Archive folder made.')
        except:
            print('Error making the archive folder')
    for f in filenames:
        try:
            #shutil.move(f, os.path.join('archive',os.path.basename(f)))
            shutil.copyfile(f, os.path.join('archive',os.path.basename(f)))
            print('Original image archived')
        except:
            print(f + ' unable to be archived')

def save_labeled_images(images, filenames):
    """Save labeled images to labeled images folder.

    Args:
        images: Image objects to save.
        filenames: list of original filenames.

    """

    if not os.path.exists('labeled images'):
        try:
            os.mkdir('labeled images')
            print('Made labeled images folder')
        except:
            print('Error making the labeled images folder')
    for i, img in enumerate(images):
        try:
            img.save(os.path.join('labeled images',
                                  os.path.basename(filenames[i])))
            print('labeled image saved')
        except:
            print(filenames + ' unable to save labeled image')

if __name__ == '__main__':
    #Load name of all jpegs in images folder
    originals = [i for i in glob.glob(os.path.join('images',
                                                   '*.[jJ][pP][gG]'))]

    #Create image objects
    images = [Image.open(i) for i in originals]

    #Load the hash database and remove images that have been labeled before.
    hash_db = hashFunctions.get_hash_db('hashes.py')
    pimages, poriginals = hashFunctions.remove_labeled_images(images,
                                                              hash_db,
                                                              originals)


    # Create image labeler objects for each image
    image_labelers = [LabeledImage.LabeledImage(image) for image in pimages]

    # Add date labels to each image, resize, and show the image
    for i in image_labelers:
        i.add_label('Added label','bottom left')
        i.add_label('Added label 2', 'bottom left')
        i.add_date_label('bottom right')

    #labeled_images = [i.get().resize((640,480)) for i in image_labelers]
    labeled_images = [i.get() for i in image_labelers]

    #Tests statements.
    print(str(len(hash_db))+' previous hashes in the database')

    save_labeled_images(labeled_images, poriginals)

    for image in labeled_images:
        image.close()

    #Get hashes of newly labeled images. Must be called after images are saved.
    new_hashes = hashFunctions.get_hashes(poriginals)
    print(str(len(new_hashes))+' new hashes created (may have duplicates)')

    #Save new and old hashes to the hash database.
    hashFunctions.save_hash_db('hashes.py', hash_db+new_hashes)

    #Close all images
    for image in pimages:
        image.close()

    #Move or copy original images to archive folder.
    archive_images(poriginals)
