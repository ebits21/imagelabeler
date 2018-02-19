#!/usr/bin/python3

"""Create a labeled image object that.

This module creates a LabeledImage object, which associate a drawing object
and surface with a pillow Image object.  Labels can be drawn onto the drawing
surface and then merged into a new Image object when called.

"""

import datetime
from PIL import Image, ImageDraw, ImageFont

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

        #exif only available for non-copied or converted image
        try:
            #try to get the original date the image was taken.
            self.imgdate = img._getexif()[36867]
        except:
            self.imgdate = False
            print('No exif data available for image')

        try:
            #try to get the orientation of the image if available.
            self.orientation = img._getexif()[274]
        except:
            self.orientation = False

        #Rotate the image if is was taken on a cellphone.
        rotated_img = self._rotate_image(img)
        self.img = rotated_img

        self.label_layer, self.label_draw = self._create_draw_surface()
        #Labels can be added to 1 of 4 image corners.
        self.labels = {'top left':False,
                       'top right':False,
                       'bottom right':False,
                       'bottom left':False
                      }

    def _rotate_image(self, image):
        """Rotate the original image if it has Orientation exif data."""
        #If it is rotated right.
        if self.orientation == 8:
            #Rotate 90 degrees counter clockwise, expand true keeps aspect.
            print('image rotated 90 degress counter clockwise')
            return image.rotate(90, expand=True)
        #If it is upside down.
        elif self.orientation == 3:
            print('image rotated 180 degress counter clockwise')
            return image.rotate(180, expand=True)
        #If it is rotated left.
        elif self.orientation ==  6:
            print('image rotated 270 degress counter clockwise')
            return image.rotate(270, expand=True)
        else:
            return image

    def _create_draw_surface(self):
       """Create a transparent drawing surface and drawing object.

       Returns:
           A new labeled image layer and drawing object based on size of image.

       """

       new_image = Image.new('RGBA', self.img.size, (255, 255, 255, 0))
       return new_image, ImageDraw.Draw(new_image)

    def clear_draw_surface(self):
        """Clear all labels and create new drawing surfaces."""

        for position in self.labels:
            self.labels[position] = False
        self.label_layer, self.label_draw = self._create_draw_surface()

    def _place_label(self, x, y, label, font):
        """Draw background box and text label on image.

        Args:
            x,y (int): x and y co-ordinates the the top left of the label.
            label (string): text to put on label.
            font (ImageFont): ttf font for the label.

        """

        text_color = (255, 255, 255, 200)
        background_color = (0, 0, 0, 200)

        #Calculate the width and height of the label.
        w, h = self.label_draw.textsize(label, font=font)

        #Draw background box the size of the text and then draw the text.
        self.label_draw.rectangle([x, y, x+w, y+h], fill=background_color)
        self.label_draw.text((x, y), label, font=font, fill=text_color)

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
                self._place_label(padding, padding, label, font)
            elif position == 'bottom left':
                self._place_label(padding, image_height-(text_height+padding),
                                  label, font)
            elif position == 'top right':
                self._place_label(image_width-(text_width+padding), padding,
                                  label, font)
            elif position == 'bottom right':
                self._place_label(image_width-(text_width+padding),
                                  image_height-(text_height+padding),
                                  label, font)

    def add_date_label(self, position):
        """Add a date label to the drawing surface.

        Args:
            position(string): position of the label.

        """

        #Create a datetime object, then draw label in June 21, 2000 format.
        if self.imgdate:
            original_date = datetime.datetime.strptime(self.imgdate,
                                                   "%Y:%m:%d %H:%M:%S")
            self.add_label(original_date.strftime("%b %d, %Y"), position)
        else:
            print('Date information not available')

    def get(self):
        """Merge drawing layers and return the merged image.

        Return:
            A merged pillow image object.

        """

        merged_image = Image.alpha_composite(self.img.convert('RGBA'),
                                             self.label_layer)
        return merged_image

