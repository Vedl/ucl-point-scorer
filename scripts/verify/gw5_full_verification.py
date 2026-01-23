"""
GW5 Full Verification - All 18 Matches
Tests both positional accuracy and points accuracy against Excel baseline.
Uses CORRECT GW5 SofaScore URLs.
"""
import pandas as pd
from player_score_calculator import calc_all_players
import sofascore_adapter
import time

# Load GW5 Excel ground truth
EXCEL_PATH = "Gameweek 5 UCL Points 25:26.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()
print(f"Loaded {len(excel_df)} players from GW5 Excel (Ground Truth)")

# All 18 GW5 matches - CORRECT URLs
GW5_MATCHES = [
    # User provided (7)
    {"name": "Benfica vs Ajax", "sofascore": "https://www.sofascore.com/football/match/benfica-afc-ajax/djbsgkb#id:14566874"},
    {"name": "Union SG vs Galatasaray", "sofascore": "https://www.sofascore.com/football/match/royale-union-saint-gilloise-galatasaray/llbskXb#id:14566937"},
    {"name": "Juventus vs Bodo/Glimt", "sofascore": "https://www.sofascore.com/football/match/juventus-bodoglimt/gnsMdb#id:14566842"},
    {"name": "Villarreal vs Dortmund", "sofascore": "https://www.sofascore.com/football/match/villarreal-borussia-dortmund/ydbsugb#id:14566620"},
    {"name": "Barcelona vs Chelsea", "sofascore": "https://www.sofascore.com/football/match/barcelona-chelsea/Nrgb#id:14566580"},
    {"name": "Leverkusen vs Man City", "sofascore": "https://www.sofascore.com/football/match/bayer-04-leverkusen-manchester-city/rsGdb#id:14566663"},
    {"name": "Qarabag vs Napoli", "sofascore": "https://www.sofascore.com/football/match/qarabag-napoli/oebsmuc#id:14566902"},
    # Browser found (11)
    {"name": "Marseille vs Newcastle", "sofascore": "https://www.sofascore.com/football/match/olympique-de-marseille-newcastle-united/OsQH#id:14566835"},
    {"name": "Slavia Praha vs Athletic", "sofascore": "https://www.sofascore.com/football/match/athletic-club-sk-slavia-praha/qUsAgb#id:14566885"},
    {"name": "Copenhagen vs Kairat", "sofascore": "https://www.sofascore.com/football/match/kairat-almaty-fc-kobenhavn/JAsxdc#id:14566974"},
    {"name": "Pafos vs Monaco", "sofascore": "https://www.sofascore.com/football/match/pafos-fc-as-monaco/dIsBHtb#id:14566968"},
    {"name": "Arsenal vs Bayern", "sofascore": "https://www.sofascore.com/football/match/fc-bayern-munchen-arsenal/Rsxdb#id:14566717"},
    {"name": "Atletico vs Inter", "sofascore": "https://www.sofascore.com/football/match/atletico-madrid-inter/XdbsLgb#id:14566774"},
    {"name": "Frankfurt vs Atalanta", "sofascore": "https://www.sofascore.com/football/match/atalanta-eintracht-frankfurt/zdbsLdb#id:14566755"},
    {"name": "Liverpool vs PSV", "sofascore": "https://www.sofascore.com/football/match/psv-eindhoven-liverpool/Uscjb#id:14566638"},
    {"name": "Olympiacos vs Real Madrid", "sofascore": "https://www.sofascore.com/football/match/olympiacos-fc-real-madrid/EgbsVob#id:14566865"},
    {"name": "PSG vs Tottenham", "sofascore": "https://www.sofascore.com/football/match/paris-saint-germain-tottenham-hotspur/IsUH#id:14566658"},
    {"name": "Sporting vs Club Brugge", "sofascore": "https://www.sofascore.com/football/match/sporting-club-brugge-kv/Nhbsbkb#id:14566855"},
]

all_calculated = []

print("\n" + "=" * 70)
print("FETCHING DATA FROM ALL 18 GW5 MATCHES")
print("=" * 70)

for i, match in enumerate(GW5_MATCHES, 1):
    print(f"\n[{i}/18] {match['name']}...")
    
    try:
        sofascore_adapter.reset_position_cache()
        df = calc_all_players(match['sofascore'], whoscored_url=None)
        
        if not df.empty:
            df['match'] = match['name']
            all_calculated.append(df[['name', 'score', 'pos', 'match']])
            print(f"  ✓ {len(df)} players")
        else:
            print(f"  ❌ No data")
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:40]}")
    
    time.sleep(0.5)

# Combine and analyze
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
    avg_diff = comparison['abs_diff'].mean()
    
    print("\n" + "=" * 70)
    print("GW5 VERIFICATION RESULTS")
    print("=" * 70)
    
    print(f"\n📊 POSITION ACCURACY:")
    print(f"   Correct: {pos_correct}/{pos_total} ({100*pos_correct/pos_total:.1f}%)")
    print(f"   Wrong:   {pos_total - pos_correct}")
    
    print(f"\n📈 POINTS ACCURACY:")
    print(f"   Exact (diff=0):     {exact} ({100*exact/pos_total:.1f}%)")
    print(f"   Close (±1-3):       {close_3} ({100*close_3/pos_total:.1f}%)")
    print(f"   Close (±4-5):       {close_5} ({100*close_5/pos_total:.1f}%)")
    print(f"   Large (>5):         {large} ({100*large/pos_total:.1f}%)")
    print(f"   Average |diff|:     {avg_diff:.2f}")
    print(f"   Within ±3:          {exact + close_3} ({100*(exact+close_3)/pos_total:.1f}%)")
    
    # Position mismatches
    pos_mismatches = comparison[~comparison['pos_match']]
    if len(pos_mismatches) > 0:
        print(f"\n\n❌ POSITION MISMATCHES ({len(pos_mismatches)}):")
        print("-" * 60)
        for _, row in pos_mismatches.iterrows():
            print(f"   {row['name']:<25} Calc={row['pos_calc']:<4} Excel={row['pos_excel']}")
    
    # Large discrepancies
    large_diff = comparison[comparison['abs_diff'] > 5].sort_values('abs_diff', ascending=False)
    if len(large_diff) > 0:
        print(f"\n\n⚠️ LARGE POINT DISCREPANCIES ({len(large_diff)}) - Top 20:")
        print("-" * 60)
        for _, row in large_diff.head(20).iterrows():
            print(f"   {row['name']:<25} Calc={row['score_calc']:>3.0f}  Excel={row['score_excel']:>3.0f}  Diff={row['diff']:>+4.0f}")
    
    # Save
    comparison.to_csv("gw5_full_verification.csv", index=False)
    print(f"\n\n✅ Results saved to: gw5_full_verification.csv")

else:
    print("\n❌ No data calculated!")
