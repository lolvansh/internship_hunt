import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_conn import Base, Application

# Config
DB_FILE = 'sqlite:///applications.db'
JSON_FILE = r'D:\python\cloud-cli\companies_final.json'

def get_best_email(email_list):
    if not email_list: return None
    emails = [e.strip().lower() for e in email_list]
    
    # Priority Logic
    for kw in ['hr@', 'career', 'job', 'talent', 'intern']:
        for e in emails:
            if kw in e: return e
    for kw in ['info@', 'hello@', 'contact@']:
        for e in emails:
            if kw in e: return e
    return emails[0]

def import_data():
    engine = create_engine(DB_FILE)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"Error: {JSON_FILE} not found!")
        return

    added = 0
    skipped = 0
    
    print(f"Scanning {len(companies)} companies from file...")
    
    for c in companies:
        name = c.get('name')
        website = c.get('website')
        emails = c.get('emails', [])
        
        # 1. Check if company exists in DB
        exists = session.query(Application).filter(
        (Application.company_name == name) | (Application.website == website)
    ).first()
        if exists:
            skipped += 1
            continue 
            
        # 2. Prepare new data

        best_email = get_best_email(emails)
        
        # 3. Add to session
        new_app = Application(
            company_name=name,
            website=website,
            all_emails=json.dumps(emails),
            target_email=best_email,
            status='pending'
        )
        session.add(new_app)
        added += 1
        
    # 4. Save all changes
    session.commit()
    print(f"Summary: Added {added} new leads. Skipped {skipped} existing.")

if __name__ == "__main__":
    import_data()