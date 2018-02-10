#!/usr/bin/python3
from PIL import Image, ImageDraw, ImageFont
import glob

class LabeledImage():

    def __init__(self, img):
        self.img = img
        self.label_layer, self.label_draw = self._create_draw_surface()
        self.labels = {
                       'top left':False,
                       'top right':False,
                       'bottom right':False,
                       'bottom left':False,
                      }
        #exif only available for non-copied or converted image
        self.imgdate = img._getexif()[36867]

    def _create_draw_surface(self):
        new_image = Image.new('RGBA', self.img.size, (255,255,255,0))
        return new_image, ImageDraw.Draw(new_image)

    def clear_draw_surface(self):
        for position in self.labels:
            self.labels[position]=False
        self.label_layer, self.label_draw = self._create_draw_surface()

    def _place_label(self,x,y,label,font):
        text_color = (255,255,255,200)
        background_color = (0,0,0,200)
        w,h = self.label_draw.textsize(label, font=font)
        self.label_draw.rectangle([x,y,x+w,y+h],fill=background_color)
        self.label_draw.text((x,y),label,font=font, fill=text_color)

    def add_label(self, label, position):
        padding = 20
        label = ' '+label+' '

        font = ImageFont.truetype('Roboto-Regular.ttf', 100)

        text_width, text_height = self.label_draw.textsize(label, font=font)
        image_width, image_height = self.img.size

        if self.labels[position] == True:
            print('Label already exists in this position')
        else:
            self.labels[position] = True
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
        #datetime functions here to make date nice format
        self.add_label(self.imgdate, position)

    def get(self):
        merged_image = Image.alpha_composite(self.img.convert('RGBA'),
                                             self.label_layer)
        return merged_image

if __name__=='__main__':
    # Load name of all jpegs in images folder
    originals = [i for i in glob.glob('images/*.[jJ][pP][gG]')]

    # Create image objects
    images = [Image.open(i) for i in originals]

    # Create image labeler objects for each image
    image_labelers = [LabeledImage(image) for image in images]

    # Add date labels to each image, resize, and show the image
    for i in image_labelers:
        i.add_date_label('top right')
        i.add_date_label('top left')
        i.clear_draw_surface()
        i.add_label('I Love Lily Popper!','bottom left')
        i.add_date_label('bottom right')
        i.get().resize((640,480)).show()

    for image in images:
        image.close()
