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
    
    
def load_queries(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    all_queries = []
    for query in data.values():
        all_queries.extend(query)
    return all_queries
    

if __name__ == '__main__':
    
    api_key = os.environ.get('API_KEY')
    queries = load_queries('queries.json')
    
    if not api_key:
        print("Error: API Key not found.")
    else:
        all_companies = []
        seen_place_ids = set()
        duplicate_count = 0
        for query in queries:
            print(f"Searching for: {query}")
            results = get_place_info(query, api_key, max_results=60)
            
            if results:
                for place in results:
                    place_id = place.get('place_id')
                    name = place.get('name')
                    
                    if place_id in seen_place_ids:
                        duplicate_count += 1
                        continue
                    place_details = get_place_details(place_id, api_key)
                    
                    if place_details and place_details.get('status') == 'OK':
                        details = place_details.get('result', {})
                        all_companies.append(details)
                        seen_place_ids.add(place_id)
                        
                    time.sleep(0.2)
            else:
                print(f"No results found for {query}")
                
    file_name = 'comapany_with_no_emails.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(all_companies, f, indent=4, ensure_ascii=False)