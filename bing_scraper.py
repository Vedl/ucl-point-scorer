from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def bing_search_scrape(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q={encoded}"
    print(f"Scraping Bing: {url}")
    
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            timeout=10
        )
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        candidates = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "whoscored.com/Matches" in href:
                print(f"Found candidate: {href}")
                candidates.append(href)
        
        return candidates

    except Exception as e:
        print(f"Error scraping Bing: {e}")
        return []

if __name__ == "__main__":
    links = bing_search_scrape("WhoScored Bayern München vs Union SG")
    for l in links:
        print(l)
