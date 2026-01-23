from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def google_search_scrape(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    print(f"Scraping Google: {url}")
    
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.google.com/"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"Google status: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Look for links
        # Google structure is complex but usually hrefs inside <a> tags work
        
        # Pattern for WhoScored match
        # https://www.whoscored.com/Matches/12345/Live/...
        
        candidates = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "whoscored.com/Matches" in href:
                print(f"Found candidate: {href}")
                # Clean up if it's a google redirect (usually direct with curl_cffi on raw page?)
                if "/url?q=" in href:
                    href = href.split("/url?q=")[1].split("&")[0]
                
                candidates.append(urllib.parse.unquote(href))
        
        return candidates

    except Exception as e:
        print(f"Error scraping Google: {e}")
        return []

if __name__ == "__main__":
    links = google_search_scrape("WhoScored Bayern München vs Union SG Champions League")
    for l in links:
        print(l)
