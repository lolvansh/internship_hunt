import requests
from bs4 import BeautifulSoup
import re
import json
import time
import concurrent.futures

def extract_emails_from_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text(separator=' ')
        
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
        mailto_emails = [link['href'].replace('mailto:', '').split('?')[0] for link in mailto_links]
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text_emails = re.findall(email_pattern, page_text)
        
        all_emails = list(set(mailto_emails + text_emails))
        
        filtered_emails = [
            email for email in all_emails 
            if not any(spam in email.lower() for spam in ['example.com', 'test.com', 'domain.com', 'email.com', 'sentry.io'])
        ]
        
        return filtered_emails
    
    except Exception as e:
        print(f"    Error: {e}")
        return []
    
    
def find_company_emails(website):
    if not website:
        return []
    
    if not website.startswith('http'):
        website = 'https://' + website
        
    website = website.rstrip('/')
    
    pages_to_check = [
        website + '/contact',
        website + '/contact-us',
        website + '/about',
        website + '/about-us',
        website,  
    ]
    
    all_emails = []
    for page_url in pages_to_check:
        print(f"Checking: {page_url}")
        emails = extract_emails_from_page(page_url)
        
        if emails:
            print(f"Found: {', '.join(emails)}")
            all_emails.extend(emails)
            break 
        time.sleep(0.5)
        
    unique_emails = list(set(all_emails))
    
    priority_emails = [e for e in unique_emails if 'hr@' in e.lower() or 'career' in e.lower()]
    if priority_emails:
        return priority_emails
    
    return unique_emails


def process_single_company(company):
    name = company.get('name', 'Unknown')
    website = company.get('website')
    if not website:
        company['emails'] = []
        return company
    
    emails = find_company_emails(website)
    company['emails'] = emails
    return company
    
    

def main():
    input_file = 'comapany_with_no_emails.json'
    output_file = 'companies_with_emails.json'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        return
    
    total_companies = len(companies)
    print(f"Found {len(companies)} companies\n")
    
    processed_companies = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_company = {
            executor.submit(process_single_company, company): company for company in companies
        }
        completed_count = 0
        
        for future in concurrent.futures.as_completed(future_to_company):
            company = future_to_company[future]
            try:
                result = future.result()
                processed_companies.append(result)
                completed_count += 1
                name = result.get('name')
                email_count = len(result.get('emails', []))
                print(f"[{completed_count}/{total_companies}] {name}: Found {email_count} emails")
            except Exception as exc:
                print(f"Generated an exception for {company.get('name')}: {exc}")
                
        
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_companies, f, indent=4, ensure_ascii=False)
        
    companies_with_emails = [c for c in processed_companies if c.get('emails')]
    print(f"Done! Found emails for {len(companies_with_emails)} out of {total_companies} companies.")
     
     
     
if __name__ == '__main__':
    main()   