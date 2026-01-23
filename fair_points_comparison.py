"""
Fair POINTS Accuracy Comparison: SofaScore vs WhoScored
Only compares starting XI players (found by both sources).
Excel is the GROUND TRUTH for correct points.
"""
import pandas as pd
from player_score_calculator import calc_all_players
import sofascore_adapter
import time

# Load Excel ground truth
EXCEL_PATH = "Gameweek 4 UCL 25:26 Points.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()
print(f"Loaded {len(excel_df)} players from Excel (Ground Truth)")

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

# Run calculations with both configurations
print("\n" + "=" * 80)
print("CALCULATING POINTS: SOFASCORE POSITIONS (No WhoScored)")
print("=" * 80)

sofascore_results = []
for i, match in enumerate(MATCHES, 1):
    print(f"\n[{i}/18] {match['name']}...")
    try:
        sofascore_adapter.reset_position_cache()
        # Calculate with SofaScore positions only (no WhoScored)
        df = calc_all_players(match['sofascore'], whoscored_url=None)
        if not df.empty:
            df['match'] = match['name']
            sofascore_results.append(df[['name', 'score', 'pos', 'match']])
            print(f"  ✓ {len(df)} players")
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:40]}")
    time.sleep(0.5)

print("\n" + "=" * 80)
print("CALCULATING POINTS: WHOSCORED POSITIONS")
print("=" * 80)

whoscored_results = []
for i, match in enumerate(MATCHES, 1):
    print(f"\n[{i}/18] {match['name']}...")
    try:
        sofascore_adapter.reset_position_cache()
        # Calculate with WhoScored positions
        df = calc_all_players(match['sofascore'], whoscored_url=match['whoscored'])
        if not df.empty:
            df['match'] = match['name']
            whoscored_results.append(df[['name', 'score', 'pos', 'match']])
            print(f"  ✓ {len(df)} players")
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:40]}")
    time.sleep(0.5)

# Combine results
sf_df = pd.concat(sofascore_results, ignore_index=True) if sofascore_results else pd.DataFrame()
ws_df = pd.concat(whoscored_results, ignore_index=True) if whoscored_results else pd.DataFrame()

sf_df['name_lower'] = sf_df['name'].str.lower().str.strip()
ws_df['name_lower'] = ws_df['name'].str.lower().str.strip()

print(f"\n\nSofaScore calculated: {len(sf_df)} player entries")
print(f"WhoScored calculated: {len(ws_df)} player entries")

# === FAIR COMPARISON: Only players in BOTH AND Excel ===
print("\n" + "=" * 80)
print("FAIR POINTS COMPARISON: Starting XI only (players in both sources)")
print("=" * 80)

# Load fair comparison to get the 287 overlapping players
fair_pos_df = pd.read_csv("fair_position_comparison.csv")
overlapping_players = set(fair_pos_df['name_lower'].tolist())

# Filter to only overlapping players
sf_overlap = sf_df[sf_df['name_lower'].isin(overlapping_players)].copy()
ws_overlap = ws_df[ws_df['name_lower'].isin(overlapping_players)].copy()

# Merge with Excel for ground truth scores
sf_merged = sf_overlap.merge(excel_df[['name_lower', 'score']], on='name_lower', suffixes=('_calc', '_excel'))
ws_merged = ws_overlap.merge(excel_df[['name_lower', 'score']], on='name_lower', suffixes=('_calc', '_excel'))

# Calculate differences
sf_merged['diff'] = sf_merged['score_calc'] - sf_merged['score_excel']
sf_merged['abs_diff'] = sf_merged['diff'].abs()

ws_merged['diff'] = ws_merged['score_calc'] - ws_merged['score_excel']
ws_merged['abs_diff'] = ws_merged['diff'].abs()

# Statistics
def calc_stats(df, label):
    total = len(df)
    exact = len(df[df['diff'] == 0])
    close_3 = len(df[(df['abs_diff'] >= 1) & (df['abs_diff'] <= 3)])
    close_5 = len(df[(df['abs_diff'] >= 4) & (df['abs_diff'] <= 5)])
    large = len(df[df['abs_diff'] > 5])
    avg_diff = df['abs_diff'].mean()
    return {
        'label': label,
        'total': total,
        'exact': exact,
        'close_3': close_3,
        'close_5': close_5,
        'large': large,
        'avg_diff': avg_diff,
        'exact_pct': 100 * exact / total if total else 0,
        'within_3_pct': 100 * (exact + close_3) / total if total else 0,
    }

sf_stats = calc_stats(sf_merged, 'SofaScore')
ws_stats = calc_stats(ws_merged, 'WhoScored')

print(f"\nPlayers compared (Starting XI): {sf_stats['total']}")

print("\n" + "=" * 80)
print("POINTS ACCURACY COMPARISON")
print("=" * 80)
print(f"\n{'Metric':<35} {'SofaScore':>15} {'WhoScored':>15}")
print("-" * 65)
print(f"{'Total Players':<35} {sf_stats['total']:>15} {ws_stats['total']:>15}")
print(f"{'Exact Matches (diff=0)':<35} {sf_stats['exact']:>15} {ws_stats['exact']:>15}")
print(f"{'Close (|diff| 1-3)':<35} {sf_stats['close_3']:>15} {ws_stats['close_3']:>15}")
print(f"{'Close (|diff| 4-5)':<35} {sf_stats['close_5']:>15} {ws_stats['close_5']:>15}")
print(f"{'Large (|diff| > 5)':<35} {sf_stats['large']:>15} {ws_stats['large']:>15}")
print(f"{'Average |diff|':<35} {sf_stats['avg_diff']:>14.2f} {ws_stats['avg_diff']:>14.2f}")
print(f"{'EXACT MATCH %':<35} {sf_stats['exact_pct']:>14.1f}% {ws_stats['exact_pct']:>14.1f}%")
print(f"{'WITHIN ±3 POINTS %':<35} {sf_stats['within_3_pct']:>14.1f}% {ws_stats['within_3_pct']:>14.1f}%")

print("\n" + "=" * 80)
# Determine winner based on exact matches and average difference
if sf_stats['exact'] > ws_stats['exact']:
    print(f"WINNER (by exact matches): SofaScore ({sf_stats['exact']} vs {ws_stats['exact']})")
elif ws_stats['exact'] > sf_stats['exact']:
    print(f"WINNER (by exact matches): WhoScored ({ws_stats['exact']} vs {sf_stats['exact']})")
else:
    print("TIE on exact matches")

if sf_stats['avg_diff'] < ws_stats['avg_diff']:
    print(f"WINNER (by avg diff): SofaScore ({sf_stats['avg_diff']:.2f} vs {ws_stats['avg_diff']:.2f})")
elif ws_stats['avg_diff'] < sf_stats['avg_diff']:
    print(f"WINNER (by avg diff): WhoScored ({ws_stats['avg_diff']:.2f} vs {sf_stats['avg_diff']:.2f})")
else:
    print("TIE on average difference")
print("=" * 80)

# Show large discrepancies from each
print(f"\n\nLarge Discrepancies (|diff| > 5) - SofaScore ({sf_stats['large']}):")
print("-" * 65)
sf_large = sf_merged[sf_merged['abs_diff'] > 5].sort_values('abs_diff', ascending=False).head(10)
for _, row in sf_large.iterrows():
    print(f"  {row['name'][:25]:<26} Calc={row['score_calc']:>3.0f}  Excel={row['score_excel']:>3.0f}  Diff={row['diff']:>+4.0f}")

print(f"\n\nLarge Discrepancies (|diff| > 5) - WhoScored ({ws_stats['large']}):")
print("-" * 65)
ws_large = ws_merged[ws_merged['abs_diff'] > 5].sort_values('abs_diff', ascending=False).head(10)
for _, row in ws_large.iterrows():
    print(f"  {row['name'][:25]:<26} Calc={row['score_calc']:>3.0f}  Excel={row['score_excel']:>3.0f}  Diff={row['diff']:>+4.0f}")

# Save results
sf_merged.to_csv("points_comparison_sofascore.csv", index=False)
ws_merged.to_csv("points_comparison_whoscored.csv", index=False)
print(f"\n\nResults saved to: points_comparison_sofascore.csv, points_comparison_whoscored.csv")
