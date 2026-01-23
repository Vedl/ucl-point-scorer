"""
Deep analysis of the 12 players with large discrepancies (|diff| > 5).
"""
import pandas as pd

# Load verification results
df = pd.read_csv("full_verification_results.csv")

# Filter large discrepancies
large_diff = df[df['abs_diff'] > 5].sort_values('abs_diff', ascending=False)

print("=" * 100)
print("DETAILED ANALYSIS OF 12 LARGE DISCREPANCIES")
print("=" * 100)

# Key stats columns to analyze
stat_cols = [
    'Unnamed: 5_level_0_Min',  # Minutes
    'Performance_Gls',  # Goals
    'Performance_Ast',  # Assists
    'Performance_Tkl',  # Tackles
    'Performance_Int',  # Interceptions
    'Passes_Cmp',
    'Passes_Att',
    'goals_scored',
    'goals_conceded',
]

for _, row in large_diff.iterrows():
    print(f"\n{'=' * 50}")
    print(f"PLAYER: {row['name']}")
    print(f"{'=' * 50}")
    print(f"Match:      {row['match']}")
    print(f"Position:   {row['pos_calc']} (same as Excel: {row['pos_match']})")
    print(f"Calculated: {row['score_calc']:.0f}")
    print(f"Excel:      {row['score_excel']:.0f}")
    print(f"Difference: {row['diff']:+.0f}")
    
    print(f"\nKey Stats:")
    for col in stat_cols:
        if col in df.columns:
            val = row.get(col, 'N/A')
            if pd.notna(val):
                print(f"  {col}: {val}")

print("\n" + "=" * 100)
print("ANALYSIS SUMMARY")
print("=" * 100)
print("""
Key observations:
1. All position matches are correct (0 mismatches)
2. Discrepancies are likely due to:
   - Different data sources (SofaScore vs FBref for Excel)
   - Stat counting differences between providers
   - Goals scored/conceded calculation timing
   
3. The largest discrepancies (+/- 12) are for:
   - Anton Gaaei: May have different minutes tracking
   - Victor Osimhen: 2 goals/assists stats difference
   
4. Most discrepancies are in the ±6-8 range
""")

# Check if any patterns emerge
print("\n" + "=" * 100)
print("STATISTICAL PATTERNS")
print("=" * 100)
print(f"Average discrepancy for all verified players: {df['diff'].mean():.2f}")
print(f"Standard deviation: {df['abs_diff'].std():.2f}")
print(f"Median absolute difference: {df['abs_diff'].median():.1f}")

# By position
print("\nBy Position:")
for pos in df['pos_calc'].unique():
    pos_data = df[df['pos_calc'] == pos]
    print(f"  {pos}: Avg diff = {pos_data['diff'].mean():+.2f}, Avg |diff| = {pos_data['abs_diff'].mean():.2f}")
