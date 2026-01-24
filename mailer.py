import smtplib
import time
import random
import os
import mimetypes
from datetime import datetime
from email.message import EmailMessage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_conn import Application

# --- CONFIGURATION ---
SENDER_EMAIL = "vansh.pandya.77@gmail.com" # please change it to your email
APP_PASSWORD = 'xxxx xxxx xxxx xxxx'#this is just a placeholder, replace with actual app password and keep it secure in the env
RESUME_FILENAME = r"D:\python\cloud-cli\assets\Resume.pdf"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "applications.db")
DB_FILE = f"sqlite:///{DB_PATH}"

# Safety Limits
DAILY_LIMIT = 80 #do not be gready dont write more than 80 in a day or chage the delay or you will be marked as spam
MIN_DELAY = 60    
MAX_DELAY = 300   
TEST_MODE = False 

# Database Connection
engine = create_engine(DB_FILE)
Session = sessionmaker(bind=engine)
session = Session()

def send_email(recipient, company_name):#please change the body according to your needs plus change the resume inside the assets folder 
    # 1. Subject Line
    subject = "Python Internship Application"
    
    # 2. Body with GitHub Link
    body = f"""\
Dear Hiring Team at {company_name},

I am writing to express my interest in the Python Developer Internship position at {company_name}.

I have strong technical skills in Python, specifically in backend, automation, web scraping, and data handling. 

I have attached my resume and GitHub profile for your review.

GitHub: https://github.com/lolvansh

Best regards,
Vansh Pandya
"""
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg.set_content(body)

    # 3. Attach Resume
    try:
        with open(RESUME_FILENAME, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(RESUME_FILENAME)
            # Guess the MIME type (e.g., application/pdf)
            maintype, subtype = mimetypes.guess_type(file_name)[0].split('/', 1)
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
    except Exception as e:
        print(f"  ❌ Resume Error: {e}")
        return False

    # 4. Sending Logic
    if TEST_MODE:
        print(f"  [TEST] Sending to: {recipient} | Subject: {subject}")
        return True

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"  ❌ SMTP Error: {e}")
        return False
    
    
def main():
    if not os.path.exists(RESUME_FILENAME):
        print(f"CRITICAL: {RESUME_FILENAME} not found.")
        return


    pending_apps = session.query(Application).filter(
        Application.status == 'pending',
        Application.target_email != None
    ).limit(DAILY_LIMIT).all()

    if not pending_apps:
        print("No pending applications found! You are all caught up.")
        return

    print(f"Found {len(pending_apps)} pending applications.")
    print(f"Mode: {'TEST (Safe)' if TEST_MODE else 'LIVE (Sending)'}\n")

    for i, app in enumerate(pending_apps, 1):
        print(f"[{i}/{len(pending_apps)}] Processing: {app.company_name}")
        
        success = send_email(app.target_email, app.company_name)
        
        if success:
            if not TEST_MODE:
                # Update status in DB using ORM
                app.status = 'sent'
                app.sent_at = datetime.now()
                session.commit() # Save changes
                print("  ✅ Sent & Saved.")
                
                # Random spam-prevention delay
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"Sleeping {delay}s...")
                time.sleep(delay)
        else:
            if not TEST_MODE:
                app.status = 'failed'
                session.commit()
                print("  ❌ Marked as failed.")

    print("\nBatch Complete.")

if __name__ == "__main__":
    main()