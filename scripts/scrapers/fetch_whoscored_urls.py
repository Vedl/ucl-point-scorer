"""
Script to fetch WhoScored GW5 Match URLs directly.
"""
from curl_cffi import requests
import re
import json

def fetch_gw5_urls():
    # URL found in previous browser logs for UCL 2025/26
    # We need to find the specific match IDs for Round 5 (Nov 25-27)
    
    # Try fetching the fixtures page
    url = "https://www.whoscored.com/Regions/250/Tournaments/12/Seasons/10531/Stages/24252/Fixtures/Europe-Champions-League-2025-2026"
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
            
            # Extract match data from initial data JSON often found in script tags
            # Format: "matches": [ ... ]
            
            # Simple regex to find match links with dates
            # Looking for matches in November 2025
            
            # Pattern for match links: /Matches/(\d+)/Live/...
            # And usually around it is the date or team names
            
            # Let's find all match links first
            matches = []
            seen_ids = set()
            
            # Regex to capture ID and Slug
            # href="/Matches/1946419/Live/Europe-Champions-League-2025-2026-Napoli-Eintracht-Frankfurt"
            pattern = r'href="(/Matches/(\d+)/(?:Live|Show|Preview)/[^"]+)"'
            
            for match in re.finditer(pattern, html, re.IGNORECASE):
                full_path = match.group(1)
                match_id = match.group(2)
                
                if match_id in seen_ids:
                    continue
                seen_ids.add(match_id)
                
                # Check if it's likely a GW5 match (Nov 2025)
                # This is hard without parsing the DOM structure vs text position
                # But we know the teams!
                
                url = "https://www.whoscored.com" + full_path
                matches.append({'id': match_id, 'url': url})
            
            print(f"Found {len(matches)} match links.")
            
            # Filter for our specific teams
            target_teams = [
                "Benfica", "Ajax", "Union", "Galatasaray", "Juventus", "Bodo", "Glimt",
                "Villarreal", "Dortmund", "Barcelona", "Chelsea", "Leverkusen", "City",
                "Qarabag", "Napoli", "Marseille", "Newcastle", "Slavia", "Athletic",
                "Copenhagen", "Kairat", "Pafos", "Monaco", "Arsenal", "Bayern",
                "Atletico", "Inter", "Frankfurt", "Atalanta", "Liverpool", "PSV",
                "Olympiacos", "Real", "PSG", "Tottenham", "Sporting", "Brugge"
            ]
            
            gw5_matches = []
            for m in matches:
                url_lower = m['url'].lower()
                for team in target_teams:
                    if team.lower() in url_lower:
                        gw5_matches.append(m)
                        break
            
            print(f"Potential GW5 Matches found: {len(gw5_matches)}")
            for m in gw5_matches:
                print(f"  {m['url']}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_gw5_urls()
