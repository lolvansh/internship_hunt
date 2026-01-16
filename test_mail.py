import smtplib
import os
import mimetypes
from email.message import EmailMessage

# --- CONFIGURATION ---
SENDER_EMAIL = "vansh.pandya.77@gmail.com"
APP_PASSWORD = "tkej tcph qwiv bdad"
RESUME_FILENAME = r"D:\python\cloud-cli\assets\Resume.pdf"

# Target for the spam test
TEST_RECIPIENT = "kanyelover540@gmail.com"

def send_test_email():
    if not os.path.exists(RESUME_FILENAME):
        print(f"❌ Error: {RESUME_FILENAME} not found. Put your resume in this folder first.")
        return

    subject = "Python Internship Application - Vansh Pandya"
    
    # Exactly the same body as your main script
    body = f"""\
Dear Hiring Team at Test Company,

I am writing to express my enthusiastic interest in the Python Developer Internship position at Test Company.

I have strong technical skills in Python, specifically in automation, web scraping, and data handling. 

I have attached my resume and GitHub profile for your review.

GitHub: https://github.com/lolvansh

Best regards,
Vansh Pandya
"""

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = TEST_RECIPIENT
    msg.set_content(body)

    # Attach Resume
    try:
        with open(RESUME_FILENAME, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(RESUME_FILENAME)
            maintype, subtype = mimetypes.guess_type(file_name)[0].split('/', 1)
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
    except Exception as e:
        print(f"❌ Resume Error: {e}")
        return

    print(f"Attempting to send to {TEST_RECIPIENT}...")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email Sent Successfully!")
        print("👉 NOW: Check your inbox (and Spam folder) at lolvansh577@gmail.com")
    except Exception as e:
        print(f"❌ Failed to send: {e}")

if __name__ == '__main__':
    send_test_email()