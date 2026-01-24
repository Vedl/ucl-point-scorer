
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sofascore_adapter import get_player_stats_df
from player_score_calculator import calc_all_players

def debug_rulli():
    url = "https://www.sofascore.com/football/match/olympique-de-marseille-liverpool/UsQH#id:14566821"
    
    # Get raw stats
    df_raw, _ = get_player_stats_df(url)
    rulli = df_raw[df_raw['Unnamed: 0_level_0_Player'].str.contains("Rulli", na=False)].iloc[0]
    
    print("="*60)
    print("RULLI RAW STATS FROM ADAPTER")
    print("="*60)
    print(f"Saves: {rulli.get('Performance_Saves', 'MISSING')}")
    print(f"High Claims: {rulli.get('Performance_HighClaims', 'MISSING')}")
    print(f"Runs Out: {rulli.get('Performance_RunsOut', 'MISSING')}")
    print(f"Recoveries: {rulli.get('Performance_Rec', 'MISSING')}")
    print(f"Passes: {rulli.get('Passes_Cmp', 'MISSING')}")
    print(f"Clearances: {rulli.get('Unnamed: 20_level_0_Clr', 'MISSING')}")
    print(f"Punches: {rulli.get('Performance_Punches', 'MISSING')}")
    print(f"PK Saved: {rulli.get('Performance_PKSaved', 'MISSING')}")
    print(f"Goals Conceded: {rulli.get('Performance_GK_GoalsConceded', 'MISSING')}")
    print(f"Minutes: {rulli.get('Unnamed: 5_level_0_Min', 'MISSING')}")
    
    # Manual calculation using formula
    print("\n" + "="*60)
    print("MANUAL CALCULATION")
    print("="*60)
    
    saves = float(rulli.get('Performance_Saves', 0) or 0)
    claims = float(rulli.get('Performance_HighClaims', 0) or 0)
    sweeper = float(rulli.get('Performance_RunsOut', 0) or 0)
    rec = float(rulli.get('Performance_Rec', 0) or 0)
    passes = float(rulli.get('Passes_Cmp', 0) or 0)
    clears = float(rulli.get('Unnamed: 20_level_0_Clr', 0) or 0)
    punch = float(rulli.get('Performance_Punches', 0) or 0)
    conceded = float(rulli.get('Performance_GK_GoalsConceded', 0) or 0)
    mins = float(rulli.get('Unnamed: 5_level_0_Min', 0) or 0)
    
    conceded_pts = 10 - (5 * conceded)
    mins_bonus = mins / 30
    
    score = (
        5.67 * saves
        + 2.42 * claims
        + 3.01 * sweeper
        + 0.63 * rec
        + 0.88 * clears
        - 0.32 * passes
        + conceded_pts
        + 0.5 * punch
        + mins_bonus
    )
    
    print(f"5.67 * {saves} (saves) = {5.67*saves:.2f}")
    print(f"2.42 * {claims} (claims) = {2.42*claims:.2f}")
    print(f"3.01 * {sweeper} (sweeper) = {3.01*sweeper:.2f}")
    print(f"0.63 * {rec} (rec) = {0.63*rec:.2f}")
    print(f"0.88 * {clears} (clears) = {0.88*clears:.2f}")
    print(f"-0.32 * {passes} (passes) = {-0.32*passes:.2f}")
    print(f"Conceded pts ({conceded} goals): {conceded_pts:.2f}")
    print(f"0.5 * {punch} (punch) = {0.5*punch:.2f}")
    print(f"Mins bonus ({mins}/30): {mins_bonus:.2f}")
    print(f"\nTOTAL: {score:.2f} -> Rounded: {round(score)}")

if __name__ == "__main__":
    debug_rulli()
