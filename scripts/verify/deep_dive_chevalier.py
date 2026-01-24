
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sofascore_adapter import get_player_stats_df

def deep_dive_chevalier():
    match_url = "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854"
    print(f"Deep diving: {match_url}")
    
    df, match_events = get_player_stats_df(match_url)
    
    # Filter Chevalier
    cheva = df[df['Unnamed: 0_level_0_Player'].str.contains("Chevalier", na=False)]
    
    if cheva.empty:
        print("Chevalier not found!")
        return
        
    row = cheva.iloc[0]
    
    print("\n" + "="*80)
    print("CHEVALIER RAW STATS")
    print("="*80)
    
    for col in df.columns:
        val = row[col]
        try:
             # Print if numeric and non-zero, or if string
            if isinstance(val, (int, float)):
                if val != 0:
                    print(f"{col}: {val}")
            else:
                print(f"{col}: {val}")
        except:
            pass
            
    print("="*80)
    
    # Also Check Scoreline from events
    goals = [e for e in match_events if e['event_kind'] == 'Goal']
    print(f"Goals in match: {len(goals)}")
    for g in goals:
        print(f" - {g['time']}: {g['player']} ({g.get('team', 'Unknown Team')})")

if __name__ == "__main__":
    deep_dive_chevalier()
