
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def verify_all():
    matches = [
        # Match 1: Marseille vs Liverpool (R6? No, R6 was 42pts for Alisson?)
        # User said Gameweek 1: Marseille 62, Liverpool 26.
        # User said Gameweek 2: Marseille 39, Liverpool 32.
        # User said Gameweek 6: Marseille 40, Liverpool 42.
        # Match 14566821 is Round 7 in API but user might call it GW something else or I mixed it up.
        # Let's rely on my 'collect_massive_data' mapping.
        # For R1 Marseille (Rulli) Target 62. Alisson Target 26.
        # Let's verify R1 specifically.
        # But verify_all_gks uses specific URLs. I need to know which Match ID corresponds to which User GW.
        # Match 14566821 (Marseille vs Liverpool) is Round 7 in meta?
        # User GW7 targets? "Gameweek 7 - you already have."
        # Ah, maybe 14566821 is user GW7?
        # Let's use the Rulli=62 match which is likely R1.
        # R1 match was Open? No, R1 was maybe vs someone else?
        # In 'collect_massive_data' output:
        # Added Gerónimo Rulli (R1 Olympique de Marseille): Target 62.
        # Match was 14566597 (Real vs Marseille?? No that ID was listed as R1?)
        # Let's just trust the massive dump and check a few key ones I know.
        
        # Real vs City (R108 in dump? No R6 match 14566595)
        # User R6: Real 36, City 18.
        ("Real vs City", "https://www.sofascore.com/football/match/real-madrid-manchester-city/rsEgb#id:14566595",
         [("Courtois", 36), ("Donnarumma", 18)]),
         
        # Inter vs Arsenal (R4)
        # User R4: Inter 29, Arsenal 33.
        # My verification script says Inter vs Arsenal ID 14566612.
        ("Inter vs Arsenal", "https://www.sofascore.com/football/match/inter-arsenal/RsXdb#id:14566612",
         [("Sommer", 29), ("Raya", 33)]),
         
        # Arsenal vs PSG (R2)
        # User R2: Arsenal 41, PSG 25.
        ("Arsenal vs PSG", "https://www.sofascore.com/football/match/arsenal-paris-saint-germain/UHsRdb#id:14566603",
         [("Raya", 41), ("Chevalier", 25)]),
    ]
    
    passed_count = 0
    total_count = 0
    
    for match_name, url, targets in matches:
        print(f"\n{'='*60}")
        print(f"Match: {match_name}")
        print(f"{'='*60}")
        
        try:
            df = calc_all_players(url)
            gks = df[df['pos'] == 'GK']
            
            for name_part, expected in targets:
                total_count += 1
                player = gks[gks['name'].str.contains(name_part, na=False, case=False)]
                if player.empty:
                    # Try partial match or manual check
                    print(f"❌ {name_part}: NOT FOUND in GK list: {gks['name'].tolist()}")
                    continue
                    
                actual = int(player.iloc[0]['score'])
                diff = actual - expected
                status = "✅" if abs(diff) <= 2 else "❌"  # Allowing slight tolerance due to rounding
                if abs(diff) <= 2:
                    passed_count += 1
                
                print(f"{status} {name_part:<20}: Expected={expected}, Got={actual}, Diff={diff:+d}")
        except Exception as e:
            print(f"⚠️ Error processing match {match_name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Passed: {passed_count}/{total_count}")
    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")

if __name__ == "__main__":
    verify_all()
