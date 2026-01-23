"""
Inspect SofaScore API JSON to find 'hitWoodwork' stat.
"""
from sofascore_adapter import fetch_sofascore_data, get_match_id
import json

def inspect():
    # Use Benfica vs Ajax match ID (14566874 for example) or found valid ID
    # Use one from GW5 probe: 1946446 (WhoScored) mapped to 14566874 (SofaScore)
    # Match: Benfica vs Ajax
    url = "https://www.sofascore.com/football/match/benfica-afc-ajax/djbsgkb#id:14566874"
    mid = get_match_id(url)
    print(f"Match ID: {mid}")
    
    data = fetch_sofascore_data(mid, "lineups")
    
    # Check one player's stats
    if 'home' in data and 'players' in data['home']:
        p = data['home']['players'][0]
        stats = p.get('statistics', {})
        print("\nAvailable Stats Keys:")
        for k in sorted(stats.keys()):
            print(f"  {k}: {stats[k]}")
            
        # Check for specific terms
        print("\nSearching for 'woodwork' or 'post'...")
        found = False
        for k in stats.keys():
            if 'wood' in k.lower() or 'post' in k.lower():
                print(f"FOUND: {k} = {stats[k]}")
                found = True
        if not found:
            print("Not found in this player. Checking all players...")
            
            # Check all
            for team in ['home', 'away']:
                for p in data[team]['players']:
                    stats = p.get('statistics', {})
                    for k in stats.keys():
                        if 'wood' in k.lower() or 'post' in k.lower():
                            print(f"FOUND in {p['player']['name']}: {k} = {stats[k]}")
                            return

if __name__ == "__main__":
    inspect()
