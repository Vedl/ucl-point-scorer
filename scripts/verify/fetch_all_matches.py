
from curl_cffi import requests
import json
import time

tournament_id = 7
season_id = 76953

# Fetch matches for the season
# Endpoint pattern: unique-tournament/{id}/season/{id}/events/last/{page} implies paging backwards?
# Or just /events/rounds for a list of rounds?
# Let's try /events/last/0 to see what we get, or search for a rounds endpoint.
# Better yet, iterate rounds 1 to 8 (UCL League Phase has 8 rounds).

print(f"Fetching matches for UCL 25/26 (Season {season_id})...")

all_matches = []

# Fetch matches round by round (Round 1 to 8)
for round_num in range(1, 9):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/events/round/{round_num}"
    try:
        res = requests.get(url, impersonate='chrome120')
        if res.status_code != 200:
            print(f"Round {round_num}: Status {res.status_code}")
            continue
            
        data = res.json()
        events = data.get('events', [])
        print(f"Round {round_num}: Found {len(events)} matches")
        
        for evt in events:
            if evt.get('status', {}).get('type') == 'finished':
                match_id = evt.get('id')
                slug = evt.get('slug')
                home = evt.get('homeTeam', {}).get('name')
                away = evt.get('awayTeam', {}).get('name')
                all_matches.append({
                    'id': match_id,
                    'slug': slug,
                    'home': home,
                    'away': away,
                    'round': round_num
                })
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error fetching round {round_num}: {e}")

print(f"\nTotal Finished Matches Found: {len(all_matches)}")

# Save to file for next step
with open("ucl_matches.json", "w") as f:
    json.dump(all_matches, f, indent=2)
