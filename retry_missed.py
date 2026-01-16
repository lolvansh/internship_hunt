import json
import re
import time
from playwright.sync_api import sync_playwright

INPUT_FILE = 'companies_with_emails.json'
OUTPUT_FILE = 'companies_final.json'

def get_emails_with_browser(page, url):
    print(f"  Visiting: {url}")
    
    try:
        page.goto(url, timeout=15000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        content = page.content()
        visible_text = page.inner_text('body')
        full_text = content + " " + visible_text
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        found_emails = re.findall(email_pattern, full_text)
        filtered_emails = list(set([
            e for e in found_emails 
            if not any(spam in e.lower() for spam in ['example.com', 'wix.com', 'sentry.io', '.png', '.jpg', '.gif'])
        ]))

        return filtered_emails
    except Exception as e:
        print(f"Error on {url}: {str(e)[:50]}...")
        return []
    
def javascript_scan(company, page):
    website = company.get('website')
    if not website:
        return []

    if not website.startswith('http'):
        website = 'https://' + website
    website = website.rstrip('/')
    
    urls_to_check = [
        website,
        website + '/contact',
        website + '/contact-us',
    ]
    all_emails = []
    
    for url in urls_to_check:
        emails = get_emails_with_browser(page, url)
        if emails:
            all_emails.extend(emails)
            # If we found emails, we can stop
            break 
            
    return list(set(all_emails))


def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_FILE}. Run the previous script first.")
        return
    
    missed_companies = [c for c in companies if not c.get('emails')]
    print(f"Loaded {len(companies)} companies.")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for i, company in enumerate(missed_companies, 1):
            name = company.get('name')
            print(f"[{i}/{len(missed_companies)}]")
            
            emails = javascript_scan(company, page)
            
            if emails:
                print(f"SUCCESS: Found {len(emails)} emails! {emails}")
                company['emails'] = emails 
            else:
                print("Still no emails found.")
            
            print("-" * 30)
            
        browser.close()
    print(f"Saving updated list to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(companies, f, indent=4, ensure_ascii=False)
    
    print("Done!")
    
        
if __name__ == '__main__':
    main()