
import requests
import json

def inspect_json():
    match_id = "14566854"
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    
    print(f"Fetching JSON for: {url}")
    try:
        # Use simple requests with headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.sofascore.com/" 
        }
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Failed: {res.status_code}")
            # Try curl_cffi if simple fails
            from curl_cffi import requests as cffi_requests
            res = cffi_requests.get(url, impersonate="chrome120")
            
        data = res.json()
        
        # Find Chevalier (Away team)
        cheva = None
        for p in data['away']['players']:
            if "Chevalier" in p['player']['name']:
                cheva = p
                break
        
        if cheva:
            print(json.dumps(cheva, indent=2))
        else:
            print("Chevalier not found in JSON line-ups.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_json()
