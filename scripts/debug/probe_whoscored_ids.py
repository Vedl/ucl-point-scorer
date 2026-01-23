"""
Script to probe WhoScored Match IDs to find GW5 matches.
GW4 ended at 1946487. Probing upwards.
"""
from curl_cffi import requests
import time

def probe_matches():
    start_id = 1946488
    end_id = start_id + 50 # Probe 50 IDs
    
    matches_found = []
    
    print(f"Probing IDs {start_id} to {end_id}...")
    
    for match_id in range(start_id, end_id):
        url = f"https://www.whoscored.com/Matches/{match_id}/Live"
        
        try:
            # We use a HEAD request or GET with small range to be fast? 
            # WhoScored might block HEAD. Let's use GET but stop early if not 200.
            # actually, just getting the title is enough.
            
            response = requests.get(
                url,
                impersonate="chrome120",
                timeout=5
            )
            
            if response.status_code == 200:
                html = response.text
                if "<title>" in html:
                    title_start = html.find("<title>") + 7
                    title_end = html.find("</title>")
                    title = html[title_start:title_end].strip()
                    
                    if "Champions League" in title or " - " in title:
                        print(f"FOUND {match_id}: {title}")
                        matches_found.append({'id': match_id, 'title': title, 'url': url})
                    else:
                        print(f"  {match_id}: {title[:30]}...")
            else:
                print(f"  {match_id}: Status {response.status_code}")
                
        except Exception as e:
            print(f"  {match_id}: Error {e}")
            
        time.sleep(0.5) # Be gentle
        
        if len(matches_found) >= 18:
            break
            
    print(f"\nTotal matches found: {len(matches_found)}")
    for m in matches_found:
        print(f"  {m['id']} -> {m['url']}")

if __name__ == "__main__":
    probe_matches()
