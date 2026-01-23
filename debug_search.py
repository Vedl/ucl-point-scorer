from googlesearch import search

def test_search(home, away):
    # Simplify names
    home_simple = home.replace("FC", "").replace("Royale", "").strip()
    away_simple = away.replace("FC", "").replace("Royale", "").strip()
    
    # Special case for Union SG which is often just "Union SG"
    if "Union Saint-Gilloise" in away_simple:
        away_simple = "Union SG"
    
    queries = [
        f"whoscored {home_simple} vs {away_simple} champions league",
        f"whoscored {home_simple} {away_simple}",
        f"whoscored Bayern vs Union SG" # Hardcoded checks
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        try:
            results = search(q, num_results=5, advanced=True)
            for r in results:
                print(f" - {r.title}: {r.url}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_search("FC Bayern München", "Royale Union Saint-Gilloise")
