#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Import module for image editing
from PIL import Image, ImageDraw, ImageFont
# Import module for manipulating data
import pandas as pd
# Import module for passing variable
import sys
# Import module for monitoring progress
import time

# 0 MONITORING
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
# 1 EMAIL DATA
df_email = pd.read_csv('data/data email.csv')
row_length = df_email.shape[0]

if __name__ == '__main__':
    # MONITORING
    printProgressBar(0,row_length,prefix='Progress:',suffix='Complete',length=50)
    for i in range(row_length):
        # 0 IMAGES
        # Create image object
        image = Image.open('images/Certificate for Gryffindor.jpg')
        draw = ImageDraw.Draw(image)
        # Image size
        width,height = image.size
        # Specified font-style and font-size 
        font = ImageFont.truetype(font='font/OpenSans-CondBold.ttf',size=110)

        # 1 ADDING TEXT TO IMAGE
        # Specify text
        text = df_email.loc[i,'name']
        # Text size for making it center
        w,h = draw.textsize(text,font=font)
        draw.text(xy=((width-w)/2,(height-h)/2 - 50),text=text,font=font,fill='black',align='left')
    
        # 2 CONVERT JPG TO PDF
        imagePDF = image.convert('RGB')
        imagePDF.save('certificates/'+text+' - Certificate for Gryffindor Student.pdf')
        # 3 CHECK STATUS
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i+1,row_length,prefix='Progress:',suffix='Complete',length=50)
