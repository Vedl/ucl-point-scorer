
# Re-optimize WITHOUT rating, using pass accuracy
import numpy as np
from scipy.optimize import minimize

# Data: (name, target, saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch)
data = [
    ("Rulli", 17, 1, 0, 1, 5, 3, 33, 4, 1, 0),
    ("Alisson", 45, 4, 1, 2, 8, 1, 16, 8, 0, 0),
    ("Chevalier", 23, 2, 0, 0, 7, 1, 21, 1, 0, 0),
    ("Neuer", 35, 1, 1, 0, 4, 0, 34, 2, 0, 0),
    ("Sommer", 19, 3, 0, 0, 9, 0, 23, 5, 0, 0),
    ("Raya", 34, 3, 2, 0, 12, 0, 19, 16, 0, 0),
]

def calc_score(params, stats):
    base, w_save, w_claim, w_sweep, w_rec, w_clr, w_acc_pass, w_fail_pass, w_og, w_punch = params
    saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch = stats
    mins_bonus = 3
    return (base + mins_bonus + 
            w_save*saves + w_claim*claims + w_sweep*sweep + 
            w_rec*rec + w_clr*clears + w_acc_pass*acc_pass + w_fail_pass*fail_pass + 
            w_og*og + w_punch*punch)

def objective(params):
    total_error = 0
    for name, target, saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch in data:
        calc = calc_score(params, (saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch))
        total_error += (calc - target) ** 2
    return total_error

# Initial guess
x0 = [10, 3, 5, 3, 0.5, 1, 0.2, -1, -5, 0.5]

# Bounds
bounds = [
    (-20, 30),   # base (clean sheet base)
    (0, 12),     # saves
    (0, 15),     # claims  
    (0, 10),     # sweep
    (-3, 3),     # rec
    (-5, 10),    # clears
    (-1, 2),     # acc_pass (positive reward)
    (-5, 1),     # fail_pass (negative penalty)
    (-15, 0),    # og
    (0, 5),      # punch
]

result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

print("Optimized Coefficients (v7 WITHOUT rating):")
print("="*60)
base, w_save, w_claim, w_sweep, w_rec, w_clr, w_acc_pass, w_fail_pass, w_og, w_punch = result.x
print(f"Base: {base:.2f}")
print(f"Saves: {w_save:.2f}")
print(f"High Claims: {w_claim:.2f}")
print(f"Sweeper: {w_sweep:.2f}")
print(f"Recoveries: {w_rec:.2f}")
print(f"Clearances: {w_clr:.2f}")
print(f"Accurate Passes: {w_acc_pass:.3f}")
print(f"Failed Passes: {w_fail_pass:.3f}")
print(f"Own Goals: {w_og:.2f}")
print(f"Punches: {w_punch:.2f}")

print("\nVerification:")
print("="*60)
for name, target, saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch in data:
    calc = calc_score(result.x, (saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch))
    diff = calc - target
    status = "✅" if abs(diff) < 1.5 else "❌"
    print(f"{status} {name:12} Target={target:3} Calc={calc:5.1f} Diff={diff:+5.1f}")

print("\nTotal Error:", result.fun)
