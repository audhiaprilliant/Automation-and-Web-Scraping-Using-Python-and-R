#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Import module for image editing
from PIL import Image, ImageDraw, ImageFont
# Import modules for sending email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Import module for manipulating markdown
import markdown
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
# 2 SENDER
sender_email = sys.argv[1]
password = sys.argv[2]

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
        imagePDF.save('Certificate for Gryffindor.pdf')
    
        # 3 RECEIVER
        receiver_email = df_email.loc[i,'email']
    
        # 4 CONFIGURE SUBJECT
        subject = 'Certificate for Gryffindor Student - {receiver}'.format(receiver = text)
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # 5 CONFIGURE BODY OF EMAIL
        f = open('markdown/body.md','r')
        htmlmarkdown = markdown.markdown(f.read())
        body = htmlmarkdown.format(receiver_name = text)
        # Turn these into plain/html MIMEText objects
        body = MIMEText(body,'html')
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(body)

        # 6 CONFIGURE ATTACHMENT FILES
        filename = 'Certificate for Gryffindor.pdf'
        # Open PDF file in binary mode
        with open(filename, 'rb') as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}')
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # 7 SEND EMAIL
        df_email_stat = pd.read_csv('data/data email - monitoring.csv')
        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email,text
                )
            # 8 CHECK STATUS
            time.sleep(0.1)
            printProgressBar(i+1,row_length,prefix='Progress:',suffix='Complete',length=50)
            # Update Progress Bar
            # Update stat
            df_email_stat.loc[i,'stat'] = '1'
            df_email_stat.to_csv('data/data email - monitoring.csv',index=False)
        except smtplib.SMTPException:
            df_email_stat.loc[i,'stat'] = 'Error'
            df_email_stat.to_csv('data/data email - monitoring.csv',index=False)
