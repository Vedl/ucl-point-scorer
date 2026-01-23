"""
Deep Inspect SofaScore API JSON to find 'hitWoodwork' stat.
"""
from sofascore_adapter import fetch_sofascore_data, get_match_id
import json

def inspect():
    # Try a few matches
    # Liverpool vs Real Madrid (GW5, high profile) -> Maybe cached ID?
    # Let's use the one we have: 14566874 (Benfica Ajax)
    
    ids = [14566874]
    
    for mid in ids:
        print(f"Checking Match ID: {mid}")
        try:
            data = fetch_sofascore_data(mid, "lineups")
            
            found_keys = set()
            
            for team in ['home', 'away']:
                if team in data:
                    for p in data[team]['players']:
                        stats = p.get('statistics', {})
                        for k in stats.keys():
                            if 'wood' in k.lower() or 'post' in k.lower():
                                print(f"FOUND in {p['player']['name']}: {k} = {stats[k]}")
                            
                            found_keys.add(k)
                            
            if 'hitWoodwork' in found_keys:
                print("Confirmed: hitWoodwork is a valid key!")
            else:
                print("Key 'hitWoodwork' NOT found in any player.")
                # print("All keys found:", sorted(list(found_keys)))
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
