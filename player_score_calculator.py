import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

def parse_minute(time_str):
    if '+' in time_str:
        base, extra = time_str.split('+')
        return int(base) + int(extra)
    return int(time_str)

def def_score_calc (df, team_score,team_conc):
    score =( 1.9*df['Aerial Duels_Won'] - 1.5*df[ 'Aerial Duels_Lost']+ 2.7*df['Performance_Tkl']
            -1.6*df['Challenges_Lost']+2.7*df['Performance_Int']+1.1*df['Unnamed: 20_level_0_Clr']
            +(10-(5*team_conc))+(3-(1.2*df['Carries_Dis'])-(0.6*(df['Performance_Fls']+df['Performance_Off']))
                               -(3.5*df['Performance_OG'])-(5*df[ 'Unnamed: 21_level_0_Err']))+
            df['Passes_Cmp']/9 - (( df['Passes_Att']-df['Passes_Cmp'])/4.5)+df['Unnamed: 23_level_0_KP']
            +df['Take-Ons_Succ']*2.5 -((df['Take-Ons_Att']-df['Take-Ons_Succ'])*0.8)+
            1.1*df[ 'Blocks_Sh']+1.5*df['Unnamed: 23_level_0_KP']+1.2*df['Performance_Crs']+
            2.5*df['Performance_SoT']+((df['Performance_Sh']-df['Performance_SoT'])/2)+
            df['Unnamed: 5_level_0_Min']/30 + 10*df['Performance_Gls']+8*df['Performance_Ast']+
            (-5*df['Performance_CrdR'])+(-5*df['Performance_PKcon']) +(-5*(df['Performance_PKatt']-df[ 'Performance_PK'])) + (3*df.get('Hit_Woodwork', 0)))
    
    pk_won = df['Performance_PKwon'].values[0]
    pk_scored = df['Performance_PK'].values[0]
    
    if (pk_won == 1) and (pk_scored != 1):
        score += 6.4
    
    
    minutes_played = df['Unnamed: 5_level_0_Min'].values[0]

    if (minutes_played <= 45) and (team_conc == 0):
            score -= 5
    
    return round(score,0)

def mid_score_calc (df, team_score,team_conc):
    score =( 1.7*df['Aerial Duels_Won'] - 1.5*df[ 'Aerial Duels_Lost']+ 2.6*df['Performance_Tkl']
            -1.2*df['Challenges_Lost']+2.5*df['Performance_Int']+1.1*df['Unnamed: 20_level_0_Clr']
            +(4-(2*team_conc)+(2*team_score))+(3-(1.1*df['Carries_Dis'])-(0.6*(df['Performance_Fls']+df['Performance_Off']))
                               -(3.3*df['Performance_OG'])-(5*df[ 'Unnamed: 21_level_0_Err']))+
            df['Passes_Cmp']/6.6- (( df['Passes_Att']-df['Passes_Cmp'])/3.2)+df['Unnamed: 23_level_0_KP']
            +df['Take-Ons_Succ']*2.9 -((df['Take-Ons_Att']-df['Take-Ons_Succ'])*0.8)+
            1.1*df[ 'Blocks_Sh']+1.5*df['Unnamed: 23_level_0_KP']+1.2*df['Performance_Crs']+
            2.2*df['Performance_SoT']+((df['Performance_Sh']-df['Performance_SoT'])/4)+
            df['Unnamed: 5_level_0_Min']/30 + 10*df['Performance_Gls']+8*df['Performance_Ast']+
            (-5*df['Performance_CrdR'])+(-5*df['Performance_PKcon']) +(-5*(df['Performance_PKatt']-df[ 'Performance_PK'])) + (3*df.get('Hit_Woodwork', 0)))
    
    pk_won = df['Performance_PKwon'].values[0]
    pk_scored = df['Performance_PK'].values[0]
    
    if (pk_won == 1) and (pk_scored != 1):
        score += 6.4
            
    return round(score,0)

def fwd_score_calc (df, team_score,team_conc):
    score =( 1.4*df['Aerial Duels_Won'] - 0.4*df[ 'Aerial Duels_Lost']+ 2.6*df['Performance_Tkl']
            -1*df['Challenges_Lost']+2.7*df['Performance_Int']+0.8*df['Unnamed: 20_level_0_Clr']
            +((3*team_score))+(5-(0.9*df['Carries_Dis'])-(0.5*(df['Performance_Fls']+df['Performance_Off']))
                               -(3.0*df['Performance_OG'])-(5*df[ 'Unnamed: 21_level_0_Err']))+
            df['Passes_Cmp']/6 - (( df['Passes_Att']-df['Passes_Cmp'])/8.0)+df['Unnamed: 23_level_0_KP']
            +df['Take-Ons_Succ']*3.0 -((df['Take-Ons_Att']-df['Take-Ons_Succ'])*1.0)+
           0.8*df[ 'Blocks_Sh']+1.5*df['Unnamed: 23_level_0_KP']+1.2*df['Performance_Crs']+
            3.0*df['Performance_SoT']+((df['Performance_Sh']-df['Performance_SoT'])/3)+
            df['Unnamed: 5_level_0_Min']/30 + 10*df['Performance_Gls']+8*df['Performance_Ast']+
            (-5*df['Performance_CrdR'])+(-5*df['Performance_PKcon'])+(-5*(df['Performance_PKatt']-df[ 'Performance_PK'])) + (3*df.get('Hit_Woodwork', 0)))
    
    pk_won = df['Performance_PKwon'].values[0]
    pk_scored = df['Performance_PK'].values[0]
    
    if (pk_won == 1) and (pk_scored != 1):
        score += 6.4
    
    return round(score,0)

def gk_score_calc(df, team_score, team_conc):
    # Goalkeeper Formula (Reverse-Engineered from Official Points)
    # Optimized using scipy to match 6 data points (without rating!):
    # - Alisson (Liverpool vs Marseille): 45 pts
    # - Rulli (Marseille vs Liverpool): 17 pts
    # - Chevalier (PSG vs Sporting): 23 pts
    # - Neuer (Bayern vs Union SG): 35 pts
    # - Sommer (Inter vs Arsenal): 19 pts
    # - Raya (Arsenal vs Inter): 34 pts
    
    # Coefficients (optimized v7 - NO rating dependency):
    # - Base (Clean Sheet): +18.02
    # - Saves: +2.67
    # - High Claims: +14.23 (extremely valuable!)
    # - Sweeper/Runs Out: +5.25
    # - Clearances: +1.34
    # - Recoveries: -0.69 (slightly penalized)
    # - Accurate Passes: +0.055 (slight reward)
    # - Failed Passes: -1.01 (heavily penalized!)
    # - Own Goals: -10.27
    # - Punches: +0.50
    # - Minutes Bonus: +3 (90/30)
    
    # Goals Conceded: -5 per goal
    conceded_penalty = 5 * df['Performance_GK_GoalsConceded']
    
    # Calculate failed passes
    failed_passes = df['Passes_Att'] - df['Passes_Cmp']
    
    score = (
        # Base (Clean Sheet bonus)
        + 18.02
        
        # GK Specific Actions
        + 2.67 * df['Performance_Saves']
        + 14.23 * df['Performance_HighClaims']  # EXTREMELY valuable!
        + 5.25 * df['Performance_RunsOut']  # Sweeper
        + 1.34 * df['Unnamed: 20_level_0_Clr']  # Clearances
        - 0.69 * df['Performance_Rec']  # Recoveries (slightly penalized)
        
        # Distribution (accuracy matters!)
        + 0.055 * df['Passes_Cmp']  # Reward accurate passes
        - 1.01 * failed_passes  # Penalize failed passes!
        
        # Goals Conceded penalty
        - conceded_penalty
        
        # Punches
        + 0.50 * df['Performance_Punches']
        
        # Big Moments
        + 7.0 * df['Performance_PKSaved']
        
        # Mistakes
        - (10.27 * df['Performance_OG'])  # Own Goals
        - (5 * df['Unnamed: 21_level_0_Err'])
        
        # Attacking (Rare)
        + 10 * df['Performance_Gls']
        + 8 * df['Performance_Ast']
        
        # Discipline
        - 5 * df['Performance_CrdR']
        - 3 * df['Performance_CrdY']
        - 5 * df['Performance_PKcon']
    )
    
    pk_won = df['Performance_PKwon'].values[0]
    pk_scored = df['Performance_PK'].values[0]
    
    if (pk_won == 1) and (pk_scored != 1):
        score += 6.4

    minutes_played = df['Unnamed: 5_level_0_Min'].values[0]
    
    # Participation score (3 pts for 90 mins)
    score += minutes_played / 30

    if (minutes_played <= 45) and (team_conc == 0):
        score -= 5  # Partial clean sheet penalty
    
    return round(score, 0)

def score_calc_wrapper(pos, df, team_score, team_conc):
    if pos == "FWD":
        return fwd_score_calc(df, team_score, team_conc)
    elif pos == "MID":
        return mid_score_calc(df, team_score, team_conc)
    elif pos == "DEF":
        return def_score_calc(df, team_score, team_conc)
    elif pos == "GK":
        return gk_score_calc(df, team_score, team_conc)
    else:
        return mid_score_calc(df, team_score, team_conc)

def process_match_events(match_events, df_home, df_away):
    """
    Processes match events and returns a DataFrame with player statistics.
    Fixed to handle 0-minute bench players correctly.
    """
    # Combine home and away players into sets for team assignments
    team_home_players = set(df_home['Unnamed: 0_level_0_Player'].str.strip())
    team_away_players = set(df_away['Unnamed: 0_level_0_Player'].str.strip())
    
    # Create lookups for substitute status
    home_subs = set(df_home[df_home['is_sub'] == True]['Unnamed: 0_level_0_Player'].str.strip())
    away_subs = set(df_away[df_away['is_sub'] == True]['Unnamed: 0_level_0_Player'].str.strip())
    all_subs = home_subs.union(away_subs)

    def get_team(player_name):
        if player_name in team_home_players:
            return 'Home'
        elif player_name in team_away_players:
            return 'Away'
        else:
            return 'Unknown'

    def parse_time(time_str):
        if '+' in time_str:
            base_minute = time_str.split('+')[0]
            return int(base_minute)
        elif ':' in time_str:
            base_minute = time_str.split(':')[0]
            return int(base_minute)
        else:
            return int(time_str)

    # Build a scoreline timeline
    scoreline_timeline = [{'minute': 0, 'home_goals': 0, 'away_goals': 0}]
    current_home_goals = 0
    current_away_goals = 0

    # Collect goal events and sort them by time
    for event in match_events:
        if event['event_kind'] == 'Goal':
            minute = parse_time(event['time'])
            scorer = event['player']
            scoring_team = get_team(scorer)

            if scoring_team == 'Home':
                current_home_goals += 1
            elif scoring_team == 'Away':
                current_away_goals += 1

            scoreline_timeline.append({
                'minute': minute,
                'home_goals': current_home_goals,
                'away_goals': current_away_goals
            })

    # Ensure the final scoreline is included
    match_end_time = 90  # Adjust if the match ended at a different time
    if scoreline_timeline[-1]['minute'] < match_end_time:
        scoreline_timeline.append({
            'minute': match_end_time,
            'home_goals': current_home_goals,
            'away_goals': current_away_goals
        })

    # Function to get scoreline just before a given minute
    def get_scoreline_before_minute(minute):
        for entry in reversed(scoreline_timeline):
            if entry['minute'] <= minute:
                return entry
        return {'home_goals': 0, 'away_goals': 0}

    # Build player intervals based on substitutions
    players = {}

    for event in match_events:
        event_kind = event['event_kind']
        minute = parse_time(event['time'])

        if event_kind == 'Substitution':
            player_on = event['player_on']
            player_off = event['player_off']

            # Player coming on
            players[player_on] = {
                'team': get_team(player_on),
                'on_time': minute,
                'off_time': match_end_time  # Until the end of the match
            }

            # Player going off
            if player_off in players:
                players[player_off]['off_time'] = minute
            else:
                players[player_off] = {
                    'team': get_team(player_off),
                    'on_time': 0,
                    'off_time': minute
                }

    # Add players who played full match OR sat on bench (need to distinguish)
    all_players = set(df_home['Unnamed: 0_level_0_Player'].tolist() + df_away['Unnamed: 0_level_0_Player'].tolist())
    
    for player in all_players:
        if player not in players:
            # FIX: Check if they are a substitute
            if player in all_subs:
                # Unused substitute
                players[player] = {
                    'team': get_team(player),
                    'on_time': 0,
                    'off_time': 0 # Played 0 minutes
                }
            else:
                # Starter who played full game
                players[player] = {
                    'team': get_team(player),
                    'on_time': 0,
                    'off_time': match_end_time
                }

    # Calculate goals scored and conceded for each player
    player_stats = []
    final_scoreline = scoreline_timeline[-1]

    for player, data in players.items():
        team = data['team']
        on_time = data['on_time']
        off_time = data['off_time']
        minutes_played = off_time - on_time

        goals_scored = 0
        goals_conceded = 0
        
        if minutes_played > 0:
            # Get scoreline before on_time and off_time
            scoreline_before_on = get_scoreline_before_minute(on_time)
            scoreline_before_off = get_scoreline_before_minute(off_time)

            if on_time == 0 and off_time == match_end_time:
                # Played full match
                goals_scored = final_scoreline['home_goals'] if team == 'Home' else final_scoreline['away_goals']
                goals_conceded = final_scoreline['away_goals'] if team == 'Home' else final_scoreline['home_goals']
            elif on_time == 0:
                # Subbed off
                goals_scored = scoreline_before_off['home_goals'] if team == 'Home' else scoreline_before_off['away_goals']
                goals_conceded = scoreline_before_off['away_goals'] if team == 'Home' else scoreline_before_off['home_goals']
            elif off_time == match_end_time:
                # Subbed on
                goals_scored = (final_scoreline['home_goals'] - scoreline_before_on['home_goals']) if team == 'Home' else (final_scoreline['away_goals'] - scoreline_before_on['away_goals'])
                goals_conceded = (final_scoreline['away_goals'] - scoreline_before_on['away_goals']) if team == 'Home' else (final_scoreline['home_goals'] - scoreline_before_on['home_goals'])
            else:
                # Subbed on and off
                goals_scored = (scoreline_before_off['home_goals'] - scoreline_before_on['home_goals']) if team == 'Home' else (scoreline_before_off['away_goals'] - scoreline_before_on['away_goals'])
                goals_conceded = (scoreline_before_off['away_goals'] - scoreline_before_on['away_goals']) if team == 'Home' else (scoreline_before_off['home_goals'] - scoreline_before_on['home_goals'])

        player_stats.append({
            'Unnamed: 0_level_0_Player': player,
            'minutes_played': minutes_played,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded
        })

    # Create DataFrame with player statistics
    df_match_stats = pd.DataFrame(player_stats)

    # Merge with df_home and df_away
    df_home = df_home.merge(df_match_stats, on='Unnamed: 0_level_0_Player', how='left')
    df_away = df_away.merge(df_match_stats, on='Unnamed: 0_level_0_Player', how='left')

    # Combine home and away DataFrames
    final_df = pd.concat([df_home, df_away], ignore_index=True)

    # Fill NaN values in statistics with defaults
    # Important: If a player was not in 'players' map (shouldn't happen with logic above), default to 0
    final_df['minutes_played'] = final_df['minutes_played'].fillna(0)
    final_df['goals_scored'] = final_df['goals_scored'].fillna(0)
    final_df['goals_conceded'] = final_df['goals_conceded'].fillna(0)

    return final_df


def calc_all_players(link, whoscored_url: str = None):
    """Calculate fantasy scores for all players in a match.
    
    Args:
        link: SofaScore match URL
        whoscored_url: Optional WhoScored URL for accurate position classification
                       (Wing-Backs classified as Defenders)
    """
    # Use the adapter to get data
    import sofascore_adapter
    
    try:
        merged_df, match_events = sofascore_adapter.get_player_stats_df(link, whoscored_url)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()


    # Split back to home/away for the existing logic processor, which expects separate DFs
    # The adapter returns a 'Team' column 'Home' or 'Away'
    df_home = merged_df[merged_df['Team'] == 'Home'].copy()
    df_away = merged_df[merged_df['Team'] == 'Away'].copy()
    
    # Process match events (goals, subs) to calculate +/- metrics (goals scored/conc while playing)
    # The existing process_match_events logic is reused entirely
    final_df_with_plus_minus = process_match_events(match_events, df_home, df_away)
    
    scores = []
    
    # Iterate through all players to calculate scores
    for index, row in final_df_with_plus_minus.iterrows():
        name = row['Unnamed: 0_level_0_Player']
        # Adapter maps position to "FWD", "MID", "DEF", "GK". 
        pos = row['Pos']
        
        # Get the specific rows for this player (should be 1 row)
        df = final_df_with_plus_minus[final_df_with_plus_minus['Unnamed: 0_level_0_Player'] == name]
        
        if df.empty:
            continue
            
        minutes_played = df['minutes_played'].values[0]
        
        # User Rule: unused subs (0 minutes) don't even show up
        if minutes_played == 0:
            continue # Skip adding to scores list
            
        t_score = df['goals_scored'].values[0]
        t_conc = df['goals_conceded'].values[0]
        
        score = 0
        try:
            score = score_calc_wrapper(pos, df, t_score, t_conc)
        except Exception as e:
            print(f"Error calculating score for {name} ({pos}): {e}")
            score = 0
            
        scores.append([name, score, pos])
    
    # Create final result DataFrame
    if not scores:
        return pd.DataFrame(columns=["name", "score", "pos"])

    # Convert scores to DF
    scores_df = pd.DataFrame(scores, columns=["name", "score", "pos"])
    
    # Merge scores back to final_df_with_plus_minus to keep all stats
    # final_df_with_plus_minus has 'Unnamed: 0_level_0_Player' as name
    stacked_df = final_df_with_plus_minus.merge(scores_df, left_on='Unnamed: 0_level_0_Player', right_on='name', how='inner')
    
    # Filter out specific test player if needed (legacy code)
    stacked_df = stacked_df[stacked_df["name"]!="Pedrinho"]
    
    stacked_df['score'] = stacked_df['score'].astype(int)
    
    return stacked_df

