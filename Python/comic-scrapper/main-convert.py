# Image manipulation
from PIL import Image
# Directory management
import os
# Regular expression
import re
# Ceiling
import math

## Parameter(s)
# Main directory
main_dir = 'data/Lennon The New York Years'
# List of directory
all_directory = [x[0] for x in os.walk(main_dir)]
# Select one directory

## Custom function(s)
# Order string based on number (https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside)
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

# Looping
for dir in all_directory[1:]:
    main_subdir = dir
    # Output PDF file name
    pdf_file = main_dir + '/' + os.path.split(main_subdir)[-1] + '.pdf'

    ## List of images
    # Images
    list_images = os.listdir(path = main_subdir)

    # Sort filename
    list_images.sort(key = natural_keys)

    # List of images
    list_images

    ## Open and resize images
    l_height = []
    l_width = []
    # Loop
    for image_path in list_images:
        # Open image
        img = Image.open(os.path.join(main_subdir, image_path))
        l_height.append(img.height)
        l_width.append(img.width)

    # Optimal size
    opt_size = (l_height[0], l_width[0])

    # Images
    images = []

    # Loop
    for image_path in list_images:
        # Open image
        img = Image.open(os.path.join(main_subdir, image_path)).convert('L')
        # Image size
        h, w = img.height, img.width
        # Resize image
        if (h == opt_size[0]):
            if (w >= opt_size[1]):
                resize_img = img
            elif (w < opt_size[1]):
                resize_img = img.resize((opt_size[1], math.ceil(h * (opt_size[1]/w))))
        elif (h > opt_size[0]):
            resize_img = img.resize((math.ceil(w * (opt_size[0]/h)), opt_size[0]))
        else:
            resize_img = img.resize((math.ceil(w * (opt_size[0]/h)), opt_size[0]))
            if resize_img.width < opt_size[1]:
                t = opt_size[1] * (opt_size[0]/h) / resize_img.height
                resize_img = resize_img.resize((opt_size[1], math.ceil(h * (opt_size[1]/w))))
        # Crop image
        crop_img = resize_img.crop((0, 0, opt_size[1], opt_size[0]))
        # Add image into list
        images.append(crop_img)

    ## Convert JPG to PDF
    # Save the images as a PDF
    images[0].save(
        pdf_file,
        save_all = True,
        append_images = images[1:],
        resolution = 100,
        quality = 95
    )