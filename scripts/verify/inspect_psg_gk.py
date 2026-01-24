
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sofascore_adapter import get_player_stats_df

def inspect_psg_stats():
    match_url = "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854"
    print(f"Fetching stats for: {match_url}")
    
    try:
        df, _ = get_player_stats_df(match_url)
        
        # Filter for Chevalier (likely "Lucas Chevalier" or just "Chevalier")
        # Let's print all GKs to be sure
        gks = df[df['Pos'] == 'GK']
        
        print("\n" + "="*80)
        print("GOALKEEPER STATS DUMP")
        print("="*80)
        
        for _, row in gks.iterrows():
            print(f"Player: {row['Unnamed: 0_level_0_Player']}")
            print(f"Team: {row['Team']}")
            print("-" * 20)
            # Print ALL columns that have non-zero values to find hidden gems
            for col in df.columns:
                val = row[col]
                # Try to convert to float/int for checking zero
                try:
                    if float(val) != 0:
                        print(f"  {col}: {val}")
                except:
                    if val and str(val) != 'nan': # Print non-empty strings
                         print(f"  {col}: {val}")
            print("="*80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_psg_stats()
