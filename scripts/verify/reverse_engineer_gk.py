
# Reverse engineering GK formula using 3 data points
# We know:
# Alisson = 45, Rulli = 17, Chevalier = 23
# All had clean sheets (0 conceded)

# Stats:
# GK           Saves  Claims  Sweeper  Recovery  Passes  Clears  Rating
# Alisson      4      1       2        8         16      1       8.3
# Rulli        1      0       1        5         33      3       5.8
# Chevalier    2      0       0        7         21      1       6.3

# Let's try: Score = Base + a*Saves + b*Claims + c*Sweeper + d*Recovery + e*Passes + f*Clears + g*Rating
# With Clean Sheet Base = 10, Minutes bonus = 3 (90/30)

# Subtracting base (13) from targets:
# Alisson: 45 - 13 = 32
# Rulli: 17 - 13 = 4
# Chevalier: 23 - 13 = 10

# Let's try different save weights to see what makes sense
# If we weight saves heavily:

print("Testing different coefficients:")
print("="*80)

def calc_score(saves, claims, sweeper, recovery, passes, clears, rating, 
               base=10, mins_bonus=3, 
               w_saves=5, w_claims=2, w_sweeper=3, w_recovery=0.5, w_passes=0.1, w_clears=1, w_rating=0):
    return (base + mins_bonus + 
            w_saves * saves + 
            w_claims * claims + 
            w_sweeper * sweeper + 
            w_recovery * recovery + 
            w_passes * passes + 
            w_clears * clears +
            w_rating * rating)

# Data
players = [
    ("Alisson", 45, 4, 1, 2, 8, 16, 1, 8.3),
    ("Rulli", 17, 1, 0, 1, 5, 33, 3, 5.8),
    ("Chevalier", 23, 2, 0, 0, 7, 21, 1, 6.3),
]

# Try different weight combinations
configs = [
    # (saves, claims, sweeper, recovery, passes, clears, rating_mult)
    ("Current", 1.5, 1.0, 1.5, 0.5, 0.1, 1.5, 0),
    ("High Saves", 5.0, 2.0, 3.0, 0.5, 0.1, 1.0, 0),
    ("Rating Based", 3.0, 1.5, 2.0, 0.3, 0.05, 0.5, 3.0),
    ("Balanced", 4.0, 2.0, 2.5, 0.5, -0.1, 1.0, 0),
    ("Negative Pass", 4.5, 2.0, 2.5, 0.5, -0.15, 1.0, 0),
]

for name, ws, wc, wsw, wr, wp, wcl, wrat in configs:
    print(f"\n{name}: Saves={ws}, Claims={wc}, Sweep={wsw}, Rec={wr}, Pass={wp}, Clr={wcl}, Rat={wrat}")
    for pname, target, saves, claims, sweep, rec, passes, clears, rating in players:
        calc = calc_score(saves, claims, sweep, rec, passes, clears, rating,
                          w_saves=ws, w_claims=wc, w_sweeper=wsw, w_recovery=wr, 
                          w_passes=wp, w_clears=wcl, w_rating=wrat)
        diff = calc - target
        print(f"  {pname:12} Target={target:3} Calc={calc:5.1f} Diff={diff:+5.1f}")
