#!/usr/bin/python3

import hashlib
import pickle
import os
from PIL import Image

def get_hash_db(filename):
    """Load pickled list of image hash strings.

    Args:
        filename(string):name of file that the hash database is stored in.

    Returns:
        list object of hash strings if the file exists. Otherwise, return
        an empty list if any file error occurs.

    """

    try:
        print('Loading hash database')
        with open(filename, 'rb') as f:
            return list(pickle.load(f))
    except:
        print('Hash database not found, creating...')
        return []

def save_hash_db(filename, hashes):
    """Save the hash database by pickling a set.

    Args:
        filename(string): name of the hash database.
        hashes(list): list of image hashes to save.

    """
    with open(filename, 'wb') as f:
        print('Saving hash database')
        pickle.dump(set(hashes),f)

def remove_labeled_images(images, hash_db, file_list):
    """Get rid of images that have already been labeled before.

    This function creates a hash for each image object and compares that hash
    to the hash database.  If there's a match, that image will be ignored.

    Args:
        images(List): list of all images in the image directory.
        hash_db(List): list of previously seen image hashes.
        file_list(List): list of all file names in the directory.

    Returns:
        unlabeled_images(List): list of Image objects that have not been
                                labeled.
        new_hashes(List): list of new image hashes.
        new_file_list(List): list of file names in directory that need labels.

    """

    unlabeled_images = []
    new_file_list = []
    for i, image in enumerate(images):
        #create an md5 hash of image, which should be sufficient for the
        #purposes of this program.
        image_hash = hashlib.md5(image.tobytes()).hexdigest()
        #image_hash = str(imagehash.average_hash(Image.open(file_list[i])))

        if image_hash not in hash_db:
            unlabeled_images.append(image)
            new_file_list.append(file_list[i])
            print('New image hash found for: ' + file_list[i])
        else:
            print('Hash database match found for: ' + file_list[i])

    return unlabeled_images, new_file_list

def get_hashes(filenames):
    """Return a list of hashes for a given list of filenames"""

    new_filenames = []
    for f in filenames:
        new_filenames.append(os.path.join('labeled images',
                                          os.path.basename(f)))

    try:
        labeled_images = [Image.open(f) for f in new_filenames]
        return [hashlib.md5(image.tobytes()).hexdigest()
            for image in labeled_images]
        #return new_hashes
    finally:
        for i in labeled_images:
            i.close()
            print('Saved and opened labeled image re-closed')

