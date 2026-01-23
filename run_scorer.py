"""
UCL Point Scorer - Main Runner
Usage:
    python run_scorer.py <sofascore_url> [whoscored_url]

Example:
    python run_scorer.py https://www.sofascore.com/match/12345
    python run_scorer.py https://www.sofascore.com/match/12345 https://www.whoscored.com/Matches/98765/Live
"""
import sys
import pandas as pd
from player_score_calculator import calc_all_players

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    sofascore_url = sys.argv[1]
    whoscored_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"\n⚽️ Calculating scores for: {sofascore_url}")
    if whoscored_url:
        print(f"🔗 Using WhoScored for positions: {whoscored_url}")
    else:
        print("⚠️ No WhoScored URL provided. Using SofaScore/Fallback positions.")
        
    try:
        df = calc_all_players(sofascore_url, whoscored_url)
        
        if df.empty:
            print("❌ No data found.")
            return
            
        # Display results
        # Sort by Score descending
        df_sorted = df.sort_values('score', ascending=False)
        
        print("\n" + "="*60)
        print(f"{'PLAYER':<30} {'POS':<5} {'PTS':>5} {'TEAM'}")
        print("="*60)
        
        for _, row in df_sorted.iterrows():
            # Get Team (Home/Away) - infer from somewhere or just print
            # player_score_calculator doesn't return Team column explicitly in final df?
            # It merges scores back to final_df_with_plus_minus which HAS 'Team' likely?
            # Let's check columns.
            # sofascore_adapter returns 'Team' ('Home'/'Away').
            # process_match_events preserves it? No, process_match_events takes df_home/df_away.
            # final_df in process_match_events merges stats.
            # But we can infer team from row data if available.
            
            # Simplified output
            print(f"{row['name']:<30} {row['pos']:<5} {row['score']:>5}")
            
        print("="*60)
        
        # Save to CSV
        filename = "match_scores.csv"
        df_sorted.to_csv(filename, index=False)
        print(f"\n✅ Results saved to {filename}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
