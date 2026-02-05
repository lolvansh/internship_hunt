import json

JSON_PATH = r"D:\python\cloud-cli\companies_final.json"

NEW_PATH = r"D:\python\cloud-cli\trial.json"

if __name__ == '__main__':
    companies = {}
    new_dict = []
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            companies = json.load(f)
    except Exception as e:
        print(e)
        
    for i in range(5):
        new_dict.append(companies[i])

    

            
    try:
        with open(NEW_PATH, 'w', encoding='utf-8') as f:
            json.dump(new_dict,f, indent=2, sort_keys=True)
    except Exception as e:
        print("bleh")
                    
                    