
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from curl_cffi import requests

def fetch_gk_stats(match_id, match_name):
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    print(f"\n{'='*80}")
    print(f"Match: {match_name}")
    print(f"{'='*80}")
    
    try:
        res = requests.get(url, impersonate="chrome120")
        data = res.json()
        
        for team_key in ['home', 'away']:
            team_name = "Home" if team_key == 'home' else "Away"
            for p in data[team_key]['players']:
                if p.get('position') == 'G' and not p.get('substitute', False):
                    stats = p.get('statistics', {})
                    print(f"\n{team_name} GK: {p['player']['name']}")
                    print("-" * 40)
                    
                    # Key stats
                    print(f"  minutesPlayed: {stats.get('minutesPlayed', 0)}")
                    print(f"  saves: {stats.get('saves', 0)}")
                    print(f"  goalsConceded: {stats.get('goalsConceded', 0)}")
                    print(f"  goodHighClaim: {stats.get('goodHighClaim', 0)}")
                    print(f"  punches: {stats.get('punches', 0)}")
                    print(f"  totalKeeperSweeper: {stats.get('totalKeeperSweeper', 0)}")
                    print(f"  ballRecovery: {stats.get('ballRecovery', 0)}")
                    print(f"  accuratePass: {stats.get('accuratePass', 0)}")
                    print(f"  totalPass: {stats.get('totalPass', 0)}")
                    print(f"  totalClearance: {stats.get('totalClearance', 0)}")
                    print(f"  penaltySave: {stats.get('penaltySave', 0)}")
                    print(f"  rating: {stats.get('rating', 0)}")
                    
    except Exception as e:
        print(f"Error: {e}")

# Fetch both matches
fetch_gk_stats("14566821", "Marseille vs Liverpool")
fetch_gk_stats("14566854", "Sporting vs PSG (Chevalier)")
