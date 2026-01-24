
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.tree import export_text

# Load data
with open("gk_optimization_data.pkl", "rb") as f:
    raw_data = pickle.load(f)

print(f"Loaded {len(raw_data)} data points")

# Prepare DataFrame
# columns: name, target, saves, claims, sweep, rec, clears, acc_pass, fail_pass, og, punch, sv_inside, poss_lost, pk_save, pk_faced, gp, ksv
cols = ["name", "target", "saves", "claims", "sweep", "rec", "clears", "acc_pass", "fail_pass", "og", "punch", "sv_inside", "poss_lost", "pk_save", "pk_faced", "gp", "ksv"]
df = pd.DataFrame(raw_data, columns=cols)

# Check for duplicates/contradictions
feature_cols = cols[2:]
duplicates = df[df.duplicated(subset=feature_cols, keep=False)]
if not duplicates.empty:
    print("\nWARNING: Found duplicate stats with potentially different targets:")
    print(duplicates.sort_values(by=feature_cols))
    
    # Check consistency
    for _, group in duplicates.groupby(feature_cols):
        if group['target'].nunique() > 1:
            print("❌ CONTRADICTION FOUND:")
            print(group[['name', 'target']])

X = df[feature_cols]
y = df['target']

# Train Random Forest
rf = RandomForestRegressor(n_estimators=500, random_state=42, max_depth=10)
rf.fit(X, y)

y_pred = rf.predict(X)
rmse = np.sqrt(mean_squared_error(y, y_pred))
print(f"\nRandom Forest RMSE (Train): {rmse:.4f}")

# Train GBM
gbm = GradientBoostingRegressor(n_estimators=500, random_state=42, learning_rate=0.05)
gbm.fit(X, y)
y_pred_gbm = gbm.predict(X)
rmse_gbm = np.sqrt(mean_squared_error(y, y_pred_gbm))
print(f"Gradient Boosting RMSE (Train): {rmse_gbm:.4f}")

# Feature Importance
print("\nFeature Importance (RF):")
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
for f in range(X.shape[1]):
    print(f"{feature_cols[indices[f]]:20}: {importances[indices[f]]:.4f}")

print("\nAccuracy Check (Threshold < 1.0):")
correct = 0
for i in range(len(y)):
    diff = abs(y.iloc[i] - y_pred[i])
    status = "✅" if diff < 1.0 else "❌"
    if diff < 1.0: correct += 1
    if diff > 5.0:
        print(f"{status} {df.iloc[i]['name']:40} Target={y.iloc[i]} Pred={y_pred[i]:.1f} Diff={diff:.1f}")

print(f"\nPassed: {correct}/{len(y)} ({correct/len(y)*100:.1f}%)")

# Save the best model (GBM)
import joblib
joblib.dump(gbm, "gk_gbm_model.pkl")
print("Saved Gradient Boosting model to gk_gbm_model.pkl")
