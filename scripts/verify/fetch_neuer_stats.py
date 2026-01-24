
from curl_cffi import requests
import json

url = 'https://api.sofascore.com/api/v1/event/14566573/lineups'
res = requests.get(url, impersonate='chrome120')
data = res.json()

print("Away Team Players (Bayern):")
for p in data['away']['players']:
    name = p['player']['name']
    pos = p.get('position', '?')
    is_sub = p.get('substitute', False)
    if pos == 'G':
        stats = p.get('statistics', {})
        print(f"\n{name} (sub={is_sub}):")
        print(f"  saves: {stats.get('saves', 0)}")
        print(f"  goalsConceded: {stats.get('goalsConceded', 0)}")
        print(f"  goodHighClaim: {stats.get('goodHighClaim', 0)}")
        print(f"  totalKeeperSweeper: {stats.get('totalKeeperSweeper', 0)}")
        print(f"  ballRecovery: {stats.get('ballRecovery', 0)}")
        print(f"  accuratePass: {stats.get('accuratePass', 0)}")
        print(f"  totalClearance: {stats.get('totalClearance', 0)}")
        print(f"  ownGoals: {stats.get('ownGoals', 0)}")
        print(f"  punches: {stats.get('punches', 0)}")
        print(f"  minutesPlayed: {stats.get('minutesPlayed', 0)}")
