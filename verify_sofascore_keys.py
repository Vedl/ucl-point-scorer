from ScraperFC import Sofascore
import pandas as pd
import json

def verify_sofascore_keys():
    sfs = Sofascore()
    
    print("Fetching UCL matches...")
    # Get matches from the 23/24 season to ensure we have completed games with full stats
    matches = sfs.get_match_dicts(year='24/25', league='UEFA Champions League')
    
    if not matches:
        print("No matches found for 24/25, trying 23/24...")
        matches = sfs.get_match_dicts(year='23/24', league='UEFA Champions League')
        
    if not matches:
        print("Could not find any UCL matches.")
        return

    # Pick a match that has finished (status code 100 often denotes finished, or just check 'status')
    # We'll just take the last one in the list as it's likely the most recent or a final
    target_match = matches[-1]
    print(f"Inspecting Match: {target_match.get('slug', 'Unknown')} (ID: {target_match['id']})")
    
    try:
        df = sfs.scrape_player_match_stats(match_id=target_match['id'])
        
        if df.empty:
            print("DataFrame is empty.")
            return

        print("\n--- ALL AVAILABLE COLUMNS ---")
        for col in sorted(df.columns):
            print(f"- {col}")
            
        print("\n--- SAMPLE ROW (First Player) ---")
        # Print non-null values of the first row to see data structure
        sample = df.iloc[0].dropna().to_dict()
        print(json.dumps(sample, default=str, indent=2))
        
        print("\n--- CRITICAL KEY CHECK ---")
        required_keys = ['challengeLost', 'dribbledPast', 'errorLeadToShot', 'errorLeadToGoal', 'dispossessed', 'possessionLost']
        for key in required_keys:
            if key in df.columns:
                print(f"[FOUND] {key}")
            else:
                print(f"[MISSING] {key}")

    except Exception as e:
        print(f"Error scraping match: {e}")

if __name__ == "__main__":
    verify_sofascore_keys()
