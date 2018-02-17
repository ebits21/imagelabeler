#!/usr/bin/python3

"""Add date or text labels to images.

This module takes .jpg images in the current directory and adds text or date labels to them.  Only images that have not been labeled before may be labeled.

The module uses the pillow (PIL) image library for image handling. The hashlib
module is used to create a fingerprint for each labeled image. If the
fingerprint has been seen before the module will not label the image. The pickle
module is used to save a list that acts as a database of previously seen hashes.

Todo:
    * Have module create labeledImages and originalImages folders and move
      processed images to the correct location.
"""

from PIL import Image, ImageDraw, ImageFont
import glob
import datetime
import hashlib
import pickle

class LabeledImage():
    """Create a labeled image object from a given image.

    This class takes a pillow image object and creates a drawing surface that
    a label background and text label can be drawn on. Finally, the drawing
    surface gets merged with the original image.

    Methods:
        clear_draw_surface():
            discard currect drawing surface and replace with a blank surface.

        add_label(label,position):
            add a given text label in one of 4 locations (ex. 'top left')

        add_date_label(position):
            add an original image creation date stamp in given location.

        get():
            returns a merged pillow image object (labeled image)

    """

    def __init__(self, img):
        """Create a labeled image object.

        Creates a pillow drawing surface and a new blank label layer the same
        size as the original image. Also keeps track of whether or not a label
        is in 1 of 4 corners of the image. Lastly, extracts the original
        creation date of the image from .jpg exif data

        Args:
            img (Image): a pillow image object with exif data unaltered.

        """

        self.img = img
        self.label_layer, self.label_draw = self._create_draw_surface()
        #Labels can be added to 1 of 4 image corners.
        self.labels = {
                       'top left':False,
                       'top right':False,
                       'bottom right':False,
                       'bottom left':False
                      }
        #exif only available for non-copied or converted image
        self.imgdate = img._getexif()[36867]

    def _create_draw_surface(self):
        """Create a transparent drawing surface and drawing object.

        Returns:
            A new labeled image layer and drawing object based on size of image.

        """

        new_image = Image.new('RGBA', self.img.size, (255,255,255,0))
        return new_image, ImageDraw.Draw(new_image)

    def clear_draw_surface(self):
        """Clear all labels and create new drawing surfaces."""

        for position in self.labels:
            self.labels[position]=False
        self.label_layer, self.label_draw = self._create_draw_surface()

    def _place_label(self,x,y,label,font):
        """Draw background box and text label on image.

        Args:
            x,y (int): x and y co-ordinates the the top left of the label.
            label (string): text to put on label.
            font (ImageFont): ttf font for the label.

        """

        text_color = (255,255,255,200)
        background_color = (0,0,0,200)

        #Calculate the width and height of the label.
        w,h = self.label_draw.textsize(label, font=font)

        #Draw background box the size of the text and then draw the text.
        self.label_draw.rectangle([x,y,x+w,y+h],fill=background_color)
        self.label_draw.text((x,y),label,font=font, fill=text_color)

    def add_label(self, label, position):
        """Draw text label to given position.

        Args:
            label (string): text to add for label.
            position (string): position to place label as kept track by the
                self.labels dictionary. Examples include 'top left',
                top right', 'bottom left', and 'bottom right'. Does not
                allow more than 1 label in a given position.

        """

        padding = 20
        label = ' '+label+' '

        font = ImageFont.truetype('Roboto-Regular.ttf', 100)

        #Calculate font and image dimensions for placing the label.
        text_width, text_height = self.label_draw.textsize(label, font=font)
        image_width, image_height = self.img.size

        #Check to see if a label already exists in a position. If is does
        #display message and do not draw a new label. If not draw a new label
        #and add entry to self.labels.
        if self.labels[position] is not False:
            print('Label' + self.labels[position] +
                  'already exists in the ' + position + ' position')
        else:
            self.labels[position] = label
            if position == 'top left':
                 self._place_label(padding,padding,label,font)
            elif position == 'bottom left':
                 self._place_label(padding,image_height-(text_height+padding),
                                    label,font)
            elif position == 'top right':
                 self._place_label(image_width-(text_width+padding),padding,
                                    label,font)
            elif position == 'bottom right':
                  self._place_label(image_width-(text_width+padding),
                                    image_height-(text_height+padding),
                                     label,font)

    def add_date_label(self, position):
        """Add a date label to the drawing surface.

        Args:
            position(string): position of the label.

        """

        #Create a datetime object, then draw label in June 21, 2000 format.
        original_date = datetime.datetime.strptime(self.imgdate,
                                                   "%Y:%m:%d %H:%M:%S")
        self.add_label(original_date.strftime("%b %d, %Y"), position)

    def get(self):
        """Merge drawing layers and return the merged image.

        Return:
            A merged pillow image object.

        """

        merged_image = Image.alpha_composite(self.img.convert('RGBA'),
                                             self.label_layer)
        return merged_image

def get_hash_db(filename):
    """Load pickled list of image hash strings.

    Args:
        filename(string):name of file that the hash database is stored in.

    Returns:
        list object of hash strings if the file exists. Otherwise, return
        an empty list if any file error occurs.

    """

    try:
        with open (filename, 'rb') as f:
            return list(pickle.load(f))
    except:
        return []

def save_hash_db(filename, hashes):
    """Save the hash database by pickling a set.

    Args:
        filename(string): name of the hash database.
        hashes(list): list of image hashes to save.

    """
    with open (filename, 'wb') as f:
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
    new_hashes = []
    new_file_list = []
    for i, image in enumerate(images):
        #create an md5 hash of image, which should be sufficient for the
        #purposes of this program.
        image_hash = hashlib.md5(image.tobytes()).hexdigest()

        if image_hash not in hash_db:
            unlabeled_images.append(image)
            new_hashes.append(image_hash)
            print(file_list[i])
            new_file_list.append(file_list[i])

    return unlabeled_images, new_hashes, new_file_list

if __name__=='__main__':
    #Load name of all jpegs in images folder
    originals = [i for i in glob.glob('images/*.[jJ][pP][gG]')]

    #Create image objects
    images = [Image.open(i) for i in originals]

    #Load the hash database and remove images that have been labeled before.
    hash_db = get_hash_db('hashes.py')
    images, new_hashes, originals = remove_labeled_images(images,
                                                              hash_db,
                                                              originals)

    # Create image labeler objects for each image
    image_labelers = [LabeledImage(image) for image in images]

    # Add date labels to each image, resize, and show the image
    for i in image_labelers:
        i.add_date_label('top right')
        i.add_date_label('top left')
        i.clear_draw_surface()
        i.add_label('Added label','bottom left')
        i.add_label('Added label 2', 'bottom left')
        i.add_date_label('bottom right')
        i.get().resize((640,480)).show()

    #Tests statements.
    print(hash_db)
    print(new_hashes)
    print(originals)

    #Save new and old hashes to the hash database.
    save_hash_db('hashes.py', hash_db+new_hashes)

    #Close all images
    for image in images:
        image.close()
