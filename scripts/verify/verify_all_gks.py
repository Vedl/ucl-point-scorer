
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def verify_all():
    matches = [
        # Match 1: Marseille vs Liverpool
        ("Marseille vs Liverpool", "https://www.sofascore.com/football/match/olympique-de-marseille-liverpool/UsQH#id:14566821", 
         [("Alisson", 45), ("Rulli", 17)]),
         
        # Match 2: Sporting vs PSG
        ("Sporting vs PSG", "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854",
         [("Chevalier", 23)]),
         
        # Match 3: Bayern vs Union SG (Bayern is HOME)
        # Note: Neuer is HOME GK
        ("Bayern vs Union SG", "https://www.sofascore.com/football/match/royale-union-saint-gilloise-fc-bayern-munchen/xdbskXb#id:14566573",
         [("Neuer", 35)]),
         
        # Match 4: Inter vs Arsenal
        ("Inter vs Arsenal", "https://www.sofascore.com/football/match/inter-arsenal/RsXdb#id:14566612",
         [("Sommer", 19), ("Raya", 34)]),
         
        # Match 5: Bodo vs Man City (City is AWAY)
        ("Bodo vs Man City", "https://www.sofascore.com/football/match/manchester-city-bodo-glimt/rsgn#id:14566841",
         [("Donnarumma", 16)]),
         
        # Match 6: Barca vs Slavia (Barca is AWAY)
        ("Barca vs Slavia", "https://www.sofascore.com/football/match/barcelona-sk-slavia-praha/qUsrgb#id:14566882",
         [("Joan García", 22)]),
         
        # Match 7: Napoli vs Copenhagen (Napoli is AWAY)
        ("Napoli vs Copenhagen", "https://www.sofascore.com/football/match/napoli-fc-kobenhavn/JAsoeb#id:14566973",
         [("Milinković-Savić", 44)]),
         
        # Match 8: Galata vs Atletico (Atletico is AWAY)
        ("Galata vs Atletico", "https://www.sofascore.com/football/match/galatasaray-atletico-madrid/Lgbsllb#id:14566935",
         [("Oblak", 30)]),
         
        # Match 9: Real vs Monaco (Real is HOME)
        ("Real vs Monaco", "https://www.sofascore.com/football/match/real-madrid-as-monaco/dIsEgb#id:14566598",
         [("Courtois", 37)]),
         
        # Match 10: Benfica vs Juve (Juve is HOME)
        ("Benfica vs Juve", "https://www.sofascore.com/football/match/benfica-juventus/Mdbsgkb#id:14566765",
         [("Di Gregorio", 37)]),

        # Match 11: Dortmund vs Spurs (Spurs is HOME)
        ("Dortmund vs Spurs", "https://www.sofascore.com/football/match/borussia-dortmund-tottenham-hotspur/Isydb#id:14566826",
         [("Vicario", 35)]),
         
        # Match 12: PSV vs Newcastle (Newcastle is HOME)
        ("PSV vs Newcastle", "https://www.sofascore.com/football/match/psv-eindhoven-newcastle-united/Oscjb#id:14566957",
         [("Pope", 32)]),
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
