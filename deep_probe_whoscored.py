"""
Deep Probe for WhoScored UCL GW5 Matches.
Range: 1946300 to 1946600
"""
from curl_cffi import requests
import concurrent.futures
import time

def check_match(match_id):
    url = f"https://www.whoscored.com/Matches/{match_id}/Live"
    try:
        response = requests.get(url, impersonate="chrome120", timeout=5)
        if response.status_code == 200:
            html = response.text
            if "<title>" in html:
                title_start = html.find("<title>") + 7
                title_end = html.find("</title>")
                title = html[title_start:title_end].strip()
                
                if "Champions League" in title and "2025/2026" in title:
                    return {'id': match_id, 'title': title, 'url': url}
    except:
        pass
    return None

def main():
    start_id = 1946300
    end_id = 1946600
    
    print(f"Probing IDs {start_id} to {end_id} with thread pool...")
    
    matches_found = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_match, mid): mid for mid in range(start_id, end_id)}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"FOUND {result['id']}: {result['title']}")
                matches_found.append(result)
                
    print(f"\nTotal UCL matches found: {len(matches_found)}")
    # Sort for easier reading
    matches_found.sort(key=lambda x: x['id'])
    
    for m in matches_found:
        print(f"  {m['id']} -> {m['title']}")

if __name__ == "__main__":
    main()
