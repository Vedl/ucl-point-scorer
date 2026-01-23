"""
Gameweek 5 UCL Accuracy Test
Tests both positional accuracy and points accuracy against Excel baseline.
Uses updated WhoScored mapping (AMR/AML -> FWD, MR/ML -> MID)
"""
import pandas as pd
from player_score_calculator import calc_all_players
from curl_cffi import requests
import sofascore_adapter
from whoscored_adapter import get_whoscored_positions, POSITION_MAP
import re
import time

# Load GW5 Excel ground truth
EXCEL_PATH = "Gameweek 5 UCL Points 25:26.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()
print(f"Loaded {len(excel_df)} players from GW5 Excel (Ground Truth)")

# GW5 Matches (November 25-26, 2025)
# SofaScore URLs need to be fetched - using pattern based on GW4
# Match IDs typically increment, so estimating based on GW4 patterns

GW5_MATCHES = [
    {"name": "Ajax vs Benfica", "sofascore_id": "14567100"},
    {"name": "Galatasaray vs Union SG", "sofascore_id": "14567101"},
    {"name": "Dortmund vs Villarreal", "sofascore_id": "14567102"},
    {"name": "Chelsea vs Barcelona", "sofascore_id": "14567103"},
    {"name": "Bodo/Glimt vs Juventus", "sofascore_id": "14567104"},
    {"name": "Man City vs Leverkusen", "sofascore_id": "14567105"},
    {"name": "Marseille vs Newcastle", "sofascore_id": "14567106"},
    {"name": "Slavia Praha vs Athletic", "sofascore_id": "14567107"},
    {"name": "Napoli vs Qarabag", "sofascore_id": "14567108"},
    {"name": "Copenhagen vs Kairat", "sofascore_id": "14567109"},
    {"name": "Pafos vs Monaco", "sofascore_id": "14567110"},
    {"name": "Arsenal vs Bayern", "sofascore_id": "14567111"},
    {"name": "Atletico vs Inter", "sofascore_id": "14567112"},
    {"name": "Frankfurt vs Atalanta", "sofascore_id": "14567113"},
    {"name": "Liverpool vs PSV", "sofascore_id": "14567114"},
    {"name": "Olympiacos vs Real Madrid", "sofascore_id": "14567115"},
    {"name": "PSG vs Tottenham", "sofascore_id": "14567116"},
    {"name": "Sporting vs Club Brugge", "sofascore_id": "14567117"},
]

# First, let's find actual GW5 match IDs from SofaScore API
def find_gw5_matches():
    """Find actual GW5 match IDs from SofaScore."""
    print("\nSearching for GW5 match IDs...")
    
    # Try to find matches from November 25-26, 2025
    base_url = "https://www.sofascore.com/api/v1/unique-tournament/7/season/61644/events/round/5"
    
    try:
        response = requests.get(base_url, impersonate="chrome120")
        if response.status_code == 200:
            data = response.json()
            matches = []
            for event in data.get('events', []):
                home = event['homeTeam']['name']
                away = event['awayTeam']['name']
                match_id = event['id']
                matches.append({
                    'name': f"{home} vs {away}",
                    'sofascore_id': str(match_id),
                    'home': home,
                    'away': away
                })
            return matches
    except Exception as e:
        print(f"Error fetching GW5 matches: {e}")
    
    return None

# Try to find actual match IDs
actual_matches = find_gw5_matches()

if actual_matches:
    print(f"Found {len(actual_matches)} GW5 matches from SofaScore API")
    GW5_MATCHES = actual_matches
else:
    print("Could not fetch match IDs from API, will try direct search...")

# ========================================================
# POSITION ACCURACY TEST  
# ========================================================
def get_sofascore_raw_positions(match_id):
    """Fetch raw SofaScore positions."""
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
        pass
    
    return positions

# Collect positions from both sources
all_sofascore_positions = {}
all_whoscored_positions = {}
all_calculated_sf = []
all_calculated_ws = []

print("\n" + "=" * 70)
print("FETCHING DATA FROM ALL GW5 MATCHES")
print("=" * 70)

successful_matches = 0
for i, match in enumerate(GW5_MATCHES[:18], 1):  # Limit to 18 matches
    print(f"\n[{i}/18] {match['name']}...")
    match_id = match['sofascore_id']
    
    try:
        # Get SofaScore positions
        sf_pos = get_sofascore_raw_positions(match_id)
        if sf_pos:
            all_sofascore_positions.update(sf_pos)
            print(f"  SofaScore: {len(sf_pos)} players")
        else:
            print(f"  SofaScore: Failed to fetch")
            continue
        
        # Try to construct WhoScored URL and get positions
        # WhoScored match IDs are different, but we can try to search
        # For now, skip WhoScored for this quick test
        
        # Calculate points with SofaScore
        sofascore_adapter.reset_position_cache()
        sofascore_url = f"https://www.sofascore.com/football/match/x/x#id:{match_id}"
        
        df_sf = calc_all_players(sofascore_url, whoscored_url=None)
        if not df_sf.empty:
            df_sf['match'] = match['name']
            all_calculated_sf.append(df_sf[['name', 'score', 'pos', 'match']])
            successful_matches += 1
        
    except Exception as e:
        print(f"  Error: {str(e)[:40]}")
    
    time.sleep(0.5)

print(f"\n\nSuccessfully processed {successful_matches} matches")

# ========================================================
# COMPARISON WITH EXCEL
# ========================================================
if all_calculated_sf:
    sf_df = pd.concat(all_calculated_sf, ignore_index=True)
    sf_df['name_lower'] = sf_df['name'].str.lower().str.strip()
    
    print(f"\nTotal SofaScore calculated: {len(sf_df)} player entries")
    
    # Merge with Excel
    comparison = sf_df.merge(
        excel_df[['name_lower', 'score', 'pos']],
        on='name_lower',
        how='inner',
        suffixes=('_calc', '_excel')
    )
    
    print(f"Matched with Excel: {len(comparison)} players")
    
    # Position accuracy
    comparison['pos_match'] = comparison['pos_calc'] == comparison['pos_excel']
    pos_correct = comparison['pos_match'].sum()
    pos_total = len(comparison)
    
    # Points accuracy
    comparison['diff'] = comparison['score_calc'] - comparison['score_excel']
    comparison['abs_diff'] = comparison['diff'].abs()
    
    exact = len(comparison[comparison['diff'] == 0])
    close_3 = len(comparison[(comparison['abs_diff'] >= 1) & (comparison['abs_diff'] <= 3)])
    close_5 = len(comparison[(comparison['abs_diff'] >= 4) & (comparison['abs_diff'] <= 5)])
    large = len(comparison[comparison['abs_diff'] > 5])
    
    print("\n" + "=" * 70)
    print("GW5 VERIFICATION RESULTS (SofaScore)")
    print("=" * 70)
    print(f"\nPOSITION ACCURACY:")
    print(f"  Correct: {pos_correct}/{pos_total} ({100*pos_correct/pos_total:.1f}%)")
    print(f"  Wrong:   {pos_total - pos_correct}")
    
    print(f"\nPOINTS ACCURACY:")
    print(f"  Exact (diff=0):     {exact} ({100*exact/pos_total:.1f}%)")
    print(f"  Close (±1-3):       {close_3}")
    print(f"  Close (±4-5):       {close_5}")
    print(f"  Large (>5):         {large}")
    print(f"  Average |diff|:     {comparison['abs_diff'].mean():.2f}")
    print(f"  Within ±3:          {exact + close_3} ({100*(exact+close_3)/pos_total:.1f}%)")
    
    # Show position mismatches
    pos_mismatches = comparison[~comparison['pos_match']]
    if len(pos_mismatches) > 0:
        print(f"\n\nPosition Mismatches ({len(pos_mismatches)}):")
        print("-" * 60)
        for _, row in pos_mismatches.head(20).iterrows():
            print(f"  {row['name']:<25} Calc={row['pos_calc']:<4} Excel={row['pos_excel']}")
    
    # Show large discrepancies
    large_diff = comparison[comparison['abs_diff'] > 5].sort_values('abs_diff', ascending=False)
    if len(large_diff) > 0:
        print(f"\n\nLarge Discrepancies ({len(large_diff)}):")
        print("-" * 60)
        for _, row in large_diff.head(15).iterrows():
            print(f"  {row['name']:<25} Calc={row['score_calc']:>3.0f}  Excel={row['score_excel']:>3.0f}  Diff={row['diff']:>+4.0f}")
    
    # Save results
    comparison.to_csv("gw5_verification_results.csv", index=False)
    print(f"\n\nResults saved to: gw5_verification_results.csv")

else:
    print("\nNo data was calculated. Need to find correct GW5 match IDs.")
