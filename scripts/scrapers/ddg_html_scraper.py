from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def ddg_html_search(query):
    url = "https://html.duckduckgo.com/html/"
    print(f"Scraping DDG HTML: {query}")
    
    try:
        response = requests.post(
            url,
            data={"q": query},
            impersonate="chrome120",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://html.duckduckgo.com/"
            },
            timeout=10
        )
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        candidates = []
        for a in soup.find_all('a', class_='result__a'):
            href = a['href']
            if "whoscored.com/Matches" in href:
                print(f"Found candidate: {href}")
                candidates.append(href)
        
        return candidates

    except Exception as e:
        print(f"Error scraping DDG: {e}")
        return []

if __name__ == "__main__":
    links = ddg_html_search("WhoScored Bayern München vs Union SG Champions League")
    for l in links:
        print(l)
