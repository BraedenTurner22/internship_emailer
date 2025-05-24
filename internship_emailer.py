import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header

# load env at import
load_dotenv()
SENDER_EMAIL        = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL      = os.getenv('RECEIVER_EMAIL')
GOOGLE_PASSWORD_KEY = os.getenv('GOOGLE_PASSWORD_KEY')

def send_email(job: dict) -> None:
    """
    job: {
      'Company': ...,
      'Role': ...,
      'Location': ...,
      'Application Link': ...
    }
    """
    # Build subject and body
    subject = f"New Internship: {job['Company']} – {job['Role']}"
    body = (
        f"Company: {job['Company']}\n"
        f"Role:    {job['Role']}\n"
        f"Location:{job['Location']}\n"
        f"Apply:   {job['Application Link']}\n"
    )
    # Create a MIMEText object with UTF-8
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From']    = SENDER_EMAIL
    msg['To']      = RECEIVER_EMAIL

    # Send
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, GOOGLE_PASSWORD_KEY)
        server.sendmail(
            SENDER_EMAIL,
            [RECEIVER_EMAIL],
            msg.as_string()
        )
    print(f"✉️  Sent: {subject}")
