
# Fine-tuning GK formula
# Key observations:
# 1. Alisson has high saves (4), rating (8.3), but few passes (16)
# 2. Rulli has low saves (1), rating (5.8), and MANY passes (33)
# 3. Chevalier is in between

# The formula likely PENALIZES excessive passing (distribution errors?)
# And heavily rewards saves

import numpy as np
from scipy.optimize import minimize

# Data: (name, target, saves, claims, sweeper, recovery, passes, clears)
data = [
    ("Alisson", 45, 4, 1, 2, 8, 16, 1),
    ("Rulli", 17, 1, 0, 1, 5, 33, 3),
    ("Chevalier", 23, 2, 0, 0, 7, 21, 1),
]

def calc_score(params, stats):
    base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr = params
    saves, claims, sweep, rec, passes, clears = stats
    mins_bonus = 3  # 90/30
    return base + mins_bonus + w_save*saves + w_claim*claims + w_sweep*sweep + w_rec*rec + w_pass*passes + w_clr*clears

def objective(params):
    total_error = 0
    for name, target, saves, claims, sweep, rec, passes, clears in data:
        calc = calc_score(params, (saves, claims, sweep, rec, passes, clears))
        total_error += (calc - target) ** 2
    return total_error

# Initial guess: base=10, saves=5, claims=2, sweep=2.5, rec=0.5, pass=-0.2, clr=1
x0 = [10, 5, 2, 2.5, 0.5, -0.2, 1]

# Bounds: base (5-15), saves (3-8), claims (1-4), sweep (1-5), rec (0-2), pass (-0.5 to 0.2), clr (0-3)
bounds = [(5, 15), (3, 10), (1, 5), (1, 6), (0, 2), (-0.5, 0.2), (0, 3)]

result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

print("Optimized Coefficients:")
print("="*60)
base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr = result.x
print(f"Base (Clean Sheet): {base:.2f}")
print(f"Saves: {w_save:.2f}")
print(f"High Claims: {w_claim:.2f}")
print(f"Sweeper (Runs Out): {w_sweep:.2f}")
print(f"Recoveries: {w_rec:.2f}")
print(f"Passes: {w_pass:.3f}")
print(f"Clearances: {w_clr:.2f}")

print("\nVerification:")
print("="*60)
for name, target, saves, claims, sweep, rec, passes, clears in data:
    calc = calc_score(result.x, (saves, claims, sweep, rec, passes, clears))
    print(f"{name:12} Target={target:3} Calc={calc:5.1f} Diff={calc-target:+5.1f}")
