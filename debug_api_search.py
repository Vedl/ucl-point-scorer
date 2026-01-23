from curl_cffi import requests
import json

def debug_api():
    endpoints = [
        "https://www.whoscored.com/AutoComplete/Search?t=Bayern",
        "https://www.whoscored.com/Search/Search?t=Bayern",
        "https://www.whoscored.com/api/Search?t=Bayern",
        "https://www.whoscored.com/statistics/search?t=Bayern"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.whoscored.com/",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    for url in endpoints:
        print(f"Trying {url}...")
        try:
            response = requests.get(url, impersonate="chrome120", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Type: {response.headers.get('Content-Type', '')}")
                if "json" in response.headers.get('Content-Type', ''):
                    print("JSON FOUND!")
                    print(response.text[:500])
                    break
                else:
                    print("Not JSON.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_api()
