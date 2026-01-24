# UCL Fantasy Scoring Statistics

The following statistics are scraped from SofaScore/WhoScored and used in the scoring algorithm.

## 1. Attacking Stats
- **Goals** (`Performance_Gls`): +10 points
- **Assists** (`Performance_Ast`): +8 points
- **Shots on Target** (`Performance_SoT`)
- **Total Shots** (`Performance_Sh`)
- **Key Passes** (`KP`)
- **Crosses** (`Performance_Crs`)
- **Dribbles Won** (`Take-Ons_Succ`)
- **Dribbles Attempted** (`Take-Ons_Att`)
- **Offsides** (`Performance_Off`)

## 2. Defensive Stats
- **Tackles Won** (`Performance_Tkl`)
- **Interceptions** (`Performance_Int`)
- **Clearances** (`Clr`)
- **Shots Blocked** (`Blocks_Sh`)
- **Aerial Duels Won** (`Aerial Duels_Won`)
- **Aerial Duels Lost** (`Aerial Duels_Lost`)
- **Possession Lost/Dispossessed** (`Carries_Dis`)
- **Challenges Lost** (Dribbled Past)
- **Errors Leading to Goal** (`Err`): -5 points
- **Own Goals**: -3.5 points (DEF/GK)

## 3. Passing & Possession
- **Passes Completed** (`Passes_Cmp`)
- **Passes Attempted** (`Passes_Att`)
- **Fouls Committed** (`Performance_Fls`)

## 4. Discipline
- **Yellow Card**: -5 points
- **Red Card**: -5 points
- **Penalty Won**: +6.4 points (if not taken by player)
- **Penalty Conceded**: -5 points
- **Penalty Missed**: -5 points

## 5. Goalkeeper Specifics (Reverse-Engineered Formula v10 Live)
- **Goals Prevented**: +9.59 points (Key metric!)
- **High Claims**: +8.40 points
- **Runs Out (Sweeper)**: +5.01 points
- **Penalty Faced**: +5.00 points
- **Base (Clean Sheet)**: +20.46 points
- **Saves**: +1.33 points
- **Clearances**: +1.07 points
- **Failed Passes**: +2.00 per pass (volume indicator?)
- **Accurate Passes**: +0.19 per pass
- **Recoveries**: -0.22 points
- **Possession Lost**: -2.05 points
- **Saved Inside Box**: -3.17 points
- **Keeper Save Value**: -4.25 points
- **Punches**: -5.90 points
- **Goals Conceded**: Implicitly covered by 'Goals Prevented'
- **Minutes Bonus**: +3 (for 90 mins)

## 5. Contextual Stats (impact score)
- **Minutes Played**: (must be >0 for points)
  - <45 mins + No Clean Sheet: -5 points
- **Team Goals Scored** (while on pitch)
- **Team Goals Conceded** (while on pitch)
  - **Clean Sheet Bonus**: +10 points (Defs), +4 points (Mids)

---

## Positional Coefficients (Multipliers)

The algorithm applies different weights depending on the player's position (FWD, MID, DEF).

| Stat | DEF | MID | FWD |
|------|-----|-----|-----|
| Aerial Duels Won | 1.9 | 1.7 | 1.4 |
| Aerial Duels Lost | -1.5 | -1.5 | -0.4 |
| Tackles | 2.7 | 2.6 | 2.6 |
| Interceptions | 2.7 | 2.5 | 2.7 |
| Clearances | 1.1 | 1.1 | 0.8 |
| Dribbles Won | 2.5 | 2.9 | 3.0 |
| Shots on Target | 2.5 | 2.2 | 3.0 |
| Blocked Shots | 1.1 | 1.1 | 0.8 |
| Crosses | 1.2 | 1.2 | 1.2 |
| Key Passes | 1.5 | 1.5 | 1.5 |

*Note: This is a simplified view; the actual code uses complex composite formulas.*
