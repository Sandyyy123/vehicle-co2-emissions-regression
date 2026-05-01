# Modeling 2 - Tuned XGBoost (CO2 g/km Regression)

## What changed vs `modeling_1.md`

Same feature set, same train/val/test split, same XGBoost backbone; deeper trees, more boosting rounds, lower learning rate.

Final config: `n_estimators=400, max_depth=8, learning_rate=0.05, subsample=0.9, colsample_bytree=0.8, tree_method='hist'`.

## Test results

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Linear Regression (modeling_1) | 2.095 | 1.175 | 0.9971 |
| Random Forest (modeling_1) | 1.940 | 0.208 | 0.9975 |
| XGBoost baseline (modeling_1) | 0.989 | 0.288 | 0.9994 |
| **XGBoost tuned (this run)** | **0.949** | **0.156** | **0.9994** |

Tuning shaves 4% off test RMSE (0.989 -> 0.949) and almost halves MAE (0.288 -> 0.156). Validation RMSE is 0.469 vs test 0.949: the held-out test split is harder than the validation slice, suggesting some near-duplicate variant rows fall on the val side. R² is already ceiling-bound at 0.9994.

## Validation curve

Validation RMSE drops steadily with depth and tree count up to depth 8 / 400 trees. Going deeper (10) overfits without test gain on this sample size.

## The honest variant - drop consumption leakage

Removing the three `Consommation *` columns and the `HC` / `NOX` / `Particules` pollutant columns and re-fitting on the same XGBoost config gives a much harder problem: predict CO2 from mass, engine power, fuel type, body type, transmission, and gamme.

That variant is captured in the `modeling_3` slot (planned) and is expected to drop test R² below 0.95 with RMSE in the 8-12 g/km range, based on the literature for "type-approval CO2 prediction without consumption inputs" (e.g. Tietge 2017 ICCT comparative analysis, Fontaras 2017 PECS review).

## Takeaways

- Tuning yields a small absolute gain on a problem where the physical identity dominates.
- The interesting modeling problem is the leakage-stripped one. `modeling_3` (out of scope here) does that.
- Even with consumption features kept, the residual structure XGBoost picks up (low-CO2 hybrids, bi-fuel petrol/LPG, Euro-class effects) is meaningful for understanding model uncertainty.

## Persisted artifacts

- `deliverables/co2_xgboost.pkl` - tuned XGBoost pipeline
- `deliverables/metrics.json` - full per-split metrics for all four models
- `deliverables/feature_importance_rf.png` - top features bar chart
- `deliverables/residuals_xgb_baseline.png` - residual distribution (XGBoost baseline)
