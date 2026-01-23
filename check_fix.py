from player_score_calculator import calc_all_players
import pandas as pd

def check_fix():
    url = "https://www.sofascore.com/football/match/borussia-dortmund-manchester-city/rsydb#id:14566662"
    print(f"Checking Match: {url}")
    df = calc_all_players(url)
    
    targets = ["Ryerson", "Svensson"]
    for t in targets:
        row = df[df['name'].str.contains(t, case=False)]
        if not row.empty:
            print(f"\nPlayer: {row['name'].values[0]}")
            print(f"Pos: {row['pos'].values[0]}")
            print(f"Score: {row['score'].values[0]}")
        else:
            print(f"Player {t} not found.")

if __name__ == "__main__":
    check_fix()
