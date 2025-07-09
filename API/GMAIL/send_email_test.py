import ssl
from email.message import EmailMessage
import smtplib

import os
from env_loader import load_env_from_project_root
load_env_from_project_root()
EMAIL_PASS = os.getenv("EMAIL_PASS")

email_sender = 'hugo.lambert.perso@gmail.com'
email_receiver = 'hugo.lambert.perso@gmail.com'
email_password = EMAIL_PASS

subject = 'TEST AUTO EMAIL'
body = '''
SUCCESS.
'''

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())