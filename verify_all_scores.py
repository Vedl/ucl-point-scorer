"""
Comprehensive Score Verification Script
Compares calculated player scores against the Excel ground truth.
"""
import pandas as pd
from player_score_calculator import calc_all_players
import os

# Load Excel ground truth
EXCEL_PATH = "Gameweek 4 UCL 25:26 Points.xlsx"
excel_df = pd.read_excel(EXCEL_PATH)
excel_df['name_lower'] = excel_df['name'].str.lower().str.strip()

print(f"Loaded {len(excel_df)} players from Excel")

# Known match for verification (BVB vs Man City)
TEST_MATCH = {
    'sofascore': "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662",
    'whoscored': "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"
}

print(f"\n--- Testing Match: BVB vs Man City ---")
print(f"SofaScore: {TEST_MATCH['sofascore']}")
print(f"WhoScored: {TEST_MATCH['whoscored']}")

# Calculate scores
calculated_df = calc_all_players(TEST_MATCH['sofascore'], TEST_MATCH['whoscored'])

if calculated_df.empty:
    print("ERROR: No data returned from calculator!")
    exit(1)

calculated_df['name_lower'] = calculated_df['name'].str.lower().str.strip()

# Merge with Excel data
comparison = calculated_df.merge(
    excel_df[['name_lower', 'score', 'pos']],
    on='name_lower',
    how='inner',
    suffixes=('_calc', '_excel')
)

print(f"\nMatched {len(comparison)} players between calculated and Excel")

# Calculate differences
comparison['diff'] = comparison['score_calc'] - comparison['score_excel']
comparison['pos_match'] = comparison['pos_calc'] == comparison['pos_excel']

# Sort by absolute difference
comparison['abs_diff'] = comparison['diff'].abs()
comparison = comparison.sort_values('abs_diff', ascending=False)

# Show summary
print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

exact_matches = len(comparison[comparison['diff'] == 0])
close_matches = len(comparison[(comparison['diff'].abs() <= 3) & (comparison['diff'] != 0)])
large_diffs = len(comparison[comparison['diff'].abs() > 3])
pos_mismatches = len(comparison[~comparison['pos_match']])

print(f"Exact matches (diff=0):        {exact_matches}")
print(f"Close matches (|diff| <= 3):   {close_matches}")
print(f"Large differences (|diff| > 3): {large_diffs}")
print(f"Position mismatches:           {pos_mismatches}")

# Show all players with differences
print("\n" + "=" * 80)
print("ALL PLAYER COMPARISONS (sorted by difference)")
print("=" * 80)
print(f"{'Player':<25} {'Calc':>6} {'Excel':>6} {'Diff':>6} {'CalcPos':>8} {'ExcelPos':>8} {'Match':>6}")
print("-" * 80)

for _, row in comparison.iterrows():
    pos_status = "✓" if row['pos_match'] else "✗"
    diff_str = f"{row['diff']:+.0f}" if row['diff'] != 0 else "0"
    print(f"{row['name'][:24]:<25} {row['score_calc']:>6.0f} {row['score_excel']:>6.0f} {diff_str:>6} {row['pos_calc']:>8} {row['pos_excel']:>8} {pos_status:>6}")

# Show players with large discrepancies
if large_diffs > 0:
    print("\n" + "=" * 80)
    print("PLAYERS WITH LARGE DISCREPANCIES (|diff| > 3)")
    print("=" * 80)
    
    large_diff_df = comparison[comparison['diff'].abs() > 3]
    for _, row in large_diff_df.iterrows():
        print(f"\n{row['name']}:")
        print(f"  Calculated: {row['score_calc']:.0f} ({row['pos_calc']})")
        print(f"  Expected:   {row['score_excel']:.0f} ({row['pos_excel']})")
        print(f"  Difference: {row['diff']:+.0f}")
        if not row['pos_match']:
            print(f"  ⚠️  POSITION MISMATCH!")

# Save full comparison to CSV for review
comparison.to_csv("score_verification_results.csv", index=False)
print(f"\nFull comparison saved to: score_verification_results.csv")
