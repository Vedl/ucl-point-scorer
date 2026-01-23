"""
WhoScored Adapter - Fetches granular player positions from WhoScored pages.

Position Mapping (Updated to match Excel classification):
- GK -> GK
- DR, DC, DL, DMR, DML -> DEF (Wing-Backs classified as Defenders)
- MC, DMC, AMC -> MID (Central midfielders only)
- MR, ML, AMR, AML -> FWD (Wingers classified as Forwards)
- FW, FWR, FWL -> FWD
"""

from curl_cffi import requests
import re
import json

# Position code to internal position mapping
# Updated: Wingers (AMR, AML, MR, ML) now map to FWD to match Excel classification
POSITION_MAP = {
    # Goalkeeper
    'GK': 'GK',
    
    # Defenders (including Wing-Backs)
    'DR': 'DEF',
    'DC': 'DEF', 
    'DL': 'DEF',
    'DMR': 'DEF',  # Wing-Back Right -> Defender
    'DML': 'DEF',  # Wing-Back Left -> Defender
    
    # Midfielders (Central + Wide)
    'MC': 'MID',   # Central Midfielder
    'DMC': 'MID',  # Defensive Midfielder
    'AMC': 'MID',  # Attacking Midfielder (Central)
    'MR': 'MID',   # Right Midfielder -> Midfielder
    'ML': 'MID',   # Left Midfielder -> Midfielder
    
    # Forwards (Attacking wingers + Strikers)
    'AMR': 'FWD',  # Attacking Right Winger -> Forward
    'AML': 'FWD',  # Attacking Left Winger -> Forward
    'FW': 'FWD',   # Striker
    'FWR': 'FWD',  # Right Forward
    'FWL': 'FWD',  # Left Forward
    'Sub': 'MID',  # Default for substitutes
}



def extract_match_id_from_url(url: str) -> str:
    """Extract match ID from WhoScored URL.
    
    Examples:
    - https://www.whoscored.com/matches/1946404/live/... -> 1946404
    """
    match = re.search(r'/matches/(\d+)/', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract match ID from URL: {url}")


def fetch_whoscored_html(url: str) -> str:
    """Fetch WhoScored page HTML using curl_cffi to bypass Cloudflare."""
    try:
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.whoscored.com/',
            }
        )
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch WhoScored page: HTTP {response.status_code}")
        return response.text
    except Exception as e:
        raise ValueError(f"WhoScored request failed: {e}")


def parse_match_centre_data(html: str) -> dict:
    """Extract player positions from embedded JSON in WhoScored HTML.
    
    The HTML contains JSON objects like:
    {"playerId":320436,"shirtNo":26,"name":"Julian Ryerson","position":"DMR",...}
    """
    positions = {}
    
    # Pattern to match player objects with name and position
    # Example: "name":"Julian Ryerson","position":"DMR"
    pattern = r'"name"\s*:\s*"([^"]+)"\s*,\s*"position"\s*:\s*"([A-Z]+)"'
    
    for match in re.finditer(pattern, html):
        player_name = match.group(1).strip()
        position_code = match.group(2).strip()
        
        # Map to our internal position format
        internal_pos = POSITION_MAP.get(position_code, 'MID')
        positions[player_name.lower()] = internal_pos
    
    return positions


def parse_positions_from_table(html: str) -> dict:
    """Fallback: parse player positions from the statistics table HTML."""
    return parse_match_centre_data(html)  # Use same logic



def get_whoscored_positions(url: str) -> dict:
    """Main function to get player positions from a WhoScored match URL.
    
    Args:
        url: WhoScored match URL (e.g., https://www.whoscored.com/matches/1946404/live/...)
    
    Returns:
        Dict mapping player names (lowercase) to positions (GK/DEF/MID/FWD)
    """
    try:
        print(f"Fetching WhoScored positions from: {url}")
        html = fetch_whoscored_html(url)
        
        positions = {}
        
        # Try parsing the embedded JSON first
        data = parse_match_centre_data(html)
        
        if isinstance(data, dict):
            # Process home and away players
            for team_key in ['home', 'away']:
                team_data = data.get(team_key, {})
                players = team_data.get('players', [])
                
                for player in players:
                    name = player.get('name', '')
                    pos_code = player.get('position', 'Sub')
                    
                    internal_pos = POSITION_MAP.get(pos_code, 'MID')
                    positions[name.lower()] = internal_pos
        else:
            # Fallback to table parsing (already a dict of positions)
            positions = data if isinstance(data, dict) else {}
        
        if not positions:
            # Last resort: parse from raw HTML patterns
            positions = parse_positions_from_table(html)
        
        print(f"Loaded {len(positions)} positions from WhoScored.")
        return positions
        
    except Exception as e:
        print(f"Failed to get WhoScored positions: {e}")
        return {}


# Test function
if __name__ == "__main__":
    test_url = "https://www.whoscored.com/matches/1946404/live/europe-champions-league-2025-2026-manchester-city-borussia-dortmund"
    positions = get_whoscored_positions(test_url)
    
    print("\n--- Position Results ---")
    # Check for our target players
    targets = ['julian ryerson', 'daniel svensson', 'foden', 'haaland']
    for target in targets:
        pos = positions.get(target, 'NOT FOUND')
        print(f"{target}: {pos}")
