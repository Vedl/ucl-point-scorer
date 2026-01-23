
import pandas as pd
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from player_score_calculator import calc_all_players

def verify_gk_logic():
    # Union SG vs Bayern (known working match ID)
    # Using a constructed URL that should work with the adapter
    match_url = "https://www.sofascore.com/union-saint-gilloise-fc-bayern-munchen/xdbsob#id:14566573"
    
    print(f"Testing GK Logic on: {match_url}")
    
    try:
        df = calc_all_players(match_url)
        
        if df.empty:
            print("No data returned.")
            return

        # Filter for Goalkeepers
        gks = df[df['pos'] == 'GK']
        
        if gks.empty:
            print("No GKs found.")
            return

        print("\n" + "="*80)
        print(f"{'PLAYER':<20} {'SCORE':<6} {'SAVES':<6} {'CLAIMS':<6} {'PUNCH':<6} {'RUNOUT':<6} {'PASS':<6} {'CONC':<6}")
        print("="*80)
        
        for _, row in gks.iterrows():
            name = row['name']
            score = row['score']
            saves = row.get('Performance_Saves', 0)
            claims = row.get('Performance_HighClaims', 0)
            punches = row.get('Performance_Punches', 0)
            runs_out = row.get('Performance_RunsOut', 0)
            passes = row.get('Passes_Cmp', 0)
            conceded = row.get('Performance_GK_GoalsConceded', 0)
            clean_sheet = 10 if conceded == 0 else (10 - 5 * conceded)
            
            # Manual Check
            # Formula:
            # + Conceded Pts (10 - 5*conceded)
            # + 1.3 * Saves
            # + 1.0 * HighClaims
            # + 0.5 * Punches
            # + 1.5 * RunsOut
            # + 0.1 * Passes
            # + Other defensive stats (Tackles, Ints, etc.)
            
            expected_partial = (
                clean_sheet + 
                (1.3 * saves) + 
                (1.0 * claims) + 
                (0.5 * punches) + 
                (1.5 * runs_out) + 
                (0.1 * passes)
            )
            
            print(f"{name:<20} {score:<6} {saves:<6} {claims:<6} {punches:<6} {runs_out:<6} {passes:<6} {conceded:<6}")
            print(f"  -> Partial Expected (Main Stats): {expected_partial:.2f}")
            print(f"  -> Actual Score: {score}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_gk_logic()
