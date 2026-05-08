# Improvements - Project 05: CO2 Emissions by Vehicles

**Reviewer role:** IMPROVER
**Date:** 2026-05-08
**Scope:** recommendations only, no file modifications.

---

## Top recommendation (single highest-leverage change)

**Run and report the leakage-stripped variant (`modeling_3`) as the primary deliverable, not as a footnote.** The current headline (RMSE 0.949 g/km, R2 0.9994) is a closed-form algebraic identity, not a learning result, and the manuscript itself flags this. The brief explicitly asks to "anticipate emissions for new vehicle series before they reach market", which is precisely the design-only setting (mass, power, fuel type, body, transmission, segment, no consumption inputs). Build that variant with the same XGBoost + tuned configuration, add 5-fold cross-validation with bootstrap CIs (n=1000) on RMSE/MAE/R2, and present its metrics in Table 1 with the consumption-included variant relegated to a sensitivity appendix. This single change converts the project from "ML fits stoichiometry" to "ML predicts engineering CO2 from a vehicle dossier" - the latter is publishable, defensible, and matches the regulatory framing. Priority: **HIGH**.

---

## Weakness 1: Train/val/test split is row-level, not group-level (data leakage of a different kind)

**Issue.** The 60/20/20 random split places near-duplicate Type-Variante-Version rows from the same `Modele dossier` (e.g. 200 BMW 320d trim variants) into all three folds. The validation RMSE (0.469) being half the test RMSE (0.949) is a direct fingerprint of this: the val split caught row-level neighbours of training points. The reported generalisation is to *unseen variants of seen models*, not to genuinely new vehicle series.

**Fix.** Switch to `GroupKFold` with `Modele dossier` (or `Marque + Modele dossier`) as the group key. Re-report metrics. Expect test RMSE in the consumption-included variant to roughly double; in the consumption-stripped variant it will reveal whether the model generalises to a brand-new model line at all. This is the "brand-level CV" already mentioned in Methods 3.2 - actually run it. Priority: **HIGH**.

---

## Weakness 2: No bootstrap confidence intervals or repeated seeds

**Issue.** Single random seed (42), single split, single number per cell in Table 1. No claim about how stable RMSE 0.949 is under resampling. The Discussion already acknowledges "a single random seed without bootstrap confidence intervals" as a limitation, then leaves it unresolved.

**Fix.** Run 5 seeds (42, 7, 13, 100, 2026) and report mean +/- std for RMSE/MAE/R2. Add a 1000-sample non-parametric bootstrap on the test fold for CI on each metric. With n_test = 8,963, bootstrap is cheap (under 1 minute on CPU). Add to `metrics.json` and Table 1. Priority: **MEDIUM**.

---

## Weakness 3: Heteroscedastic right tail not addressed; no log-CO2 or robust loss tried

**Issue.** EDA explicitly identifies a heavy right tail (12.18% IQR outliers, max 572 g/km Aston Martin One-77) and a thin left mode (PHEVs at 27 g/km). Both are biased predictors at the tails because XGBoost with squared loss compresses the tails. Manuscript Section 5 mentions this but does not address it.

**Fix.** Three concrete experiments: (a) target = `log(CO2 + 1)` with inverse transform at predict time, (b) XGBoost with `objective='reg:pseudohubererror'` and `huber_slope=1.0`, (c) Quantile Regression Forest at q=0.05/0.50/0.95 to ship prediction intervals (more useful for regulators than point estimates). Compare RMSE on the upper-decile and lower-decile slices. Priority: **MEDIUM**.

---

## Weakness 4: Feature importance uses impurity only; no SHAP, no permutation importance

**Issue.** Manuscript Section 5 explicitly notes "reliance on impurity-based feature importance rather than SHAP" as a limitation. Impurity importance is biased toward high-cardinality and continuous features and is unstable across seeds. With only one consumption column dominating (0.791), the headline feature ranking could mislead a client.

**Fix.** Add (a) `sklearn.inspection.permutation_importance` on the test fold (10 repeats), and (b) SHAP TreeExplainer on a 2,000-row test sample with a beeswarm summary plot and a force plot for one diesel and one petrol exemplar. Persist both as `deliverables/shap_summary.png` and `deliverables/permutation_importance.csv`. SHAP also enables the per-prediction explanations a regulator would need for compliance audits. Priority: **MEDIUM**.

---

## Weakness 5: Feature engineering is shallow; physics-informed features are missing

**Issue.** The `_build_modeling_notebook.py` script adds only mid-mass, log-mass, power-to-weight, and fiscal-power x mass. The literature (Weiss 2020 [23]; Tietge 2017 [16]) identifies several stronger predictors that the carlab dataset can construct: (a) engine displacement is implicit in Puissance fiscale (French CV formula encodes displacement and CO2 historically), (b) Carrosserie x mass interaction (frontal area proxy, drives aerodynamic load), (c) gearbox count from `Boite de vitesse` parsed (M 6 -> 6 ratios; modern 8-speeds reduce CO2 by 3-5%), (d) Euro standard ordinal (Champ V9: Euro 4/5/6 ordinal, not one-hot - newer standards correlate with lower CO2 via efficiency mandates).

**Fix.** Add four engineered features: `gear_count` (parsed from `Boite de vitesse`), `transmission_type` (M/A/V from prefix), `euro_standard_ordinal` (4, 5, 6, 6b mapped to 4-7), and `mass_x_body` (interaction). Re-run RF/XGB. Likely gain 2-4 g/km RMSE in the leakage-stripped variant. Priority: **MEDIUM**.

---

## Weakness 6: Reproducibility gaps - no `requirements.txt`, no Docker, no data-version pin

**Issue.** The project root has no `requirements.txt`, no `pyproject.toml`, no `environment.yml`. The notebook imports xgboost, sklearn, pandas, joblib without specifying versions. The CSV is read from a relative path (`../data/`) without checksum verification. A second analyst cannot reliably reproduce RMSE 0.949 because xgboost 1.x vs 2.x give different floating-point results on the same seed.

**Fix.** Add `requirements.txt` pinning xgboost==2.1.3, scikit-learn==1.5.2, pandas==2.2.3, numpy==1.26.4, joblib==1.4.2. Add a `data/CHECKSUMS.sha256` file with the SHA-256 of `cl_JUIN_2013-complet3.csv` (currently 9,021,508 bytes). Add a 5-line `Makefile` (`make data`, `make train`, `make report`). Optional: a 30-line Dockerfile for full pinning. Priority: **HIGH** (this is what the brief calls "architecture / model serving notes" in `reports/architecture.md`, which is currently missing).

---

## Weakness 7: Missing reports per the README checklist

**Issue.** The README lists 8 required reports; only 3 exist (`exploration_1.md`, `modeling_1.md`, `modeling_2.md`). Missing: `exploration_2.md` (distributions, correlations, viz), `exploration_3.md` (feature engineering, preprocessing plan), `modeling_3.md` (final model, error analysis - this is the leakage-stripped variant), `architecture.md` (data flow, batch scoring), `final_report.md` (executive summary). The notebook checklist also lists 4 notebooks but only `01_eda.ipynb` and `03_modeling.ipynb` exist (`02_features.ipynb` and `04_evaluation.ipynb` are absent).

**Fix.** Generate the 5 missing markdown reports. Most can be produced from existing artefacts (manuscript already covers exploration_2/3 content; modeling_3 is the leakage-stripped run from Weakness 1; architecture.md is a 1-page batch-scoring sketch using the persisted .pkl). Without these, the project cannot pass Liora validation. Priority: **HIGH**.

---

## Weakness 8: Presentation does not show error analysis or business framing

**Issue.** `deliverables/presentation.html` (225 KB) exists but the manuscript and reports do not include: a confusion matrix on emission-class buckets (e.g. EU 95 g/km compliance vs non-compliance bucket - the brief explicitly asks about this), per-segment error bars (luxury vs economy fail differently), or a calibration plot on PHEV/BEV outliers. A business audience needs the "which vehicles will fail compliance?" view, not RMSE.

**Fix.** Add three deliverables: (a) bucket the predictions into [<95, 95-130, 130-200, >200] g/km bins, build a 4x4 confusion matrix on the test fold, report per-bucket precision/recall, (b) per-segment (`gamme`) RMSE table - luxe vs economique vs urbaine etc., (c) a slide showing the EU 95 g/km threshold horizontal line on a predicted-vs-actual scatter, with off-target vehicles labelled by Marque. This converts the deliverable from an academic exercise to a regulatory-grade tool. Priority: **MEDIUM**.

---

## Weakness 9: PHEV/BEV handling is acknowledged but not implemented

**Issue.** Manuscript Section 5 paragraph on hybrid/electric vehicles correctly notes that PHEV CO2 (27 g/km) is utility-factor-weighted and BEVs may be coded as zero or NaN. None of the modelling code segments these out. Tree models will fit the PHEV tail by `Hybride='oui'` + low-mass split, which is brittle - a new PHEV variant outside the training range will be predicted poorly.

**Fix.** Either (a) train a separate model for `Hybride='oui'` rows (n is small but the relationship is structurally different), (b) add a binary `is_phev_or_bev` feature based on `Carburant in {EE, EH}` and check XGBoost behaviour with that as a stratum, or (c) explicitly exclude PHEV/BEV from training and report two metric tables: ICE-only and full sample. Option (c) is the cleanest given the dataset constraints. Priority: **LOW** (small population, large fix; address only if time permits).

---

## Priority summary

| Weakness | Priority |
|---|---|
| 1. Run leakage-stripped variant as headline (Top recommendation) | HIGH |
| 2. GroupKFold by Modele dossier | HIGH |
| 6. requirements.txt + Makefile + checksums | HIGH |
| 7. Generate 5 missing reports + 2 missing notebooks | HIGH |
| 3. Bootstrap CIs + 5 seeds | MEDIUM |
| 4. Heteroscedastic loss + log-CO2 + quantile regression | MEDIUM |
| 5. SHAP + permutation importance | MEDIUM |
| 8. Physics-informed features (gear count, euro ordinal, body x mass) | MEDIUM |
| 9. Business-facing presentation: compliance buckets, per-segment RMSE | MEDIUM |
| 10. PHEV/BEV stratified handling | LOW |

---

**Role B (IMPROVER) complete.**
