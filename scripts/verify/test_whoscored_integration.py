"""Test WhoScored integration for accurate position classification."""
from player_score_calculator import calc_all_players

# Match: Man City vs Borussia Dortmund (2025/26 UCL)
SOFASCORE_URL = "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662"
WHOSCORED_URL = "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"

print("=" * 60)
print("Testing WhoScored Position Integration")
print("=" * 60)

print(f"\nSofaScore URL: {SOFASCORE_URL}")
print(f"WhoScored URL: {WHOSCORED_URL}")

# Calculate with WhoScored position override
print("\n--- Fetching data (with WhoScored positions)... ---")
df = calc_all_players(SOFASCORE_URL, WHOSCORED_URL)

if df.empty:
    print("ERROR: No data returned!")
    exit(1)

# Check target players
targets = {
    "Ryerson": {"expected_pos": "DEF", "expected_score_range": (15, 25)},
    "Svensson": {"expected_pos": "DEF", "expected_score_range": (5, 15)},
}

print("\n--- Verification Results ---")
all_passed = True

for name, expected in targets.items():
    row = df[df['name'].str.contains(name, case=False)]
    
    if row.empty:
        print(f"❌ {name}: NOT FOUND in results")
        all_passed = False
        continue
    
    actual_pos = row['pos'].values[0]
    actual_score = int(row['score'].values[0])
    
    pos_ok = actual_pos == expected["expected_pos"]
    score_ok = expected["expected_score_range"][0] <= actual_score <= expected["expected_score_range"][1]
    
    status = "✅" if (pos_ok and score_ok) else "⚠️" if pos_ok else "❌"
    
    print(f"{status} {name}: Pos={actual_pos} (expected {expected['expected_pos']}), Score={actual_score}")
    
    if not pos_ok:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("✅ ALL TESTS PASSED - WhoScored integration working!")
else:
    print("❌ SOME TESTS FAILED - Check output above")
print("=" * 60)
