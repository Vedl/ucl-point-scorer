from player_score_calculator import calc_all_players
import pandas as pd

def test_scoring():
    # Real Madrid vs Dortmund 2024 Final
    # Using a constructed URL that the adapter can parse
    url = "https://www.sofascore.com/borussia-dortmund-real-madrid/Ebsydb#id:12173509"
    
    print(f"Testing scoring for: {url}")
    try:
        df = calc_all_players(url)
        
        if df.empty:
            print("FAILED: Result DataFrame is empty.")
        else:
            print("SUCCESS: Scoring completed.")
            print("\n--- SAMPLE SCORES ---")
            print(df.head(10))
            
            # Check for NaN or weird values
            if df['score'].isnull().any():
                print("WARNING: NaNs found in scores.")
            
            # Verify specific star players exist
            stars = ['Vinícius Júnior', 'Jude Bellingham', 'Mats Hummels']
            for star in stars:
                entry = df[df['name'].str.contains(star, case=False)]
                if not entry.empty:
                    print(f"\nScore for {star}: {entry['score'].values[0]} ({entry['pos'].values[0]})")
                else:
                    print(f"\nWARNING: Star player '{star}' not found in results.")

    except Exception as e:
        print(f"FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scoring()
