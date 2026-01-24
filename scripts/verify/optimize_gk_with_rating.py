
# Re-optimize with rating as a factor
import numpy as np
from scipy.optimize import minimize

# Data: (name, target, saves, claims, sweeper, rec, passes, clears, og, punch, rating)
data = [
    ("Alisson", 45, 4, 1, 2, 8, 16, 1, 0, 0, 8.3),
    ("Rulli", 17, 1, 0, 1, 5, 33, 3, 1, 0, 5.8),
    ("Chevalier", 23, 2, 0, 0, 7, 21, 1, 0, 0, 6.3),     
    ("Neuer", 35, 1, 1, 0, 4, 34, 0, 0, 0, 7.1),
]

def calc_score(params, stats):
    base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og, w_punch, w_rating = params
    saves, claims, sweep, rec, passes, clears, og, punch, rating = stats
    mins_bonus = 3
    return (base + mins_bonus + 
            w_save*saves + w_claim*claims + w_sweep*sweep + 
            w_rec*rec + w_pass*passes + w_clr*clears + w_og*og + 
            w_punch*punch + w_rating*rating)

def objective(params):
    total_error = 0
    for name, target, saves, claims, sweep, rec, passes, clears, og, punch, rating in data:
        calc = calc_score(params, (saves, claims, sweep, rec, passes, clears, og, punch, rating))
        total_error += (calc - target) ** 2
    return total_error

# Initial guess with rating
x0 = [0, 5, 3, 3, 0.5, 0, 1, -3, 0.5, 5]

# Bounds
bounds = [
    (-10, 25),   # base
    (0, 12),     # saves
    (0, 8),      # claims  
    (0, 8),      # sweep
    (-1, 3),     # rec
    (-0.5, 0.5), # pass
    (-2, 5),     # clr
    (-15, 0),    # og
    (0, 5),      # punch
    (0, 10),     # rating
]

result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

print("Optimized Coefficients (v5 with rating):")
print("="*60)
base, w_save, w_claim, w_sweep, w_rec, w_pass, w_clr, w_og, w_punch, w_rating = result.x
print(f"Base: {base:.2f}")
print(f"Saves: {w_save:.2f}")
print(f"High Claims: {w_claim:.2f}")
print(f"Sweeper: {w_sweep:.2f}")
print(f"Recoveries: {w_rec:.2f}")
print(f"Passes: {w_pass:.3f}")
print(f"Clearances: {w_clr:.2f}")
print(f"Own Goals: {w_og:.2f}")
print(f"Punches: {w_punch:.2f}")
print(f"Rating: {w_rating:.2f}")

print("\nVerification:")
print("="*60)
for name, target, saves, claims, sweep, rec, passes, clears, og, punch, rating in data:
    calc = calc_score(result.x, (saves, claims, sweep, rec, passes, clears, og, punch, rating))
    diff = calc - target
    status = "✅" if abs(diff) < 0.6 else "❌"
    print(f"{status} {name:12} Target={target:3} Calc={calc:5.1f} Diff={diff:+5.1f}")

print("\nTotal Error:", result.fun)
