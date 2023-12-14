# email_sender.py

import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

cur_path = os.getcwd()
new_path = os.path.relpath('./credentials/email_credentials.json', cur_path)

with open(new_path) as f:
    data = json.load(f)
sender_email = data['EMAIL_USERNAME']
sender_password = data['EMAIL_PASSWORD']
subject = 'Your new ebook from Podcast Reader'

def send_email(body, receiver_email, attachment_path):
    """
    Send an email with an attachment.

    Parameters:
    subject (str): Subject of the email
    body (str): Body of the email
    sender_email (str): Email address of the sender
    sender_password (str): Password of the sender's email account
    receiver_email (str): Email address of the receiver
    attachment_path (str): File path of the attachment
    """
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent
    filename = attachment_path.split("/")[-1]
    with open(attachment_path, "rb") as attachment:
        # Instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload(attachment.read())

        # Encode into base64
        encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', f"attachment; filename= {filename}")
    
    # Attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # Create SMTP session for sending the mail
    with smtplib.SMTP('mail.privateemail.com', 587) as s: # Use your SMTP server and port
        s.starttls()
        s.login(sender_email, sender_password)
        
        # Converts the Multipart msg into a string
        text = msg.as_string()
        
        # Sending the mail
        s.sendmail(sender_email, receiver_email, text)

