"""
Script to fetch WhoScored GW5 Match URLs - Attempt 2
Uses canonical URL and searches for JSON data.
"""
from curl_cffi import requests
import re
import json

def fetch_gw5_urls():
    # Canonical URL from previous response
    url = "https://www.whoscored.com/regions/250/tournaments/12/seasons/10903/stages/24797/fixtures/europe-champions-league-2025-2026"
    print(f"Fetching {url}...")
    
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            }
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            html = response.text
            
            # Save to file for debug if needed
            # with open("whoscored_debug.html", "w") as f:
            #     f.write(html)
            
            # Look for JSON data
            # Typically in <script> window.initialData = ... </script> or similar
            
            # Regex for JSON array of matches
            # "id":1946xxx ... "homeTeam": ...
            
            # Let's simple capture ALL match-like URLs
            # /Matches/1946419/Live/
            pattern = r'Matches/(\d+)/(?:Live|Show|Preview)'
            
            match_ids = set()
            for match in re.finditer(pattern, html, re.IGNORECASE):
                match_ids.add(match.group(1))
            
            print(f"Found {len(match_ids)} match IDs via regex.")
            
            if len(match_ids) > 0:
                print(list(match_ids)[:10])
                
                # If we found matches, we can construct the URLs!
                # We need to know WHICH match is which.
                # The text around the link usually helps.
                
                matches = []
                # Regex for full link: <a href="/Matches/123/Live/Team-vs-Team" ...>
                link_pattern = r'href="(/Matches/(\d+)/(?:Live|Show|Preview)/([^"]+))"'
                
                for match in re.finditer(link_pattern, html, re.IGNORECASE):
                    full_path = match.group(1)
                    match_id = match.group(2)
                    slug = match.group(3)
                    
                    matches.append({
                        'id': match_id,
                        'slug': slug,
                        'url': "https://www.whoscored.com" + full_path
                    })
                
                print(f"Found {len(matches)} detailed match links.")
                
                # Filter for GW5 teams
                target_teams = [
                    "Benfica", "Ajax", "Union", "Galatasaray", "Juventus", "Bodo", "Glimt",
                    "Villarreal", "Dortmund", "Barcelona", "Chelsea", "Leverkusen", "City",
                    "Qarabag", "Napoli", "Marseille", "Newcastle", "Slavia", "Athletic",
                    "Copenhagen", "Kairat", "Pafos", "Monaco", "Arsenal", "Bayern",
                    "Atletico", "Inter", "Frankfurt", "Atalanta", "Liverpool", "PSV",
                    "Olympiacos", "Real", "PSG", "Tottenham", "Sporting", "Brugge"
                ]
                
                gw5_matches = []
                seen = set()
                
                for m in matches:
                    if m['id'] in seen: continue
                    seen.add(m['id'])
                    
                    slug_lower = m['slug'].lower()
                    for team in target_teams:
                        if team.lower() in slug_lower:
                            gw5_matches.append(m)
                            break
                            
                print(f"Potential GW5 Matches found: {len(gw5_matches)}")
                for m in gw5_matches:
                    print(f"  {m['slug']} -> {m['url']}")
            
            else:
                print("No match IDs found. Checking for initialData...")
                # Try to extract JSON blob
                json_pattern = r'initialData\s*=\s*({.*?});'
                json_match = re.search(json_pattern, html, re.DOTALL)
                if json_match:
                    print("Found initialData JSON!")
                    # data = json.loads(json_match.group(1))
                    # print(data.keys())
                else:
                    print("No initialData found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_gw5_urls()
