#!/usr/bin/python3
from PIL import Image, ImageDraw, ImageFont

class LabeledImage():

    def __init__(self, originalimg, label, labelPosition):
        self.originalimg = originalimg
        self.label = label
        self.labelPosition = labelPosition

        #Load Roboto font with large 200 size font
        self.fnt = ImageFont.truetype('Roboto-Regular.ttf', 75)
        self.txtcolor = (255,255,255,200)
        self.bgtxtcolor = (0,0,0,200)
        self.pdg = 20
        #Create a blank image, original image size, to write text with
        #no opacity
        self.labelLayer = Image.new('RGBA', self.originalimg.size,
                                    (255,255,255,0))
        self.labelDraw = ImageDraw.Draw(self.labelLayer)

        #Find the font and image dimensions to aid in placing text
        self.txtwidth, self.txtheight = self.labelDraw.textsize(self.label,
                                                                font=self.fnt)
        self.imgwidth, self.imgheight = self.originalimg.size

    def drawLabel(self):
        if self.labelPosition == 'top left':
            #Top left text
            self.labelDraw.rectangle([self.pdg, self.pdg,
                                      (self.pdg + self.txtwidth),
                                      (self.pdg+self.txtheight)],
                                      fill=self.bgtxtcolor)
            self.labelDraw.text((self.pdg, self.pdg), self.label,
                                font=self.fnt, fill=self.txtcolor)
        elif self.labelPosition == 'bottom left':
            #Bottom left text
            self.labelDraw.rectangle([self.pdg,
                                      self.imgheight-(self.txtheight+self.pdg),
                                      self.pdg+self.txtwidth,
                                      self.imgheight-self.pdg],
                                      fill=self.bgtxtcolor)
            self.labelDraw.text((self.pdg,
                                 self.imgheight-(self.txtheight+self.pdg)),
                                 self.label, font=self.fnt, fill=self.txtcolor)
        elif self.labelPosition == 'top right':
            #Top right text
            self.labelDraw.rectangle([self.imgwidth-(self.txtwidth+self.pdg),
                                      self.pdg, self.imgwidth-self.pdg,
                                      self.txtheight+self.pdg],
                                      fill = self.bgtxtcolor)
            self.labelDraw.text((self.imgwidth-(self.txtwidth+self.pdg),
                                 self.pdg), self.label, font=self.fnt,
                                 fill=self.txtcolor)
        elif self.labelPosition == 'bottom right':
            #Bottom right text
            self.labelDraw.rectangle([self.imgwidth-(self.txtwidth+self.pdg),
                                      self.imgheight-(self.txtheight+self.pdg),
                                      self.imgwidth-self.pdg,
                                      self.imgheight-self.pdg],
                                      fill = self.bgtxtcolor)
            self.labelDraw.text((self.imgwidth-(self.txtwidth+self.pdg),
                                 self.imgheight-(self.txtheight+self.pdg)),
                                 self.label, font=self.fnt, fill=self.txtcolor)
        else:
            print('Invalid label position specified')

    def show(self):
        self.drawLabel()
        return Image.alpha_composite(self.originalimg, self.labelLayer)

#Open the image and convert it to RGBA
imgtwo = Image.open('images/imageone.jpg').convert('RGBA')
#Get the creation date of the image from the appropriate exif tag
text = Image.open('images/imageone.jpg')._getexif()[36867]
finalImage = LabeledImage(imgtwo, ' ' + text + ' ', 'bottom left')

thumbsize = (640, 480)
godImage = finalImage.show()
godImage.thumbnail(thumbsize)
godImage.show()


