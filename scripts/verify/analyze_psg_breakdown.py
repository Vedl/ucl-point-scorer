
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def analyze_psg_match():
    match_url = "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854"
    print(f"Processing: {match_url}")
    
    df = calc_all_players(match_url)
    
    print("\n" + "="*80)
    print("DETAILED SCORING BREAKDOWN")
    print("="*80)
    
    # Check Chevalier
    player = df[df['name'].str.contains("Chevalier", na=False)]
    if not player.empty:
        row = player.iloc[0]
        print(f"Player: {row['name']}")
        print(f"Position: {row['pos']}")
        print(f"Calculated Score: {row['score']}")
        print(f"Minutes Played: {row['minutes_played']}")
        print(f"Goals Conceded: {row['goals_conceded']}")
        print(f"Team Scored: {row['goals_scored']}")
        
        # Print breakdown components
        saves = row.get('Performance_Saves', 0)
        pk_saved = row.get('Performance_PKSaved', 0)
        claims = row.get('Performance_HighClaims', 0)
        passes = row.get('Passes_Cmp', 0)
        
        print(f"Stats - Saves: {saves}, PKSaved: {pk_saved}, Claims: {claims}, Passes: {passes}")
        
    else:
        print("Chevalier not found in output.")

if __name__ == "__main__":
    analyze_psg_match()
