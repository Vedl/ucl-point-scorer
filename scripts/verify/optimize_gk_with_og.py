
# Re-optimize with actual data including Rulli's OG
import numpy as np
from scipy.optimize import minimize

# Updated data with OGs:
# GK           Saves  Claims  Sweeper  Rec   Passes  Clears  OG  Target
# Alisson      4      1       2        8     16      1       0   45
# Rulli        1      0       1        5     33      3       1   17  <- HAS OG!
# Chevalier    2      0       0        7     21      1       0   23

data = [
    ("Alisson", 45, 4, 1, 2, 8, 16, 1, 0),
    ("Rulli", 17, 1, 0, 1, 5, 33, 3, 1),  # OG=1
    ("Chevalier", 23, 2, 0, 0, 7, 21, 1, 0),
]

def calc_score(params, stats):
    base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og = params
    saves, claims, sweep, rec, passes, clears, og = stats
    mins_bonus = 3
    return (base + mins_bonus + 
            w_save*saves + w_claim*claims + w_sweep*sweep + 
            w_rec*rec + w_pass*passes + w_clr*clears + w_og*og)

def objective(params):
    total_error = 0
    for name, target, saves, claims, sweep, rec, passes, clears, og in data:
        calc = calc_score(params, (saves, claims, sweep, rec, passes, clears, og))
        total_error += (calc - target) ** 2
    return total_error

# Initial guess: base=10, saves=5, claims=2, sweep=3, rec=0.5, pass=-0.2, clr=1, og=-3.5
x0 = [10, 5, 2, 3, 0.5, -0.2, 1, -3.5]

# Bounds
bounds = [(5, 15), (3, 10), (1, 5), (1, 6), (0, 2), (-0.5, 0.2), (0, 3), (-10, 0)]

result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

print("Optimized Coefficients:")
print("="*60)
base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og = result.x
print(f"Base (Clean Sheet): {base:.2f}")
print(f"Saves: {w_save:.2f}")
print(f"High Claims: {w_claim:.2f}")
print(f"Sweeper (Runs Out): {w_sweep:.2f}")
print(f"Recoveries: {w_rec:.2f}")
print(f"Passes: {w_pass:.3f}")
print(f"Clearances: {w_clr:.2f}")
print(f"Own Goals: {w_og:.2f}")

print("\nVerification:")
print("="*60)
for name, target, saves, claims, sweep, rec, passes, clears, og in data:
    calc = calc_score(result.x, (saves, claims, sweep, rec, passes, clears, og))
    print(f"{name:12} Target={target:3} Calc={calc:5.1f} Diff={calc-target:+5.1f}")
