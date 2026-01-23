from curl_cffi import requests

def debug_bing():
    url = "https://www.bing.com/search?q=WhoScored+Bayern+Munchen+vs+Union+SG"
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        response = requests.get(url, impersonate="chrome120", headers=headers)
        print(f"Status: {response.status_code}")
        with open("bing_debug.html", "w") as f:
            f.write(response.text)
        print("Saved to bing_debug.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_bing()
