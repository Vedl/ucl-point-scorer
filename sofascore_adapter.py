from curl_cffi import requests
import pandas as pd
import re
import math
import os
from whoscored_adapter import get_whoscored_positions

WHOSCORED_POS_MAP = None
EXCEL_POS_MAP = None

def load_excel_positions():
    """Legacy: Load positions from Excel file (fallback only)."""
    global EXCEL_POS_MAP
    if EXCEL_POS_MAP is not None:
        return EXCEL_POS_MAP
        
    file_path = "Gameweek 4 UCL 25:26 Points.xlsx"
    if not os.path.exists(file_path):
        EXCEL_POS_MAP = {}
        return EXCEL_POS_MAP
        
    try:
        df = pd.read_excel(file_path)
        mapping = {}
        for index, row in df.iterrows():
            p_name = str(row['name']).strip()
            p_pos = str(row['pos']).strip()
            mapping[p_name.lower()] = p_pos
            
        EXCEL_POS_MAP = mapping
        print(f"Loaded {len(mapping)} positions from Excel.")
    except Exception as e:
        print(f"Failed to load Excel positions: {e}")
        EXCEL_POS_MAP = {}
        
    return EXCEL_POS_MAP


def load_whoscored_positions(whoscored_url: str = None):
    """Load positions from WhoScored for accurate Wing-Back classification."""
    global WHOSCORED_POS_MAP
    
    # Return cached if already loaded
    if WHOSCORED_POS_MAP is not None:
        return WHOSCORED_POS_MAP
    
    if whoscored_url:
        WHOSCORED_POS_MAP = get_whoscored_positions(whoscored_url)
    else:
        WHOSCORED_POS_MAP = {}
        
    return WHOSCORED_POS_MAP


def reset_position_cache():
    """Reset position caches (call when switching matches)."""
    global WHOSCORED_POS_MAP, EXCEL_POS_MAP
    WHOSCORED_POS_MAP = None
    EXCEL_POS_MAP = None

def get_match_id(url):
    # Extract ID from url like https://www.sofascore.com/team-a-vs-team-b/slug#id:12345
    # or just https://www.sofascore.com/.../12345
    # Try regex for #id:(\d+)
    match = re.search(r'#id:(\d+)', url)
    if match:
        return match.group(1)
    
    # Try just finding digits at the end if no #id:
    # .../12173509
    match = re.search(r'/(\d+)$', url)
    if match:
        return match.group(1)
        
    raise ValueError("Could not parse match ID from URL")

def fetch_sofascore_data(match_id, endpoint="lineups"):
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/{endpoint}"
    # Impersonate chrome to bypass 403
    try:
        response = requests.get(url, impersonate="chrome120")
        if response.status_code != 200:
            if response.status_code == 404:
                return {}
            # If 403, might need retry or newer chrome version
            raise ValueError(f"Failed to fetch SofaScore data ({endpoint}): {response.status_code}")
        return response.json()
    except Exception as e:
        raise ValueError(f"Request failed: {e}")

def get_match_metadata(match_id):
    """Fetch basic match info (teams, time)"""
    url = f"https://api.sofascore.com/api/v1/event/{match_id}"
    try:
        response = requests.get(url, impersonate="chrome120")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def get_match_events_sofascore(match_id):
    data = fetch_sofascore_data(match_id, "incidents")
    incidents = data.get('incidents', [])
    
    # Sort by time (usually reverse sorted in API?)
    # We want chronological.
    incidents.sort(key=lambda x: x.get('time', 0))
    
    events = []
    
    for inc in incidents:
        # incidentType: 'goal', 'card', 'substitution', 'period'
        itype = inc.get('incidentType')
        time = str(inc.get('time', 0)) 
        if inc.get('addedTime'):
            time += f"+{inc['addedTime']}"
            
        event = {
            'time': time,
            'event_kind': 'Unknown',
            'player': None,
            'player_on': None,
            'player_off': None
        }
        
        if itype == 'goal':
            event['event_kind'] = 'Goal'
            event['player'] = inc.get('player', {}).get('name')
            # Handle Own Goal or Penalty? 
            if inc.get('isHome'):
                # We need to know who scored relative to teams. 
                # Existing logic infers team from player name match.
                pass
                
        elif itype == 'card':
            # Yellow or Red
            if inc.get('incidentClass') == 'yellow':
                event['event_kind'] = 'Yellow Card'
            elif inc.get('incidentClass') == 'red':
                event['event_kind'] = 'Red Card'
            event['player'] = inc.get('player', {}).get('name')
            
        elif itype == 'substitution':
            event['event_kind'] = 'Substitution'
            event['player_on'] = inc.get('playerIn', {}).get('name')
            event['player_off'] = inc.get('playerOut', {}).get('name')
            
        else:
            continue
            
        events.append(event)
        
    return events

def map_player_stats(player_data):
    stats = player_data.get('statistics', {})
    
    # Safely get values, default to 0
    def get(key):
        return stats.get(key, 0)
        
    mapped = {}
    
    # --- MAPPING LOGIC ---
    
    # Basic Info
    mapped['Unnamed: 0_level_0_Player'] = player_data['player']['name']
    mapped['Unnamed: 5_level_0_Min'] = get('minutesPlayed')
    
    # Position (SofaScore gives 'F', 'M', 'D', 'G')
    # Priority: 1. WhoScored (DMR/DML -> DEF), 2. Excel Override, 3. SofaScore
    whoscored_map = load_whoscored_positions()
    excel_map = load_excel_positions()
    player_name = player_data['player']['name']
    
    whoscored_pos = whoscored_map.get(player_name.lower())
    excel_pos = excel_map.get(player_name.lower())
    
    pos_map = {'F': 'FWD', 'M': 'MID', 'D': 'DEF', 'G': 'GK'}
    
    if whoscored_pos:
        # WhoScored provides accurate position (DEF for Wing-Backs)
        mapped['Pos'] = whoscored_pos
    elif excel_pos:
        # Excel fallback
        if excel_pos in ['FWD', 'MID', 'DEF', 'GK']:
             mapped['Pos'] = excel_pos
        else:
             mapped['Pos'] = pos_map.get(excel_pos, 'MID')
    else:
        # Fallback to SofaScore General -> Match
        general_pos = player_data.get('player', {}).get('position')
        match_pos = player_data.get('position', 'M')
        
        if general_pos in pos_map:
            raw_pos = general_pos
        else:
            raw_pos = match_pos
            
        mapped['Pos'] = pos_map.get(raw_pos, 'MID')
    
    # Attacking
    mapped['Performance_Gls'] = get('goals')
    mapped['Performance_Ast'] = get('goalAssist')
    mapped['Performance_Sh'] = get('totalScoringAttempt') # Total shots
    mapped['Performance_SoT'] = get('onTargetScoringAttempt')
    
    # Passing
    mapped['Passes_Cmp'] = get('accuratePass')
    mapped['Passes_Att'] = get('totalPass')
    mapped['Unnamed: 23_level_0_KP'] = get('keyPass')
    mapped['Performance_Crs'] = get('totalCross') # or accurateCross? Formula usually accounts for volume? FBref 'Crs' is usually attempted or completed? 
    # FBref "Crs" in standard tables is usually Crosses Attempted? Or completed? 
    # Usually "Crs" columns in FBref are "Crosses". 
    # Scoring uses: 1.2 * Crs. Likely attempted or successful? 
    # Let's use totalCross for now (volume).
    
    # Dribbling / Possession
    mapped['Take-Ons_Succ'] = get('wonContest') # "Dribbles won" often called wonContest
    mapped['Take-Ons_Att'] = get('totalContest') # "Dribbles attempted"
    mapped['Carries_Dis'] = get('dispossessed')
    mapped['Performance_Fls'] = get('fouls')
    mapped['Performance_Off'] = get('offsides') # Verify key, maybe totalOffside
    
    # Defensive
    mapped['Performance_Tkl'] = get('totalTackle')
    mapped['Performance_Int'] = get('interceptionWon')
    mapped['Unnamed: 20_level_0_Clr'] = get('totalClearance')
    mapped['Blocks_Sh'] = get('blockedScoringAttempt')
    mapped['Challenges_Lost'] = get('challengeLost') # Dribbled Past
    mapped['Unnamed: 21_level_0_Err'] = get('errorLeadToGoal') # Best proxy for Err
    mapped['Performance_OG'] = get('ownGoals')
    mapped['Performance_Rec'] = get('ballRecovery')
    
    # Aerial
    mapped['Aerial Duels_Won'] = get('aerialWon') 
    mapped['Aerial Duels_Lost'] = get('aerialLost')
    
    # Penalties
    mapped['Performance_PKwon'] = get('penaltyWon')
    mapped['Performance_PKcon'] = get('penaltyConceded')
    mapped['Performance_PK'] = get('goalsFromPenalty') # Penalties Scored
    # Performance_PKatt (Attempted) = Scored + Missed
    mapped['Performance_PKatt'] = get('goalsFromPenalty') + get('penaltyMissed') 
    
    # Discipline
    mapped['Performance_CrdY'] = get('yellowCards') if 'yellowCards' in stats else (1 if get('yellowCard') else 0)
    mapped['Performance_CrdR'] = get('redCards') if 'redCards' in stats else (1 if get('redCard') else 0)
    
    # Goalkeeping
    mapped['Performance_Saves'] = get('saves')
    mapped['Performance_Punches'] = get('punches')
    mapped['Performance_HighClaims'] = get('goodHighClaim')
    mapped['Performance_RunsOut'] = get('totalKeeperSweeper') # or runsOut?
    mapped['Performance_PKSaved'] = get('penaltySave')
    mapped['Performance_GK_GoalsConceded'] = get('goalsConceded')
    
    # Misc
    mapped['Hit_Woodwork'] = get('hitWoodwork')
    
    # Metadata
    mapped['is_sub'] = player_data.get('substitute', False)

    # Return as a Series-compatible dict
    return mapped

def get_player_stats_df(match_url, whoscored_url: str = None):
    """Fetch player stats from SofaScore with optional WhoScored position override.
    
    Args:
        match_url: SofaScore match URL
        whoscored_url: Optional WhoScored match URL for accurate position classification
                       (e.g., Wing-Backs as Defenders)
    """
    # Reset caches for new match
    reset_position_cache()
    
    # Pre-load WhoScored positions if URL provided
    if whoscored_url:
        load_whoscored_positions(whoscored_url)
    
    match_id = get_match_id(match_url)
    data = fetch_sofascore_data(match_id, "lineups")
    
    players = []
    
    # Process Home
    for p in data['home']['players']:
        row = map_player_stats(p)
        row['Team'] = 'Home' # Internal flag if needed
        players.append(row)
        
    # Process Away
    for p in data['away']['players']:
        row = map_player_stats(p)
        row['Team'] = 'Away'
        players.append(row)
        
    df = pd.DataFrame(players)
    
    # Fetch events for accurate +/- calculation
    events = get_match_events_sofascore(match_id)
    
    return df, events
