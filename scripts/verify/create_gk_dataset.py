
import json
import pandas as pd
from curl_cffi import requests
import time
import os

# Load matches
with open("ucl_matches.json", "r") as f:
    matches = json.load(f)

print(f"Processing {len(matches)} matches...")

# v11 Coefficients
COEFFS = {
    'Base': 21.94, 'Saves': 1.55, 'Claims': 8.16, 'Sweeper': 4.52,
    'Rec': -0.54, 'Clear': 1.47, 'AccPass': 0.15, 'FailPass': 2.00,
    'Punch': -6.70, 'SIB': -2.56, 'Poss': -1.94, 'PKFaced': 5.00,
    'PKSaved': 0.00, 'GP': 9.70, 'KSV': -4.42, 'Minutes': 3
}

results = []

for idx, m in enumerate(matches):
    match_id = m['id']
    slug = m['slug']
    round_name = f"Round {m['round']}"
    
    print(f"[{idx+1}/{len(matches)}] {slug} ({match_id})...")
    
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    try:
        res = requests.get(url, impersonate='chrome120')
        if res.status_code != 200:
            print(f"  Skipping {match_id}: Status {res.status_code}")
            continue
            
        data = res.json()
        
        # Process both teams
        for team_key in ['home', 'away']:
            team_name = m[team_key]
            
            for p in data[team_key]['players']:
                # Find GKs (Position 'G' or substitute GK if played)
                pos = p.get('position', '')
                sub = p.get('substitute', False)
                mins = p.get('statistics', {}).get('minutesPlayed', 0)
                
                # Logic: Must be GK position OR have GK stats? 
                # Usually position='G'. And must have played > 0 mins.
                if pos == 'G' and mins > 0:
                    name = p['player']['name']
                    stats = p.get('statistics', {})
                    
                    # Extract Features
                    saves = stats.get('saves', 0)
                    claims = stats.get('goodHighClaim', 0)
                    sweep = stats.get('totalKeeperSweeper', 0)
                    rec = stats.get('ballRecovery', 0)
                    clears = stats.get('totalClearance', 0)
                    acc_pass = stats.get('accuratePass', 0)
                    total_pass = stats.get('totalPass', 0)
                    fail_pass = total_pass - acc_pass
                    og = stats.get('ownGoals', 0)
                    pt_og = -10.27 * og # Old rule? Or implicit? v11 didn't optimize OG explicitly (coeff ~0?)
                    # Wait, v11 used 'Own Goals' as feature but coeff likely close to 0 or ignored if not in list?
                    # In optimize_gk_v11.py, I included 'og' in bounds but didn't print it if coeff < 0.001.
                    # Let's assume standard OG penalty for now (-1 per scoring rules? No, -5 or -10?)
                    # Actually Rulli (OG) was matched with 17 pts.
                    # If my formula v11 doesn't have OG coeff shown, it means it's effectively 0 in linear model 
                    # OR covered by other negative stats (goals conceded/prevented).
                    # Goals Prevented accounts for OG heavily (GP drops).
                    # So explicit OG penalty might double count?
                    # Let's stick strictly to v11 features + standard cards.
                    
                    punch = stats.get('punches', 0)
                    sib = stats.get('savedShotsFromInsideTheBox', 0)
                    poss = stats.get('possessionLostCtrl', 0)
                    pk_save = stats.get('penaltySave', 0)
                    pk_faced = stats.get('penaltyFaced', 0)
                    gp = stats.get('goalsPrevented', 0)
                    ksv = stats.get('keeperSaveValue', 0)
                    
                    # Discipline
                    yc = 1 if stats.get('yellowCards') else 0
                    rc = 1 if stats.get('redCards') else 0
                    disc_score = (-3 * yc) + (-5 * rc)
                    
                    # Calculate Score
                    score = (COEFFS['Base'] + COEFFS['Minutes'] + 
                             COEFFS['Saves']*saves + COEFFS['Claims']*claims + COEFFS['Sweeper']*sweep + 
                             COEFFS['Rec']*rec + COEFFS['Clear']*clears + 
                             COEFFS['AccPass']*acc_pass + COEFFS['FailPass']*fail_pass + 
                             COEFFS['Punch']*punch + COEFFS['SIB']*sib + COEFFS['Poss']*poss + 
                             COEFFS['PKFaced']*pk_faced + COEFFS['PKSaved']*pk_save + 
                             COEFFS['GP']*gp + COEFFS['KSV']*ksv + 
                             disc_score - (5 * stats.get('penaltyConceded', 0))) # PK Conceded
                    
                    score = round(score)
                    
                    results.append({
                        'Match_ID': match_id,
                        'Round': round_name,
                        'Match': slug,
                        'Team': team_name,
                        'Player': name,
                        'Calculated_Score': score,
                        'Saves': saves,
                        'Claims': claims,
                        'Sweeper': sweep,
                        'Goals_Prevented': gp,
                        'Minutes': mins
                    })
                    
        time.sleep(0.1) # Be nice to API
        
    except Exception as e:
        print(f"  Error processing {match_id}: {e}")

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("ucl_gk_dataset_v11.csv", index=False)
print(f"Saved {len(df)} GK performances to ucl_gk_dataset_v11.csv")
