from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def ddg_lite_search(query):
    url = "https://lite.duckduckgo.com/lite/"
    print(f"Scraping DDG Lite: {query}")
    
    try:
        data = {
            "q": query,
            "kl": "us-en" # Region/Language
        }
        
        response = requests.post(
            url,
            data=data,
            impersonate="chrome120",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://lite.duckduckgo.com/"
            },
            timeout=10
        )
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # In Lite, results are often in table rows
        # <a class="result-link" href="...">
        
        candidates = []
        for a in soup.find_all('a', class_='result-link'):
            href = a['href']
            print(f"  Candidate: {href}")
            if "whoscored.com/Matches" in href:
                print(f"FOUND: {href}")
                candidates.append(href)
        
        return candidates

    except Exception as e:
        print(f"Error scraping DDG Lite: {e}")
        return []

if __name__ == "__main__":
    queries = [
        "WhoScored Chelsea Fixtures",
        "whoscored.com Chelsea Fixtures",
        "WhoScored Chelsea"
    ]
    for q in queries:
        ddg_lite_search(q)
