
import json
import pandas as pd
from curl_cffi import requests
import time
import os

# Define Targets (Gw -> Team -> Score)
# Use flexible team name matching
TARGETS = {
    1: {
        'Juventus': 7, 'Dortmund': 16, 'Bayern': 33, 'Arsenal': 37, 'Liverpool': 26, 'Spurs': 36,
        'Atletico': 18, 'City': 31, 'Napoli': 49, 'Barcelona': 55, 'Real Madrid': 34, 'Inter': 39,
        'PSG': 35, 'Marseille': 62
    },
    2: {
        'Arsenal': 41, 'City': 19, 'Juventus': 27, 'Dortmund': 27, 'Bayern': 27, 'PSG': 25,
        'Inter': 37, 'Barcelona': 33, 'Real Madrid': 34, 'Napoli': 32, 'Atletico': 25, 'Spurs': 24,
        'Marseille': 39, 'Liverpool': 32
    },
    3: {
        'City': 38, 'Arsenal': 37, 'Real Madrid': 44, 'Napoli': 5, 'Dortmund': 27, 'Juventus': 47,
        'Atletico': 16, 'PSG': 19, 'Bayern': 40, 'Barcelona': 27, 'Spurs': 60, 'Liverpool': 20,
        'Inter': 45, 'Marseille': 38
    },
    4: {
        'City': 42, 'Arsenal': 33, 'Juventus': 21, 'Barcelona': 20, 'PSG': 25, 'Newcastle': 55,
        'Atletico': 38, 'Napoli': 42, 'Real Madrid': 51, 'Spurs': 47, 'Bayern': 51, 'Inter': 29,
        'Liverpool': 31, 'Marseille': 34
    },
    5: {
        'Juventus': 29, 'Marseille': 52, 'Bayern': 17, 'Newcastle': 30, 'Arsenal': 26, 'Inter': 31,
        'Barcelona': 21, 'PSG': 14, 'Atletico': 37, 'Real Madrid': 28, 'Spurs': 9, 'Liverpool': 10,
        'City': 13, 'Napoli': 42
    },
    6: {
        'Atletico': 22, 'City': 18, 'Spurs': 49, 'Marseille': 40, 'Newcastle': 37, 'Napoli': 38,
        'Liverpool': 42, 'Juventus': 50, 'Bayern': 26, 'PSG': 36, 'Arsenal': 51, 'Barcelona': 31,
        'Inter': 41, 'Real Madrid': 36
    }
}

# Alias mapping for team names in SofaScore vs User Input
TEAM_ALIASES = {
    'Juventus': ['Juventus'],
    'Dortmund': ['Borussia Dortmund'],
    'Bayern': ['FC Bayern München'],
    'Arsenal': ['Arsenal'],
    'Liverpool': ['Liverpool'],
    'Spurs': ['Tottenham Hotspur'],
    'Atletico': ['Atlético Madrid'],
    'City': ['Manchester City'],
    'Napoli': ['Napoli'],
    'Barcelona': ['Barcelona'],
    'Real Madrid': ['Real Madrid'],
    'Inter': ['Inter'],
    'PSG': ['Paris Saint-Germain'],
    'Marseille': ['Olympique de Marseille'],
    'Newcastle': ['Newcastle United']
}

def get_target_score(round_num, team_name):
    # Find user key for this team name
    user_key = None
    for k, aliases in TEAM_ALIASES.items():
        if team_name in aliases:
            user_key = k
            break
            
    if user_key and round_num in TARGETS:
        return TARGETS[round_num].get(user_key) # Returns None if not found
    return None

# Load matches
with open("ucl_matches.json", "r") as f:
    matches = json.load(f)

print(f"Processing {len(matches)} matches to map targets...")

live_optimization_data = []

for idx, m in enumerate(matches):
    match_id = m['id']
    slug = m['slug']
    round_num = m['round']
    
    # Skip if round not in 1-6 (User requests for 1-6, plus we have 7 implicit)
    # Actually fetch EVERYTHING to build the full dataset, but mark targets where known.
    
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    try:
        res = requests.get(url, impersonate='chrome120')
        if res.status_code != 200: continue
        data = res.json()
        
        for team_key in ['home', 'away']:
            team_name = m[team_key]
            target = get_target_score(round_num, team_name)
            
            for p in data[team_key]['players']:
                possible_positions = ['G']
                pos = p.get('position', '')
                mins = p.get('statistics', {}).get('minutesPlayed', 0)
                
                # Loose filter: GK pos or handled ball? No, stick to GK.
                if pos == 'G' and mins > 0:
                    name = p['player']['name']
                    stats = p.get('statistics', {})
                    
                    # Extract Features for Optimization
                    # (saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch, sv_inside, poss_lost, pk_save, pk_faced, gp, ksv)
                    
                    saves = stats.get('saves', 0)
                    claims = stats.get('goodHighClaim', 0)
                    sweep = stats.get('totalKeeperSweeper', 0)
                    rec = stats.get('ballRecovery', 0)
                    clears = stats.get('totalClearance', 0)
                    acc_pass = stats.get('accuratePass', 0)
                    total_pass = stats.get('totalPass', 0)
                    fail_pass = total_pass - acc_pass
                    og = stats.get('ownGoals', 0)
                    punch = stats.get('punches', 0)
                    sib = stats.get('savedShotsFromInsideTheBox', 0)
                    poss = stats.get('possessionLostCtrl', 0)
                    pk_save = stats.get('penaltySave', 0)
                    pk_faced = stats.get('penaltyFaced', 0)
                    gp = stats.get('goalsPrevented', 0)
                    ksv = stats.get('keeperSaveValue', 0)
                    
                    # Discipline penalty to SUBTRACT from target before optimization?
                    # The formula usually has discipline outside the optimization loop or optimized?
                    # Standard: YC=-3, RC=-5.
                    yc = 1 if stats.get('yellowCards') else 0
                    rc = 1 if stats.get('redCards') else 0
                    disc_deduction = (-3 * yc) + (-5 * rc) - (5 * stats.get('penaltyConceded', 0))
                    
                    if target is not None:
                        # Adjusted target = Target - Discipline_Penalty? 
                        # No, calculated score INCLUDES discipline. 
                        # So Optimzation Target = Target_User.
                        # The optimization function needs to account for discipline or we subtract it here.
                        # Let's subtract discipline from target so we optimize only the performance metrics.
                        # e.g. Target 10, YC (-3). Performance points should sum to 13.
                        # So adj_target = Target - disc_deduction. (10 - (-3) = 13).
                        adj_target = target - disc_deduction
                        
                        row = (f"{name} ({team_name} R{round_num})", adj_target, 
                               saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, 
                               punch, sib, poss, pk_save, pk_faced, gp, ksv)
                        live_optimization_data.append(row)
                        print(f"Added {name} (R{round_num} {team_name}): Target {target} -> Adj {adj_target}")
        
        time.sleep(0.05)
        
    except Exception as e:
        print(f"Error {match_id}: {e}")

# Save collected data for optimization script
import pickle
with open("gk_optimization_data.pkl", "wb") as f:
    pickle.dump(live_optimization_data, f)

print(f"Collected {len(live_optimization_data)} data points for optimization.")
