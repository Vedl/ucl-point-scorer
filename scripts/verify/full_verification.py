"""
Full 18-Match Verification Script
Compares calculated scores against Excel for ALL players in UCL Gameweek 4.
"""
import pandas as pd
from player_score_calculator import calc_all_players
import sofascore_adapter
import time

# Load Excel ground truth
EXCEL_PATH = "Gameweek 4 UCL 25:26 Points.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()
print(f"Loaded {len(excel_df)} players from Excel")

# All 18 UCL Gameweek 4 matches (SofaScore URLs)
MATCHES = [
    {"name": "Napoli vs Eintracht Frankfurt", "sofascore": "https://www.sofascore.com/football/match/napoli-eintracht-frankfurt/zdbsoeb#id:14566900"},
    {"name": "Slavia Praha vs Arsenal", "sofascore": "https://www.sofascore.com/football/match/sk-slavia-praha-arsenal/RsqU#id:14566883"},
    {"name": "Atletico Madrid vs Union SG", "sofascore": "https://www.sofascore.com/football/match/royale-union-saint-gilloise-atletico-madrid/LgbskXb#id:14566777"},
    {"name": "Bodo/Glimt vs Monaco", "sofascore": "https://www.sofascore.com/football/match/as-monaco-bodoglimt/gnsdI#id:14566844"},
    {"name": "Juventus vs Sporting CP", "sofascore": "https://www.sofascore.com/football/match/sporting-juventus/Mdbsbkb#id:14566766"},
    {"name": "Liverpool vs Real Madrid", "sofascore": "https://www.sofascore.com/football/match/real-madrid-liverpool/UsEgb#id:14566636"},
    {"name": "Olympiacos vs PSV", "sofascore": "https://www.sofascore.com/football/match/olympiacos-fc-psv-eindhoven/cjbsVob#id:14566867"},
    {"name": "PSG vs Bayern Munich", "sofascore": "https://www.sofascore.com/football/match/fc-bayern-munchen-paris-saint-germain/UHsxdb#id:14566656"},
    {"name": "Copenhagen vs Tottenham", "sofascore": "https://www.sofascore.com/football/match/fc-kobenhavn-tottenham-hotspur/IsJA#id:14566829"},
    {"name": "Pafos vs Villarreal", "sofascore": "https://www.sofascore.com/football/match/pafos-fc-villarreal/ugbsBHtb#id:14566966"},
    {"name": "Qarabag vs Chelsea", "sofascore": "https://www.sofascore.com/football/match/qarabag-chelsea/Nsmuc#id:14566919"},
    {"name": "Ajax vs Galatasaray", "sofascore": "https://www.sofascore.com/football/match/galatasaray-afc-ajax/djbsllb#id:14566876"},
    {"name": "Benfica vs Leverkusen", "sofascore": "https://www.sofascore.com/football/match/benfica-bayer-04-leverkusen/Gdbsgkb#id:14566736"},
    {"name": "Club Brugge vs Barcelona", "sofascore": "https://www.sofascore.com/football/match/club-brugge-kv-barcelona/rgbsNhb#id:14566745"},
    {"name": "Kairat vs Inter", "sofascore": "https://www.sofascore.com/football/match/kairat-almaty-inter/Xdbsxdc#id:14566614"},
    {"name": "Man City vs Dortmund", "sofascore": "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662"},
    {"name": "Newcastle vs Athletic", "sofascore": "https://www.sofascore.com/football/match/athletic-club-newcastle-united/OsAgb#id:14566958"},
    {"name": "Atalanta vs Marseille", "sofascore": "https://www.sofascore.com/football/match/atalanta-olympique-de-marseille/QHsLdb#id:14566822"},
]

all_calculated = []
match_results = []

print("\n" + "=" * 80)
print("RUNNING FULL VERIFICATION (18 MATCHES)")
print("=" * 80)

for i, match in enumerate(MATCHES, 1):
    print(f"\n[{i}/18] {match['name']}...")
    
    try:
        # Reset position cache between matches
        sofascore_adapter.reset_position_cache()
        
        # Calculate scores (without WhoScored for now - will add if needed)
        df = calc_all_players(match['sofascore'])
        
        if df.empty:
            print(f"  ❌ ERROR: No data returned")
            match_results.append({"match": match['name'], "status": "ERROR", "players": 0})
            continue
        
        df['match'] = match['name']
        all_calculated.append(df)
        
        print(f"  ✓ Loaded {len(df)} players")
        match_results.append({"match": match['name'], "status": "OK", "players": len(df)})
        
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)[:50]}")
        match_results.append({"match": match['name'], "status": "ERROR", "players": 0, "error": str(e)})
    
    # Small delay to avoid rate limiting
    time.sleep(1)

# Combine all calculated results
if all_calculated:
    combined_df = pd.concat(all_calculated, ignore_index=True)
    combined_df['name_lower'] = combined_df['name'].str.lower().str.strip()
    
    print(f"\n\nTotal calculated: {len(combined_df)} player entries")
    
    # Merge with Excel
    comparison = combined_df.merge(
        excel_df[['name_lower', 'score', 'pos']],
        on='name_lower',
        how='inner',
        suffixes=('_calc', '_excel')
    )
    
    print(f"Matched with Excel: {len(comparison)} players")
    
    # Calculate differences
    comparison['diff'] = comparison['score_calc'] - comparison['score_excel']
    comparison['pos_match'] = comparison['pos_calc'] == comparison['pos_excel']
    comparison['abs_diff'] = comparison['diff'].abs()
    
    # Statistics
    exact_matches = len(comparison[comparison['diff'] == 0])
    close_1 = len(comparison[(comparison['abs_diff'] >= 1) & (comparison['abs_diff'] <= 3)])
    close_5 = len(comparison[(comparison['abs_diff'] >= 4) & (comparison['abs_diff'] <= 5)])
    large_diffs = len(comparison[comparison['abs_diff'] > 5])
    pos_mismatches = len(comparison[~comparison['pos_match']])
    
    print("\n" + "=" * 80)
    print("OVERALL VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total players verified:       {len(comparison)}")
    print(f"Exact matches (diff=0):       {exact_matches} ({100*exact_matches/len(comparison):.1f}%)")
    print(f"Close (|diff| 1-3):           {close_1} ({100*close_1/len(comparison):.1f}%)")
    print(f"Close (|diff| 4-5):           {close_5} ({100*close_5/len(comparison):.1f}%)")
    print(f"Large differences (|diff|>5): {large_diffs} ({100*large_diffs/len(comparison):.1f}%)")
    print(f"Position mismatches:          {pos_mismatches}")
    
    # Show position mismatches
    if pos_mismatches > 0:
        print("\n" + "=" * 80)
        print("POSITION MISMATCHES")
        print("=" * 80)
        pos_mismatch_df = comparison[~comparison['pos_match']]
        for _, row in pos_mismatch_df.iterrows():
            print(f"  {row['name']}: Calc={row['pos_calc']}, Excel={row['pos_excel']} (Match: {row['match']})")
    
    # Show large discrepancies
    if large_diffs > 0:
        print("\n" + "=" * 80)
        print(f"LARGE DISCREPANCIES (|diff| > 5) - Top 20")
        print("=" * 80)
        large_df = comparison[comparison['abs_diff'] > 5].sort_values('abs_diff', ascending=False).head(20)
        print(f"{'Player':<25} {'Calc':>6} {'Excel':>6} {'Diff':>6} {'Match':<30}")
        print("-" * 80)
        for _, row in large_df.iterrows():
            print(f"{row['name'][:24]:<25} {row['score_calc']:>6.0f} {row['score_excel']:>6.0f} {row['diff']:>+6.0f} {row['match'][:29]:<30}")
    
    # Save full results
    comparison.to_csv("full_verification_results.csv", index=False)
    print(f"\n\nFull results saved to: full_verification_results.csv")
    
    # Summary by match
    print("\n" + "=" * 80)
    print("SUMMARY BY MATCH")
    print("=" * 80)
    for match_name in comparison['match'].unique():
        match_data = comparison[comparison['match'] == match_name]
        exact = len(match_data[match_data['diff'] == 0])
        avg_diff = match_data['abs_diff'].mean()
        print(f"{match_name[:35]:<36} Players: {len(match_data):>3}, Exact: {exact:>3}, Avg |diff|: {avg_diff:.1f}")

else:
    print("\n❌ No data was calculated successfully!")
