"""
Test Automated WhoScored URL Discovery via DuckDuckGo Lite
"""
from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def search_whoscored(home_team, away_team):
    query = f"site:whoscored.com/Matches/ Champions League {home_team} {away_team} 2025"
    encoded_query = urllib.parse.quote(query)
    url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
    
    print(f"Searching: {query}")
    
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://lite.duckduckgo.com/"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', class_='result-link')
            
            for link in links:
                href = link.get('href', '')
                # Check if it's a match link
                # Format: https://www.whoscored.com/Matches/12345/Live/Team-vs-Team
                if "whoscored.com/Matches/" in href and "/Live" in href:
                    print(f"Found: {href}")
                    return href
                    
        else:
            print(f"Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return None

if __name__ == "__main__":
    # Test cases
    search_whoscored("Benfica", "Ajax") # GW5
    search_whoscored("Chelsea", "Barcelona") # GW5
    search_whoscored("Arsenal", "Bayern") # GW5
