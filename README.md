imagelabeler
============
A Python 3.5.2 class that adds labels, such as original date stamps, to .jpg images.  Makes use of the [**Pillow 5.0.0 image manipulation library**](https://python-pillow.org/).

*Designed to be used in a clinical health setting for automatically datestamping otoscopic pictures.*

### Basic behaviour:

1. If used as a `__main__` program:

    * Searches the `images/` directory for .jpg images and loads pillow image objects.
    	* Uses an MD5 hash to determine if the image has already been labeled.
    	* Automatically rotates images if taken on a cellphone.
    * Creates LabeledImage objects for the images.
        * Labels images with text or original date from Exif data.
        * Returns a merged Pillow Image object.
    * Saves an archive copy of the original image.
    * Saves the newly labeled images to their own folder.
    
2. The LabeledImage class:
    * Takes a Pillow image instance, rotates it *if needed*, and creates a new 'drawing' layer to place labels on.
    * Up to 4 labels can be created in each corner of the image.
    * LabeledImage.add_date_label(position) automatically adds the original image creation date.
        * Only works with original .jpgs with required exif data.
       
### To Be Added:

* ~~**Image hashing functions** to keep track whether or not an image has been labeled before.~~
* Find way to **preserve Exif data** and resize images.
* Functions to move original images to an archive (keep 50 images).
    * Partially implemented.
* **Error checking** and handling and optimizations.
* Re-format code to PEP-8 standards, and add docstrings and other documentation.
    * Partially implemented.
* **Front end GUI** (PyQT 5)
