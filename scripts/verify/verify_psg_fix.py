
import pandas as pd
import sys
import os

# Create dummy verify script based on analyze_psg_breakdown
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def verify_fix():
    match_url = "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854"
    print(f"Verifying Fix on: {match_url}")
    
    df = calc_all_players(match_url)
    
    # Check Chevalier
    player = df[df['name'].str.contains("Chevalier", na=False)]
    if not player.empty:
        row = player.iloc[0]
        score = row['score']
        print(f"Player: {row['name']}")
        print(f"New Score: {score}")
        
        if score >= 22 and score <= 24:
            print("✅ SUCCESS: Score is within range of 23.")
        else:
            print(f"❌ FAIL: Score {score} is not close to 23.")
            
        # Also Check Neuer (Proxy for regression test)
        # Note: can't easily check Neuer here without fetching another match, 
        # but the prompt focuses on PSG.
    else:
        print("Chevalier not found.")

if __name__ == "__main__":
    verify_fix()
