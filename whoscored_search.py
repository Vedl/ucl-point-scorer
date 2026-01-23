from duckduckgo_search import DDGS
try:
    from googlesearch import search as google_search
except ImportError:
    google_search = None
import time
import re

def clean_team_name(name):
    # Common prefixes/suffixes to remove for better search results
    remove_words = ["FC", "Royale", "CF", "AS", "AC", "Real", "Sporting", "Club", "Olympique"]
    
    cleaned = name
    for w in remove_words:
        cleaned = cleaned.replace(w, "").strip()
    
    # English mappings for WhoScored compatibility
    name_map = {
        "FC Bayern München": "Bayern Munich",
        "Bayern München": "Bayern Munich",
        "Bayern": "Bayern Munich",
        "Royale Union Saint-Gilloise": "Union St. Gilloise",
        "Union Saint-Gilloise": "Union St. Gilloise",
        "Union SG": "Union St. Gilloise",
        "Bayer 04 Leverkusen": "Bayer Leverkusen",
        "Leverkusen": "Bayer Leverkusen",
        "Sporting CP": "Sporting",
        "PSV Eindhoven": "PSV",
        "Club Brugge KV": "Club Brugge",
        "Sturm Graz": "Sturm Graz",
        "Salzburg": "Red Bull Salzburg",
        "FC Salzburg": "Red Bull Salzburg",
        "Sparta Praha": "Sparta Prague",
        "Slovan Bratislava": "Slovan Bratislava",
        "Crvena zvezda": "Red Star Belgrade",
        "Shakhtar Donetsk": "Shakhtar",
        "Dinamo Zagreb": "Dinamo Zagreb",
        "Young Boys": "Young Boys", 
        "Bologna": "Bologna",
        "Brest": "Brest", 
        "Girona": "Girona",
        "Stuttgart": "VfB Stuttgart",
        "VfB Stuttgart": "VfB Stuttgart",
        "Dortmund": "Borussia Dortmund",
        "Borussia Dortmund": "Borussia Dortmund",
        "RB Leipzig": "RB Leipzig",
        "Real Madrid": "Real Madrid",
        "Barcelona": "Barcelona",
        "Atletico Madrid": "Atletico Madrid",
        "Manchester City": "Man City",
        "Arsenal": "Arsenal",
        "Aston Villa": "Aston Villa",
        "Liverpool": "Liverpool",
        "Inter": "Inter",
        "Milan": "AC Milan",
        "AC Milan": "AC Milan",
        "Juventus": "Juventus",
        "Atalanta": "Atalanta",
        "Paris Saint-Germain": "PSG",
        "PSG": "PSG",
        "Monaco": "Monaco",
        "Lille": "Lille",
        "Benfica": "Benfica",
        "Feyenoord": "Feyenoord",
        "Celtic": "Celtic"
    }
    
    # 1. Try exact map
    if name in name_map:
        return name_map[name]
        
    # 2. Try cleaning
    cleaned = name.replace("FC", "").replace("Royale", "").replace("CF", "").replace("AS", "").strip()
    if cleaned in name_map:
        return name_map[cleaned]
        
    return cleaned

def cleanup_bing_url(url):
    # Bing sometimes returns google redirects or tracking links if parsed wrongly
    # But usually just the href
    return url

def find_match_url(home_team, away_team):
    """
    Find WhoScored match URL using multiple strategies.
    Now with English Name Mapping.
    """
    
    # 1. Prepare standardized names
    h_eng = clean_team_name(home_team)
    a_eng = clean_team_name(away_team)
    
    queries = [
        f"whoscored {h_eng} vs {a_eng}",
        f"whoscored {h_eng} vs {a_eng} champions league",
        f"whoscored {h_eng} {a_eng}"
    ]
    
    print(f"Searching match for {home_team} ({h_eng}) vs {away_team} ({a_eng})")
    
    def validate_url(url):
        if not url: return False
        if "whoscored.com" not in url: return False
        if "/Matches/" not in url: return False
        return True

    # Strategy 1: DDG Lite (Custom Scraper) - proven to work in restricted envs
    print("Strategy 1: DDG Lite HTML Scrape")
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    
    for q in queries:
        try:
            print(f"  DDG Lite Query: {q}")
            url = "https://lite.duckduckgo.com/lite/"
            data = {"q": q, "kl": "us-en"}
            
            resp = requests.post(
                url, 
                data=data, 
                impersonate="chrome120",
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
                timeout=10
            )
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'lxml')
                for a in soup.find_all('a', class_='result-link'):
                    href = a['href']
                    if validate_url(href):
                        print(f"FOUND via DDG Lite: {href}")
                        return href
        except Exception as e:
            print(f"DDG Lite error: {e}")
    # Strategy 2: Google Search (googlesearch-python)
    if google_search:
        print("Strategy 2: Google")
        for q in queries:
            try:
                # advanced=True returns objects with .url
                results = google_search(q, num_results=5, advanced=True)
                for r in results:
                    url = r.url
                    if validate_url(url):
                        print(f"FOUND via Google: {url}")
                        return url
            except Exception as e:
                pass
                
    # Strategy 3: Raw Bing HTML Scrape (Fallback)
    print("Strategy 3: Raw Bing Scrape")
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    import urllib.parse
    
    for q in queries:
        try:
            url_enc = urllib.parse.quote(q)
            b_url = f"https://www.bing.com/search?q={url_enc}"
            print(f"  Bing scraping: {b_url}")
            
            resp = requests.get(b_url, impersonate="chrome120")
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Find links
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    # Log potentially relevant links
                    if "whoscored" in href:
                        print(f"    Bing Candidate: {href}")
                        
                    if validate_url(href):
                         print(f"FOUND via Bing Raw: {href}")
                         return href
        except Exception as e:
             print(f"Bing Error: {e}")
    
    # Strategy 4: Team Fixtures Lookup (The "Nuclear Option")
    print("Strategy 4: Team Fixtures Page Lookup")
    # 1. Find Home Team Fixtures URL
    fixtures_url = None
    q_fixtures = f"WhoScored {h_eng} Fixtures"
    print(f"  Searching for fixtures: {q_fixtures}")
    
    try:
        # Reuse DDG Lite logic for fixtures
        url_lite = "https://lite.duckduckgo.com/lite/"
        data = {"q": q_fixtures, "kl": "us-en"}
        resp = requests.post(
            url_lite, 
            data=data, 
            impersonate="chrome120",
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
            timeout=10
        )
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')
            for a in soup.find_all('a', class_='result-link'):
                href = a['href']
                # Search for any Team URL: /Teams/123/
                # Could be /Show/ or /Fixtures/ or /History/ etc.
                match = re.search(r'/Teams/(\d+)/', href)
                if match:
                    tid = match.group(1)
                    # Construct generic fixtures URL to avoid language/slug issues
                    # "https://www.whoscored.com/Teams/{id}/Fixtures"
                    # We can leave the final slug empty or putting "Team" works
                    fixtures_url = f"https://www.whoscored.com/Teams/{tid}/Fixtures"
                    print(f"  Found Team ID: {tid} -> {fixtures_url}")
                    break
    except Exception as e:
        print(f"  Fixtures search error: {e}")
        
    if fixtures_url:
        # 2. Scrape Fixtures Page for Opponent
        try:
             print(f"  Scraping fixtures page: {fixtures_url}")
             f_resp = requests.get(fixtures_url, impersonate="chrome120", headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
             if f_resp.status_code == 200:
                 # Regex for match data: [12345, ... 'OpponentName', ...]
                 
                 lines = f_resp.text.split('\n')
                 # Search terms
                 search_terms = [a_eng, away_team, "Union", "St. Gilloise", "Union SG", "Pafos", "Pafos FC"]
                 
                 found_id = None
                 for line in lines:
                     # Identify a data line? they start with ,[
                     # REMOVED "Champions League" check to be generic
                     if ",[" in line: 
                         # Check opponent
                         for term in search_terms:
                             if term in line:
                                 # Extract ID (first number after [)
                                 # Line example: ,[1946356,1,'21-01-26'...
                                 match = re.search(r',\[(\d+),', line)
                                 if match:
                                     found_id = match.group(1)
                                     print(f"  Found Match ID in fixtures: {found_id} (Matched '{term}')")
                                     break
                     if found_id: break
                
                 if found_id:
                     final_url = f"https://www.whoscored.com/Matches/{found_id}/Live"
                     print(f"FOUND via Team Fixtures: {final_url}")
                     return final_url
                     
        except Exception as e:
            print(f"  Fixtures page scrape error: {e}")

    print("All search strategies failed.")
    return None
