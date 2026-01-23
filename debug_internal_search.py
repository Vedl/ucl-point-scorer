from curl_cffi import requests
import urllib.parse

def debug_internal_search():
    # Search for "Union SG" or "Bayern"
    # let's try "Bayern" as it's simpler
    query = "Bayern"
    url = f"https://www.whoscored.com/Search/?t={query}"
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.whoscored.com/",
    }
    try:
        response = requests.get(url, impersonate="chrome120", headers=headers)
        print(f"Status: {response.status_code}")
        with open("internal_search_debug.html", "w") as f:
            f.write(response.text)
        print("Saved to internal_search_debug.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_internal_search()
