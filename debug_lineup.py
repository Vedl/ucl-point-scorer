
from curl_cffi import requests
import json

def inspect_lineups(match_id):
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    try:
        response = requests.get(url, impersonate="chrome120")
        if response.status_code == 200:
            data = response.json()
            # Print keys in 'home' to see if there is 'players', 'lineup', 'subs'
            print("Home Keys:", data['home'].keys())
            
            # Check separate lists
            if 'players' in data['home']:
                print(f"Num 'players': {len(data['home']['players'])}")
                # Check first player sample
                print("Sample Player:", json.dumps(data['home']['players'][0], indent=2))
                
            # Check for explicitly 'lineup' or 'substitutes' keys if 'players' isn't the only one
            # (Sometimes 'players' contains everyone, sometimes it's split)
            # Actually, standard SofaScore structure usually has 'players' as a list, 
            # and each player object has 'substitute': boolean field.
            
    except Exception as e:
        print(f"Error: {e}")

# Use a recent match ID (from the screenshot or history)
# Match ID from previous successful run in app logs: 12173509 (Bayern vs Union)
# Or from URL in screenshot: 14566573 (Union SG vs Bayern)
inspect_lineups(14566573)
