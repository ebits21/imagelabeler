# imagelabeler

A Python class that adds labels, such as original date stamps, to .jpg images.  Makes use of the Pillow image manipulation library.

Designed to be used in a clinical health setting for automatically datestamping otoscopic pictures.

## Basic behaviour:

* If used as a `__main__` program:
    * Searches the images/ directory for .jpg images and loads pillow image objects.
    * Creates LabeledImage objects for the images.
        * Labels images with text or original date from Exif data.
        * Returns a merged Pillow Image object.
    * Resizes images for testing purposes.
    * Shows the images on the screen as a preview.
    
* The LabeledImage class:
    * Takes a Pillow image instance and creates a new 'drawing' layer to place labels on.
    * Up to 4 labels can be created in each corner of the image.
    * LabeledImage.add_date_label(position) automatically adds date the image was created.
        * Only works with original .jpgs with required exif data.
       
## To Be Added:

* Image hashing functions to keep track whether or not an image has been labeled before.
* Find way to preserve Exif data and resize images.
* Functions to move original images to an archive (keep 50 images).
* Error checking and handling and optimizations.
* Front end GUI (PyQT 5)
