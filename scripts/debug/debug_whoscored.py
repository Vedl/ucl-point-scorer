"""Debug script to analyze WhoScored HTML structure."""
from curl_cffi import requests
import re

url = "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"

response = requests.get(
    url,
    impersonate="chrome120",
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.whoscored.com/',
    }
)

html = response.text
print(f"HTML length: {len(html)}")

# Save to file for inspection
with open("whoscored_debug.html", "w") as f:
    f.write(html)

# Look for player names we know exist
targets = ['Ryerson', 'Svensson', 'Foden', 'Haaland', 'Donnarumma']
for t in targets:
    if t in html:
        # Find context around the name
        idx = html.find(t)
        context = html[max(0, idx-100):idx+200]
        print(f"\n--- Found {t} at index {idx} ---")
        print(context[:300])
    else:
        print(f"{t}: NOT FOUND in HTML")

# Look for position codes
pos_codes = ['DMR', 'DML', 'DMC', 'AMC', 'FW']
for code in pos_codes:
    count = html.count(code)
    if count > 0:
        idx = html.find(code)
        context = html[max(0, idx-50):idx+50]
        print(f"\n--- Found {code} ({count}x) ---")
        print(context)
