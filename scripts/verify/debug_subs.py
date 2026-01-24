
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players
from sofascore_adapter import get_player_stats_df

def debug_subs():
    match_url = "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854"
    print(f"Debugging subs for: {match_url}")
    
    # Get raw data first
    df_raw, events = get_player_stats_df(match_url)
    
    print("\n" + "="*80)
    print("RAW DATA: Players with is_sub=True")
    print("="*80)
    
    subs = df_raw[df_raw['is_sub'] == True]
    for _, row in subs.iterrows():
        name = row['Unnamed: 0_level_0_Player']
        mins = row['Unnamed: 5_level_0_Min']
        team = row['Team']
        print(f"  {name:<25} Team={team} MinutesPlayed={mins}")
    
    print("\n" + "="*80)
    print("FINAL OUTPUT: Players in scores list")
    print("="*80)
    
    df_final = calc_all_players(match_url)
    
    # Check if any player with 0 min in raw data made it to final
    for _, row in df_final.iterrows():
        name = row['name']
        score = row['score']
        mins = row.get('minutes_played', 'N/A')
        pos = row['pos']
        print(f"  {name:<25} Pos={pos} Score={score:<4} MinutesPlayed={mins}")

if __name__ == "__main__":
    debug_subs()
