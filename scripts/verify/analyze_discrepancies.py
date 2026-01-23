"""
Deep dive into players with large score discrepancies.
Analyzes the raw stats to understand why calculated differs from Excel.
"""
import pandas as pd
from player_score_calculator import calc_all_players

# Match: BVB vs Man City
SOFASCORE_URL = "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662"
WHOSCORED_URL = "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"

# Load Excel
excel_df = pd.read_excel("Gameweek 4 UCL 25:26 Points.xlsx")

# Get calculated data
print("Fetching match data...")
df = calc_all_players(SOFASCORE_URL, WHOSCORED_URL)

# Players with large discrepancies
targets = ["Fábio Silva", "Tijjani Reijnders", "Karim Adeyemi"]

print("\n" + "=" * 80)
print("DETAILED ANALYSIS OF LARGE DISCREPANCIES")
print("=" * 80)

# Key stats that affect scoring
key_stats = [
    'Unnamed: 0_level_0_Player',  # Name
    'Pos',  # Position used
    'Unnamed: 5_level_0_Min',  # Minutes
    'Performance_Gls',  # Goals
    'Performance_Ast',  # Assists
    'Performance_Tkl',  # Tackles
    'Performance_Int',  # Interceptions
    'Unnamed: 20_level_0_Clr',  # Clearances
    'Aerial Duels_Won',
    'Aerial Duels_Lost',
    'Challenges_Lost',  # Dribbled past
    'Passes_Cmp',
    'Passes_Att',
    'Take-Ons_Succ',
    'Take-Ons_Att',
    'Performance_Sh',  # Shots
    'Performance_SoT',  # Shots on target
    'Performance_CrdY',
    'Performance_CrdR',
    'goals_scored',  # Team goals while on pitch
    'goals_conceded',  # Team conceded while on pitch
    'score',  # Final calculated score
]

for target in targets:
    row = df[df['name'].str.contains(target, case=False, na=False)]
    excel_row = excel_df[excel_df['name'].str.contains(target, case=False, na=False)]
    
    if row.empty:
        print(f"\n{target}: NOT FOUND in calculated data")
        continue
    
    print(f"\n{'=' * 40}")
    print(f"PLAYER: {target}")
    print(f"{'=' * 40}")
    
    calc_score = int(row['score'].values[0])
    excel_score = int(excel_row['score'].values[0]) if not excel_row.empty else "N/A"
    diff = calc_score - excel_score if excel_score != "N/A" else "N/A"
    
    print(f"Calculated Score: {calc_score}")
    print(f"Excel Score:      {excel_score}")
    print(f"Difference:       {diff}")
    print(f"\nPosition: {row['Pos'].values[0]} (Excel: {excel_row['pos'].values[0] if not excel_row.empty else 'N/A'})")
    
    print(f"\n--- Key Stats ---")
    for stat in key_stats:
        if stat in row.columns:
            val = row[stat].values[0]
            # Format: truncate long strings
            if isinstance(val, str) and len(val) > 30:
                val = val[:30] + "..."
            print(f"  {stat}: {val}")

print("\n" + "=" * 80)
print("ANALYSIS NOTES:")
print("=" * 80)
print("""
Differences could be due to:
1. Different data source (SofaScore vs original FBref data used for Excel)
2. Stat counting differences (e.g., what counts as a 'tackle')
3. Goals scored/conceded calculation (tracking substitutions)
4. Rounding differences in formula

Small differences (±3) are expected due to data source variations.
Larger differences (±4-5) may indicate formula or stat mapping issues.
""")
