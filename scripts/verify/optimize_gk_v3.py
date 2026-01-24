
# Re-optimize with 4 data points including Scherpen
import numpy as np
from scipy.optimize import minimize

# Data: (name, target, saves, claims, sweeper, rec, passes, clears, og)
# All at 90 mins (mins_bonus = 3)
data = [
    ("Alisson", 45, 4, 1, 2, 8, 16, 1, 0),       # Liverpool vs Marseille
    ("Rulli", 17, 1, 0, 1, 5, 33, 3, 1),         # Marseille vs Liverpool (OG!)
    ("Chevalier", 23, 2, 0, 0, 7, 21, 1, 0),     # PSG vs Sporting  
    ("Scherpen", 35, 2, 3, 0, 10, 16, 1, 0),     # Bayern vs Union SG (user says 35)
]

def calc_score(params, stats):
    base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og, w_punch = params
    saves, claims, sweep, rec, passes, clears, og = stats
    punch = 0  # Will add punch data if needed
    mins_bonus = 3
    return (base + mins_bonus + 
            w_save*saves + w_claim*claims + w_sweep*sweep + 
            w_rec*rec + w_pass*passes + w_clr*clears + w_og*og + w_punch*punch)

def objective(params):
    total_error = 0
    for name, target, saves, claims, sweep, rec, passes, clears, og in data:
        calc = calc_score(params, (saves, claims, sweep, rec, passes, clears, og))
        total_error += (calc - target) ** 2
    return total_error

# Initial guess with punch weight
x0 = [10.54, 5.52, 2.40, 3.53, 0.29, -0.24, 1.36, -3.28, 0.5]

# Bounds
bounds = [
    (5, 20),    # base
    (3, 12),    # saves
    (1, 8),     # claims  
    (1, 8),     # sweep
    (0, 3),     # rec
    (-1, 0.5),  # pass
    (0, 4),     # clr
    (-10, 0),   # og
    (0, 3),     # punch
]

result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

print("Optimized Coefficients (v3 with Scherpen):")
print("="*60)
base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og, w_punch = result.x
print(f"Base (Clean Sheet): {base:.2f}")
print(f"Saves: {w_save:.2f}")
print(f"High Claims: {w_claim:.2f}")
print(f"Sweeper (Runs Out): {w_sweep:.2f}")
print(f"Recoveries: {w_rec:.2f}")
print(f"Passes: {w_pass:.3f}")
print(f"Clearances: {w_clr:.2f}")
print(f"Own Goals: {w_og:.2f}")
print(f"Punches: {w_punch:.2f}")

print("\nVerification:")
print("="*60)
for name, target, saves, claims, sweep, rec, passes, clears, og in data:
    calc = calc_score(result.x, (saves, claims, sweep, rec, passes, clears, og))
    diff = calc - target
    status = "✅" if abs(diff) < 0.6 else "❌"
    print(f"{status} {name:12} Target={target:3} Calc={calc:5.1f} Diff={diff:+5.1f}")
