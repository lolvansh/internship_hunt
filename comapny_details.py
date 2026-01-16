import requests
import os
from dotenv import load_dotenv
import json
import time


load_dotenv()

import requests
import os
from dotenv import load_dotenv  


load_dotenv()

def get_place_info(query, api_key, max_results):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": query,
        "key": api_key,
        
    }
    all_results = []
    
    while len(all_results) < max_results:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data.get('status') == 'OK':
            all_results.extend(data.get('results', []))
            print(f"Got {len(all_results)} companies so far...")
            
            next_page_token = data.get('next_page_token')
            if not next_page_token:
                break
            
            time.sleep(2)
            params = {
                "pagetoken": next_page_token,
                "key": api_key
            }
        else:
            break 
    return all_results
            
    

    
def get_place_details(place_id, api_key):
    
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,website,formatted_phone_number", 
        "key": api_key
    }
    try:
        response = requests.get(base_url, params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    

if __name__ == '__main__':
    api_key = os.environ.get('API_KEY')
    query = "software companies in Adajan, Surat"
    
    if not api_key:
        print("Error: API Key not found.")
    else:

        results = get_place_info(query, api_key, max_results=60)  
        
        if results:  
            print(f"Total companies found: {len(results)}")
            
            companies_with_websites = []
            
            for place in results:
                place_id = place.get('place_id')
                name = place.get('name')
                
                print(f"Getting details for: {name}")
                
                place_details = get_place_details(place_id, api_key)
                
                if place_details and place_details.get('status') == 'OK':
                    companies_with_websites.append(place_details.get('result', {}))
                
                time.sleep(0.2)
            
            # Save to file
            file_name = 'companies.json'
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(companies_with_websites, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Saved {len(companies_with_websites)} companies to {file_name}")
        else:
            print("No companies found!")