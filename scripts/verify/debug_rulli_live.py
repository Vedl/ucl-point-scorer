
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def debug_rulli_live():
    url = "https://www.sofascore.com/football/match/olympique-de-marseille-liverpool/UsQH#id:14566821"
    
    df = calc_all_players(url)
    rulli = df[df['name'].str.contains("Rulli", na=False)].iloc[0]
    
    print("="*60)
    print("RULLI STATS IN FINAL DF (after processing)")
    print("="*60)
    print(f"Saves: {rulli.get('Performance_Saves', 'MISSING')}")
    print(f"High Claims: {rulli.get('Performance_HighClaims', 'MISSING')}")
    print(f"Runs Out: {rulli.get('Performance_RunsOut', 'MISSING')}")
    print(f"Recoveries: {rulli.get('Performance_Rec', 'MISSING')}")
    print(f"Passes: {rulli.get('Passes_Cmp', 'MISSING')}")
    print(f"Clearances: {rulli.get('Unnamed: 20_level_0_Clr', 'MISSING')}")
    print(f"Punches: {rulli.get('Performance_Punches', 'MISSING')}")
    print(f"PK Saved: {rulli.get('Performance_PKSaved', 'MISSING')}")
    print(f"Goals Conceded (GK): {rulli.get('Performance_GK_GoalsConceded', 'MISSING')}")
    print(f"Goals Conceded (calculated): {rulli.get('goals_conceded', 'MISSING')}")
    print(f"Minutes: {rulli.get('Unnamed: 5_level_0_Min', 'MISSING')}")
    print(f"Score: {rulli.get('score', 'MISSING')}")

if __name__ == "__main__":
    debug_rulli_live()
