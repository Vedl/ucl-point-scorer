from curl_cffi import requests

def fetch_and_save():
    url = "https://www.whoscored.com/Regions/250/Tournaments/12/Seasons/10531/Stages/24252/Fixtures/Europe-Champions-League-2025-2026"
    print(f"Fetching {url}...")
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        )
        with open("debug_fixtures.html", "w") as f:
            f.write(response.text)
        print("Saved to debug_fixtures.html")
        
        # Quick check
        if "Bayern" in response.text:
            print("Found 'Bayern' in text")
        else:
            print("'Bayern' NOT found in text")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save()
