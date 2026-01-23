from curl_cffi import requests
from bs4 import BeautifulSoup
import re

def examine_team_fixtures():
    url = "https://www.whoscored.com/Teams/37/Fixtures/Germania-Bayern-Munich"
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        response = requests.get(url, impersonate="chrome120", headers=headers)
        print(f"Status: {response.status_code}")
        
        with open("team_fixtures_debug.html", "w") as f:
            f.write(response.text)
        print("Saved to team_fixtures_debug.html")
        
        # The fixtures might be in a script tag or simple HTML
        # Checking HTML first
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text()
            
            if "/Matches/" in href and ("Union" in text or "SG" in text or "Union" in href):
                print(f"FOUND MATCH: {text} -> {href}")
                
            # Also check if just "Union" is in the row text
            # This is harder to parse without context
        
        # Check raw text for regex
        if "Union" in response.text:
            print("Found 'Union' in text")
            
        matches = re.findall(r'href="(/Matches/[^"]+)"', response.text)
        print(f"Found {len(matches)} match links total")
        for m in matches:
            if "Union" in m:
                print(f"Regex Found: {m}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    examine_team_fixtures()
