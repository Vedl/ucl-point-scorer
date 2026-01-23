"""
FAIR Position Accuracy Comparison: SofaScore vs WhoScored
Only compares players that BOTH sources have data for.
Excel is the GROUND TRUTH (100% correct for GW4)
"""
import pandas as pd
from curl_cffi import requests
import re
import time

# Load Excel ground truth
EXCEL_PATH = "Gameweek 4 UCL 25:26 Points.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()
print(f"Loaded {len(excel_df)} players from Excel (Ground Truth)")

# === SOFASCORE POSITION FETCHING (RAW, NO FALLBACK) ===
def get_sofascore_match_id(url):
    match = re.search(r'#id:(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/(\d+)$', url)
    return match.group(1) if match else None

def fetch_sofascore_raw_positions(match_id):
    """Fetch RAW SofaScore positions without any fallback."""
    positions = {}
    pos_map = {'F': 'FWD', 'M': 'MID', 'D': 'DEF', 'G': 'GK'}
    
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/lineups"
    try:
        response = requests.get(url, impersonate="chrome120")
        data = response.json()
        
        for team in ['home', 'away']:
            for player in data.get(team, {}).get('players', []):
                name = player['player']['name']
                raw_pos = player.get('position', 'M')
                mapped_pos = pos_map.get(raw_pos, 'MID')
                positions[name.lower()] = mapped_pos
    except Exception as e:
        print(f"    Error fetching SofaScore: {e}")
    
    return positions

# === WHOSCORED POSITION FETCHING ===
def fetch_whoscored_raw_positions(url):
    """Fetch RAW WhoScored positions."""
    from whoscored_adapter import get_whoscored_positions
    return get_whoscored_positions(url)

# All 18 matches
MATCHES = [
    {"name": "Napoli vs Eintracht Frankfurt", 
     "sofascore": "https://www.sofascore.com/football/match/napoli-eintracht-frankfurt/zdbsoeb#id:14566900",
     "whoscored": "https://www.whoscored.com/matches/1946419/live/europe-champions-league-2025-2026-napoli-eintracht-frankfurt"},
    {"name": "Slavia Praha vs Arsenal", 
     "sofascore": "https://www.sofascore.com/football/match/sk-slavia-praha-arsenal/RsqU#id:14566883",
     "whoscored": "https://www.whoscored.com/matches/1946416/live/europe-champions-league-2025-2026-slavia-prague-arsenal"},
    {"name": "Atletico Madrid vs Union SG", 
     "sofascore": "https://www.sofascore.com/football/match/royale-union-saint-gilloise-atletico-madrid/LgbskXb#id:14566777",
     "whoscored": "https://www.whoscored.com/matches/1946437/live/europe-champions-league-2025-2026-atletico-madrid-union-st-gilloise"},
    {"name": "Bodo/Glimt vs Monaco", 
     "sofascore": "https://www.sofascore.com/football/match/as-monaco-bodoglimt/gnsdI#id:14566844",
     "whoscored": "https://www.whoscored.com/matches/1946468/live/europe-champions-league-2025-2026-bodoe-glimt-monaco"},
    {"name": "Juventus vs Sporting CP", 
     "sofascore": "https://www.sofascore.com/football/match/sporting-juventus/Mdbsbkb#id:14566766",
     "whoscored": "https://www.whoscored.com/matches/1946425/live/europe-champions-league-2025-2026-juventus-sporting-cp"},
    {"name": "Liverpool vs Real Madrid", 
     "sofascore": "https://www.sofascore.com/football/match/real-madrid-liverpool/UsEgb#id:14566636",
     "whoscored": "https://www.whoscored.com/matches/1946375/live/europe-champions-league-2025-2026-liverpool-real-madrid"},
    {"name": "Olympiacos vs PSV", 
     "sofascore": "https://www.sofascore.com/football/match/olympiacos-fc-psv-eindhoven/cjbsVob#id:14566867",
     "whoscored": "https://www.whoscored.com/matches/1946474/live/europe-champions-league-2025-2026-olympiacos-psv-eindhoven"},
    {"name": "PSG vs Bayern Munich", 
     "sofascore": "https://www.sofascore.com/football/match/fc-bayern-munchen-paris-saint-germain/UHsxdb#id:14566656",
     "whoscored": "https://www.whoscored.com/matches/1946347/live/europe-champions-league-2025-2026-paris-saint-germain-bayern-munich"},
    {"name": "Copenhagen vs Tottenham", 
     "sofascore": "https://www.sofascore.com/football/match/fc-kobenhavn-tottenham-hotspur/IsJA#id:14566829",
     "whoscored": "https://www.whoscored.com/matches/1946463/live/europe-champions-league-2025-2026-tottenham-fc-copenhagen"},
    {"name": "Pafos vs Villarreal", 
     "sofascore": "https://www.sofascore.com/football/match/pafos-fc-villarreal/ugbsBHtb#id:14566966",
     "whoscored": "https://www.whoscored.com/matches/1946445/live/europe-champions-league-2025-2026-pafos-fc-villarreal"},
    {"name": "Qarabag vs Chelsea", 
     "sofascore": "https://www.sofascore.com/football/match/qarabag-chelsea/Nsmuc#id:14566919",
     "whoscored": "https://www.whoscored.com/matches/1946369/live/europe-champions-league-2025-2026-qarabag-fk-chelsea"},
    {"name": "Ajax vs Galatasaray", 
     "sofascore": "https://www.sofascore.com/football/match/galatasaray-afc-ajax/djbsllb#id:14566876",
     "whoscored": "https://www.whoscored.com/matches/1946478/live/europe-champions-league-2025-2026-ajax-galatasaray"},
    {"name": "Benfica vs Leverkusen", 
     "sofascore": "https://www.sofascore.com/football/match/benfica-bayer-04-leverkusen/Gdbsgkb#id:14566736",
     "whoscored": "https://www.whoscored.com/matches/1946413/live/europe-champions-league-2025-2026-benfica-bayer-leverkusen"},
    {"name": "Club Brugge vs Barcelona", 
     "sofascore": "https://www.sofascore.com/football/match/club-brugge-kv-barcelona/rgbsNhb#id:14566745",
     "whoscored": "https://www.whoscored.com/matches/1946393/live/europe-champions-league-2025-2026-club-brugge-barcelona"},
    {"name": "Kairat vs Inter", 
     "sofascore": "https://www.sofascore.com/football/match/kairat-almaty-inter/Xdbsxdc#id:14566614",
     "whoscored": "https://www.whoscored.com/matches/1946400/live/europe-champions-league-2025-2026-inter-kairat-almaty"},
    {"name": "Man City vs Dortmund", 
     "sofascore": "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662",
     "whoscored": "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"},
    {"name": "Newcastle vs Athletic", 
     "sofascore": "https://www.sofascore.com/football/match/athletic-club-newcastle-united/OsAgb#id:14566958",
     "whoscored": "https://www.whoscored.com/matches/1946487/live/europe-champions-league-2025-2026-newcastle-athletic-club"},
    {"name": "Atalanta vs Marseille", 
     "sofascore": "https://www.sofascore.com/football/match/atalanta-olympique-de-marseille/QHsLdb#id:14566822",
     "whoscored": "https://www.whoscored.com/matches/1946434/live/europe-champions-league-2025-2026-marseille-atalanta"},
]

# Collect all positions
all_sofascore_positions = {}
all_whoscored_positions = {}

print("\n" + "=" * 70)
print("FETCHING RAW POSITIONS FROM BOTH SOURCES")
print("=" * 70)

for i, match in enumerate(MATCHES, 1):
    print(f"\n[{i}/18] {match['name']}")
    
    # SofaScore
    match_id = get_sofascore_match_id(match['sofascore'])
    sf_pos = fetch_sofascore_raw_positions(match_id)
    all_sofascore_positions.update(sf_pos)
    print(f"  SofaScore: {len(sf_pos)} players")
    
    # WhoScored
    ws_pos = fetch_whoscored_raw_positions(match['whoscored'])
    all_whoscored_positions.update(ws_pos)
    print(f"  WhoScored: {len(ws_pos)} players")
    
    time.sleep(0.5)

print(f"\n\nTotal SofaScore positions: {len(all_sofascore_positions)}")
print(f"Total WhoScored positions: {len(all_whoscored_positions)}")

# ========================================================
# FAIR COMPARISON: Only players that BOTH sources have
# ========================================================
print("\n" + "=" * 70)
print("FAIR COMPARISON: Only players found by BOTH sources")
print("=" * 70)

# Find common players (in Excel, SofaScore, AND WhoScored)
common_players = []
for _, row in excel_df.iterrows():
    name = row['name_lower']
    excel_pos = row['pos']
    
    sf_pos = all_sofascore_positions.get(name)
    ws_pos = all_whoscored_positions.get(name)
    
    # Only include if BOTH sources have this player
    if sf_pos and ws_pos:
        common_players.append({
            'name': row['name'],
            'name_lower': name,
            'excel_pos': excel_pos,
            'sofascore_pos': sf_pos,
            'whoscored_pos': ws_pos,
            'sofascore_correct': sf_pos == excel_pos,
            'whoscored_correct': ws_pos == excel_pos,
        })

common_df = pd.DataFrame(common_players)
print(f"\nPlayers found by BOTH sources: {len(common_df)}")

# Calculate accuracy on the SAME set of players
sf_correct = common_df['sofascore_correct'].sum()
ws_correct = common_df['whoscored_correct'].sum()
total = len(common_df)

sf_accuracy = 100 * sf_correct / total
ws_accuracy = 100 * ws_correct / total

print("\n" + "=" * 70)
print("FAIR POSITION ACCURACY COMPARISON")
print("=" * 70)
print(f"\n{'Metric':<30} {'SofaScore':>15} {'WhoScored':>15}")
print("-" * 60)
print(f"{'Total Players Compared':<30} {total:>15} {total:>15}")
print(f"{'Correct Positions':<30} {sf_correct:>15} {ws_correct:>15}")
print(f"{'Wrong Positions':<30} {total - sf_correct:>15} {total - ws_correct:>15}")
print(f"{'ACCURACY':<30} {sf_accuracy:>14.1f}% {ws_accuracy:>14.1f}%")

print("\n" + "=" * 70)
if sf_accuracy > ws_accuracy:
    print(f"WINNER: SofaScore ({sf_accuracy:.1f}% vs {ws_accuracy:.1f}%)")
    diff = sf_accuracy - ws_accuracy
elif ws_accuracy > sf_accuracy:
    print(f"WINNER: WhoScored ({ws_accuracy:.1f}% vs {sf_accuracy:.1f}%)")
    diff = ws_accuracy - sf_accuracy
else:
    print("TIE")
    diff = 0
print(f"Difference: {diff:.1f} percentage points")
print("=" * 70)

# Show errors for each
sf_errors = common_df[~common_df['sofascore_correct']]
ws_errors = common_df[~common_df['whoscored_correct']]

print(f"\n\nSofaScore Position Errors ({len(sf_errors)} total):")
print("-" * 60)
for _, row in sf_errors.iterrows():
    print(f"  {row['name']:<30} SofaScore={row['sofascore_pos']:<4} Excel={row['excel_pos']}")

print(f"\n\nWhoScored Position Errors ({len(ws_errors)} total):")
print("-" * 60)
for _, row in ws_errors.iterrows():
    print(f"  {row['name']:<30} WhoScored={row['whoscored_pos']:<4} Excel={row['excel_pos']}")

# Save detailed results
common_df.to_csv("fair_position_comparison.csv", index=False)
print(f"\n\nDetailed results saved to: fair_position_comparison.csv")

# Also show what's NOT in WhoScored but IS in SofaScore
print("\n" + "=" * 70)
print("COVERAGE ANALYSIS")
print("=" * 70)
sf_only = []
for _, row in excel_df.iterrows():
    name = row['name_lower']
    if name in all_sofascore_positions and name not in all_whoscored_positions:
        sf_only.append(row['name'])

print(f"\nPlayers in SofaScore but NOT in WhoScored: {len(sf_only)}")
print("(These are likely substitutes who didn't start)")
if len(sf_only) <= 20:
    for p in sf_only:
        print(f"  - {p}")
else:
    for p in sf_only[:10]:
        print(f"  - {p}")
    print(f"  ... and {len(sf_only) - 10} more")
