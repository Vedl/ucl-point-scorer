
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from player_score_calculator import calc_all_players

def verify_all():
    matches = [
        ("Marseille vs Liverpool", "https://www.sofascore.com/football/match/olympique-de-marseille-liverpool/UsQH#id:14566821", 
         [("Alisson", 45), ("Rulli", 17)]),
        ("Sporting vs PSG", "https://www.sofascore.com/football/match/sporting-paris-saint-germain/UHsbkb#id:14566854",
         [("Chevalier", 23)]),
    ]
    
    all_passed = True
    
    for match_name, url, targets in matches:
        print(f"\n{'='*60}")
        print(f"Match: {match_name}")
        print(f"{'='*60}")
        
        df = calc_all_players(url)
        gks = df[df['pos'] == 'GK']
        
        for name_part, expected in targets:
            player = gks[gks['name'].str.contains(name_part, na=False)]
            if player.empty:
                print(f"❌ {name_part}: NOT FOUND")
                all_passed = False
                continue
                
            actual = int(player.iloc[0]['score'])
            status = "✅" if actual == expected else "❌"
            if actual != expected:
                all_passed = False
            print(f"{status} {name_part}: Expected={expected}, Got={actual}, Diff={actual-expected:+d}")
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")

if __name__ == "__main__":
    verify_all()
