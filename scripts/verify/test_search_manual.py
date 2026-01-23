from whoscored_search import find_match_url

# Use a known match from GW5 or recent
# Real Madrid vs Liverpool (Nov 27)
print("Testing Search...")
url = find_match_url("Liverpool", "Real Madrid")
print(f"Result: {url}")

url2 = find_match_url("Bayer Leverkusen", "Salzburg")
print(f"Result: {url2}")
