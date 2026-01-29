
import sys
import os
import pandas as pd
from player_score_calculator import calc_all_players

# Adjust path to find modules
sys.path.append(os.getcwd())

def reproduce():
    # Ajax vs Olympiacos (Round 8)
    match_id = 14566875
    # Construct a valid-looking URL pattern for the adapter
    url = f"https://www.sofascore.com/olympiacos-fc-afc-ajax/x#id:{match_id}"
    
    print(f"Fetching data for match ID {match_id}...")
    
    try:
        df = calc_all_players(url)
        
        # Filter for Rodinei
        rodinei = df[df['name'].str.contains("Rodinei", case=False, na=False)]
        
        if rodinei.empty:
            print("Rodinei not found in match data!")
            # Print all Olympiacos players to check names
            print("All Players Found:")
            print(df['name'].unique())
        else:
            print("\nRodinei Stats:")
            print(rodinei[['name', 'Pos', 'score', 'minutes_played', 'goals_scored', 'goals_conceded']].to_string())
            
            # Check position
            pos = rodinei['Pos'].values[0]
            print(f"\nAssigned Position: {pos}")
            
            if pos == 'DEF':
                print("ISSUE REPRODUCED: Rodinei is classified as DEF.")
            else:
                print(f"Rodinei is classified as {pos}. Issue NOT reproduced?")
                
    except Exception as e:
        print(f"Error reproduction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
