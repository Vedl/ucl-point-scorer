from curl_cffi import requests
from io import StringIO
import time
import random

def inspect():
    url = "https://fbref.com/en/matches/0c4a45a0/Liverpool-Real-Madrid-November-27-2024-Champions-League"
    print(f"Fetching {url}...")
    
    browsers = ["chrome110", "safari15_3", "edge101"]
    
    for browser in browsers:
        print(f"Trying {browser}...")
        try:
            r = requests.get(url, impersonate=browser, headers={
                "Referer": "https://fbref.com/",
                "Accept-Language": "en-US,en;q=0.9"
            })
            if r.status_code == 200:
                print(f"Success with {browser}!")
                html = r.text
                break
            else:
                print(f"Failed with {browser}: {r.status_code}")
                time.sleep(2)
        except Exception as e:
            print(f"Error with {browser}: {e}")
            
    else:
        print("All attempts failed.")
        return
    
    # Pre-cleaning: FBRef comments out some tables to save bandwidth? 
    # Sometimes they do <!-- table code -->. We might need to uncomment them.
    # Let's simple replace "<!--" and "-->" if we suspect tables are hidden.
    # But often read_html finds the main ones.
    
    # Actually, FBRef often puts extra tables in comments. 
    # Let's try reading without modification first.
    
    try:
        tables = pd.read_html(StringIO(html))
        print(f"Found {len(tables)} tables directly.")
        for idx, df in enumerate(tables):
            print(f"\n--- Table {idx} ---")
            # Print columns (handle multi-index)
            print("Columns:", df.columns.tolist())
            print(df.head(3).to_string())
            
    except Exception as e:
        print(f"Direct read failed: {e}")

    # Now let's try to find commented tables
    clean_html = html.replace('<!--', '').replace('-->', '')
    try:
        tables_full = pd.read_html(StringIO(clean_html))
        print(f"\n\nFound {len(tables_full)} tables after uncommenting.")
        # Just list their potential names/headers to identify them
        for idx, df in enumerate(tables_full):
            if isinstance(df.columns, pd.MultiIndex):
                top_level = set([c[0] for c in df.columns])
                print(f"Table {idx}: {top_level}")
            else:
                print(f"Table {idx}: {df.columns.tolist()[:3]}...")
                
    except Exception as e:
        print(f"Uncommented read failed: {e}")

if __name__ == "__main__":
    inspect()
