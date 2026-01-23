import sofascore_adapter
import whoscored_search
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

def reproduce():
    # User's URL (Chelsea vs Pafos)
    url = "https://www.sofascore.com/football/match/pafos-fc-chelsea/NsBHtb#id:14566583"
    print(f"Testing with URL: {url}")
    
    # 1. Get Metadata
    try:
        match_id = sofascore_adapter.get_match_id(url)
        print(f"Match ID: {match_id}")
        
        meta = sofascore_adapter.get_match_metadata(match_id)
        if not meta:
            print("Failed to get metadata")
            return
            
        home_team = meta['event']['homeTeam']['name']
        away_team = meta['event']['awayTeam']['name']
        
        print(f"Home Team (SofaScore): '{home_team}'")
        print(f"Away Team (SofaScore): '{away_team}'")
        
        # 2. Run Search
        print("\n--- Running Search ---")
        url = whoscored_search.find_match_url(home_team, away_team)
        
        if url:
            print(f"\nSUCCESS! Found URL: {url}")
        else:
            print(f"\nFAILURE. Match URL not found.")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    reproduce()
