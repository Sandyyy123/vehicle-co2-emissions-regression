# Modeling 1 - Baseline (CO2 g/km Regression)

## Task

Predict tailpipe CO2 emissions in grams per kilometer (`CO2 (g/km)`) for French passenger cars (ADEME carlab June 2013 release) from technical attributes.

After dropping rows with missing target and four high-cardinality identifier columns (`Modèle dossier`, `Modèle UTAC`, `Désignation commerciale`, `Type Variante Version (TVV)`), the modeling table holds 44,811 vehicles with 20 features (12 numeric, 8 categorical).

## Important note on features kept

The carlab file ships with three fuel-consumption columns (`Consommation urbaine`, `Consommation extra-urbaine`, `Consommation mixte`) that are physically tied to CO2 by combustion stoichiometry. They were retained in this baseline because (a) they are part of the standard regulatory fingerprint, (b) the user-facing question is "given the published vehicle dossier, predict CO2", and (c) the goal of `modeling_1` is to ground the achievable ceiling. Pollutant columns (`HC`, `NOX`, `Particules`, `CO type 1`) were also retained.

A leakage-stripped variant is the focus of `modeling_2.md` (deeper interpretation) but the consumption-included baseline is reported here so the gap is explicit.

## Split

Random 60/20/20 split with `random_state=42`:

- Train: 26,886
- Val: 8,962
- Test: 8,963

## Baselines

| Model | Val RMSE | Test RMSE | Test MAE | Test R² |
|---|---|---|---|---|
| Linear Regression | 2.043 | 2.095 | 1.175 | 0.9971 |
| Random Forest (200 trees, max_depth=15) | 1.308 | 1.940 | 0.208 | 0.9975 |
| XGBoost (200 trees, depth 6, lr 0.10) | 0.634 | 0.989 | 0.288 | 0.9994 |

All three are essentially fit by the consumption-CO2 physical identity, so R² is ceiling-bound near 1.0. The interesting differences are in RMSE and MAE.

## Top features (Random Forest, impurity-based)

| Feature | Importance |
|---|---|
| Consommation extra-urbaine (l/100km) | 0.791 |
| Consommation mixte (l/100km) | 0.180 |
| Puissance administrative | 0.0055 |
| NOX (g/km) | 0.0043 |
| Consommation urbaine (l/100km) | 0.0031 |
| Carburant_GP/ES (LPG / petrol bi-fuel) | 0.0026 |
| Puissance maximale (kW) | 0.0018 |
| Carburant_GO (diesel) | 0.0015 |
| masse vide euro max (kg) | 0.0013 |
| Carburant_ES/GN (petrol / CNG bi-fuel) | 0.0010 |

Two consumption columns capture 97% of impurity importance. Once those are present, mass and engine power add only marginal signal because the physical relation `CO2 = fuel_consumption x C_to_CO2_factor / fuel_density` already pins the answer.

## Configuration details

- Linear Regression on standardised numeric features + one-hot categorical, `LinearRegression` defaults.
- Random Forest: `n_estimators=200`, `max_depth=15`, `min_samples_leaf=3`, no scaling.
- XGBoost (baseline): `n_estimators=200`, `max_depth=6`, `learning_rate=0.1`, `subsample=0.9`, `colsample_bytree=0.8`, `tree_method='hist'`.
- Categorical pre-processing: `OneHotEncoder(handle_unknown='ignore')` for both tree and linear models. Numeric imputation with median; categorical imputation with most-frequent.

## Takeaways

- Even Linear Regression hits R² 0.997 because of the consumption-CO2 identity in the feature set. The signal is mostly closed-form.
- XGBoost beats Random Forest by 50% on RMSE (0.989 vs 1.940). It learns the residual non-linearity around fuel-type-specific factors.
- The MAE gap between Random Forest (0.21 g/km) and XGBoost baseline (0.29 g/km) is small in absolute terms (the target's standard deviation is ~38 g/km).

## Next step

`modeling_2.md` tunes XGBoost on the same feature set and discusses the leakage-aware variant where the three consumption columns are removed. That second variant is the realistic generalisation of "predict CO2 from vehicle make-up before any test cycle is run".
