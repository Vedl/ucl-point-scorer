from curl_cffi import requests
import urllib.parse

def test_internal_search(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.whoscored.com/Search/?t={encoded}"
    print(f"Fetching {url}...")
    
    try:
        response = requests.get(url, impersonate="chrome120")
        print(f"Status: {response.status_code}")
        
        if "Bayern" in response.text:
            print("Found 'Bayern' in text")
        
        # Look for match links
        # Usually they are like:
        # href="/Matches/..."
        import re
        links = re.findall(r'href="(/Matches/[^"]+)"', response.text)
        print(f"Found {len(links)} match links")
        for l in links[:5]:
            print(f" - {l}")
            
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    test_internal_search("Bayern Union SG")
