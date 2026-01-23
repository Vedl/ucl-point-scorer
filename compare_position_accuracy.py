"""
Position Accuracy Comparison: SofaScore vs WhoScored
Excel is the GROUND TRUTH (100% correct for GW4)
Tests raw positions from each source WITHOUT any fallback.
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
                # Use the MATCH position (position in lineup), not general player position
                raw_pos = player.get('position', 'M')  # Position in this specific match
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

# Compare against Excel ground truth
print("\n" + "=" * 70)
print("COMPARING AGAINST EXCEL GROUND TRUTH")
print("=" * 70)

sofascore_correct = 0
sofascore_wrong = 0
sofascore_missing = 0
sofascore_mismatches = []

whoscored_correct = 0
whoscored_wrong = 0
whoscored_missing = 0
whoscored_mismatches = []

for _, row in excel_df.iterrows():
    name = row['name_lower']
    excel_pos = row['pos']
    
    # SofaScore comparison
    sf_pos = all_sofascore_positions.get(name)
    if sf_pos:
        if sf_pos == excel_pos:
            sofascore_correct += 1
        else:
            sofascore_wrong += 1
            sofascore_mismatches.append({'name': row['name'], 'sofascore': sf_pos, 'excel': excel_pos})
    else:
        sofascore_missing += 1
    
    # WhoScored comparison
    ws_pos = all_whoscored_positions.get(name)
    if ws_pos:
        if ws_pos == excel_pos:
            whoscored_correct += 1
        else:
            whoscored_wrong += 1
            whoscored_mismatches.append({'name': row['name'], 'whoscored': ws_pos, 'excel': excel_pos})
    else:
        whoscored_missing += 1

# Results
print("\n" + "=" * 70)
print("POSITION ACCURACY RESULTS")
print("=" * 70)

sf_total = sofascore_correct + sofascore_wrong
ws_total = whoscored_correct + whoscored_wrong

print(f"\n{'Metric':<30} {'SofaScore':>15} {'WhoScored':>15}")
print("-" * 60)
print(f"{'Correct Positions':<30} {sofascore_correct:>15} {whoscored_correct:>15}")
print(f"{'Wrong Positions':<30} {sofascore_wrong:>15} {whoscored_wrong:>15}")
print(f"{'Players Not Found':<30} {sofascore_missing:>15} {whoscored_missing:>15}")
print(f"{'Total Compared':<30} {sf_total:>15} {ws_total:>15}")
print(f"{'ACCURACY':<30} {100*sofascore_correct/sf_total if sf_total else 0:>14.1f}% {100*whoscored_correct/ws_total if ws_total else 0:>14.1f}%")

print("\n" + "=" * 70)
if sf_total and ws_total:
    sf_acc = 100*sofascore_correct/sf_total
    ws_acc = 100*whoscored_correct/ws_total
    if sf_acc > ws_acc:
        print(f"WINNER: SofaScore ({sf_acc:.1f}% vs {ws_acc:.1f}%)")
    elif ws_acc > sf_acc:
        print(f"WINNER: WhoScored ({ws_acc:.1f}% vs {sf_acc:.1f}%)")
    else:
        print("TIE")
print("=" * 70)

# Show mismatches
if sofascore_mismatches:
    print(f"\nSofaScore Position Errors ({len(sofascore_mismatches)}):")
    for m in sofascore_mismatches[:15]:
        print(f"  {m['name']}: SofaScore={m['sofascore']}, Excel={m['excel']}")
    if len(sofascore_mismatches) > 15:
        print(f"  ... and {len(sofascore_mismatches) - 15} more")

if whoscored_mismatches:
    print(f"\nWhoScored Position Errors ({len(whoscored_mismatches)}):")
    for m in whoscored_mismatches[:15]:
        print(f"  {m['name']}: WhoScored={m['whoscored']}, Excel={m['excel']}")
    if len(whoscored_mismatches) > 15:
        print(f"  ... and {len(whoscored_mismatches) - 15} more")
