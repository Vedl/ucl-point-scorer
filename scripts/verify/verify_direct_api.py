import requests
import pandas as pd
import json

def verify_direct_api_keys():
    # Real Madrid vs Dortmund 2024 Final Match ID (Approximate or Known)
    # We can try a known recent match ID. 
    # Example: Real Madrid vs Dortmund (01/06/2024) -> ID: 12151439 (I'll need to check or search for this if this is wrong)
    # Let's try to search for a match first or use a hardcoded one if we can find it.
    
    # Actually, let's try to list matches first to get a valid ID 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 23/24 UCL Season ID: 52162. Unique Tournament ID: 7
    # Get last matches
    print("Fetching matches...")
    url_matches = "https://api.sofascore.com/api/v1/unique-tournament/7/season/52162/events/last/0"
    
    try:
        r = requests.get(url_matches, headers=headers)
        if r.status_code != 200:
            print(f"Failed to fetch matches: {r.status_code}")
            # Try a hardcoded ID for 2024 Final: 11874287 (Dortmund 0 - 2 Real Madrid)
            match_id = 11874287
            print(f"Using fallback match ID: {match_id}")
        else:
            data = r.json()
            events = data.get('events', [])
            if not events:
                match_id = 11874287
            else:
                match_id = events[0]['id']
                print(f"Found match: {events[0]['slug']} ({match_id})")

        print(f"Fetching lineups for match {match_id}...")
        url_lineups = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
        r_lineups = requests.get(url_lineups, headers=headers)
        
        if r_lineups.status_code != 200:
            print(f"Failed to fetch lineups: {r_lineups.status_code}")
            return
            
        data = r_lineups.json()
        home_players = data['home']['players']
        away_players = data['away']['players']
        all_players = home_players + away_players
        
        # Flatten stats
        processed_data = []
        for p in all_players:
            entry = p.get('statistics', {})
            entry['name'] = p['player']['name']
            entry['position'] = p.get('position', 'Unknown')
            processed_data.append(entry)
            
        df = pd.DataFrame(processed_data)
        
        if df.empty:
            print("No stats data found.")
            return

        print("\n--- ALL AVAILABLE COLUMNS ---")
        for col in sorted(df.columns):
            print(f"- {col}")
            
        print("\n--- SAMPLE ROW (First Player) ---")
        print(json.dumps(df.iloc[0].dropna().to_dict(), default=str, indent=2))
        
        print("\n--- CRITICAL KEY CHECK ---")
        # Check specific suspect keys
        suspects = ['challengeLost', 'dribbledPast', 'errorLeadToShot', 'errorLeadToGoal', 'dispossessed', 'possessionLost', 'totalTackle', 'interceptionWon']
        for key in suspects:
            if key in df.columns:
                print(f"[FOUND] {key}")
            else:
                print(f"[MISSING] {key}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_direct_api_keys()
