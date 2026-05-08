# Validation Report - Project #05 CO2 Emissions

**Reviewer role:** A (VALIDATOR)
**Project folder:** `/root/AI/liora_projects/05_co2_emissions/`
**Date:** 2026-05-08
**Overall verdict:** PASS-WITH-WARNINGS

## Summary (under 150 words)

Manuscript, notebooks, and deliverables are intact and internally consistent. JSON parses for both notebooks. Manuscript word count 4,470 (in 4000-5000 target). All 9 IMRaD sections present. All 29 inline numeric citations map to entries in `manuscripts/references.md` (the project keeps refs there; `reports/references.md` does not exist). 5 of 5 randomly sampled DOIs resolve via CrossRef with title matches. No em-dashes anywhere. No AI-tell phrases. Presentation HTML has 29 external URLs but all are DOI/arxiv citation links (no external CSS/JS/images), acceptable for academic content. Saved model artefacts (.pkl, .png, metrics.json) present in `deliverables/`. Two warnings: `src/model_baseline.py` and `src/model_advanced.py` are absent (model code lives in `notebooks/03_modeling.ipynb`, expected for #1-#8); `checkpoint.json` is missing; minor methodology drift between manuscript prose and notebook code for RF and XGB-baseline hyperparameters (tuned-XGB matches metrics.json exactly).

## Findings

### Task 1 - Notebook JSON validity
- [PASS] `notebooks/01_eda.ipynb` parses as valid JSON.
- [PASS] `notebooks/03_modeling.ipynb` parses as valid JSON. (Note: `02_features.ipynb` and `04_evaluation.ipynb` listed in README are not present, but the modeling code is consolidated into `03_modeling.ipynb`.)

### Task 2 - Python script syntax (`src/`)
- [WARN] `src/` directory is empty. `src/model_baseline.py` and `src/model_advanced.py` are absent. Per QA rules for projects #1-#8 this is expected (model code lives in notebooks); flagged as WARN, not FAIL.

### Task 3 - Manuscript word count
- [PASS] `manuscripts/manuscript.md` = 4,470 words. Inside the 4000-5000 target.

### Task 4 - Self-contained HTML
- [PASS] `deliverables/presentation.html` has 29 external `href`/`src` matches, but every one is a DOI link (`doi.org`, 26 hits) or arxiv link (`arxiv.org`, 3 hits) inside the references list. There are zero external CSS, JS, fonts, or image hosts. Acceptable for an academic presentation.

### Task 5 - IMRaD completeness
- [PASS] All required sections present: Title, Abstract, 1. Introduction, 2. Data, 3. Methods, 4. Results, 5. Discussion, 6. Conclusion, References. (Section "2. Data" stands in for the conventional "Materials" subhead and contains the dataset description; acceptable IMRaD adaptation for a tabular ML manuscript.)

### Task 6 - Method drift (manuscript Methods vs notebook code)
Manuscript Methods names: Linear Regression (sklearn `LinearRegression`), Random Forest (200 trees, max_depth=15, min_samples_leaf=3), XGBoost baseline (200 trees, max_depth=6, lr=0.10, subsample=0.9, colsample_bytree=0.8, tree_method='hist'), XGBoost tuned (400 trees, max_depth=8, lr=0.05, subsample=0.9, colsample_bytree=0.8), median imputation, most-frequent imputation, OneHotEncoder, 60/20/20 split, random_state=42.

- [PASS] `LinearRegression`, `RandomForestRegressor`, `XGBRegressor`, `OneHotEncoder`, `SimpleImputer(strategy='median')`, `train_test_split`, `random_state=42` (via `RANDOM_STATE = 42`), and `tree_method='hist'` all appear in `notebooks/03_modeling.ipynb`.
- [PASS] Tuned-XGBoost final config in `deliverables/metrics.json` (n=400, depth=8, lr=0.05, subsample=0.9, colsample=0.8) matches manuscript Section 3.3 exactly.
- [WARN] RF call in notebook uses `max_depth=None` (manuscript says `max_depth=15`) and does not set `min_samples_leaf=3`. Manuscript description does not match the executed RF.
- [WARN] First XGB instantiation in notebook uses `n_estimators=400, colsample_bytree=0.9` (manuscript baseline says n=200, colsample=0.8). The displayed baseline call differs from manuscript; the tuned config (which is what was persisted) matches. Recommend reconciling baseline prose.
- [WARN] `most_frequent` imputation strategy named in manuscript is not literally present in the notebook (it uses `strategy='constant'` for categoricals). Functionally close but not identical to the prose.

### Task 7 - Citation drift
- [PASS] 29 distinct numeric inline citations (`[1]` through `[29]`) found in the manuscript text. `manuscripts/references.md` contains entries 1-29 in the same numbered scheme. No orphan citations. No unused references. (Note: brief calls for `reports/references.md`; this project stores them in `manuscripts/references.md` instead - flagged informationally, not a FAIL since references are present and complete.)

### Task 8 - CrossRef live re-verification (5 random refs)
Sample (seed=7) checked against `https://api.crossref.org/works/{doi}`:

- [PASS] 10.1023/A:1010933404324 - HTTP 200, title "Random Forests" (matches ref [1] Breiman 2001).
- [PASS] 10.3390/s24248219 - HTTP 200, title "Application of Machine Learning to Predict CO2 Emissions in Light-Duty Vehicles" (matches ref [12] Udoh et al. 2024).
- [PASS] 10.1016/j.tra.2018.02.002 - HTTP 200, title "How much difference in type-approval CO2 emissions from passenger cars in Europe..." (matches ref [18] Pavlovic et al. 2018).
- [PASS] 10.1038/s43247-025-02447-2 - HTTP 200, title "Battery electric vehicles show the lowest carbon footprints among passenger cars..." (matches ref [29] Simaitis et al. 2025).
- [PASS] 10.1038/s42256-019-0138-9 - HTTP 200, title "From local explanations to global understanding with explainable AI for trees" (matches ref [6] Lundberg et al. 2020).

5/5 resolved with title match.

### Task 9 - Em-dash scan
- [PASS] 0 em-dash characters across `notebooks/01_eda.ipynb`, `notebooks/03_modeling.ipynb`, `manuscripts/references.md`, `manuscripts/manuscript.md`, `deliverables/presentation.html`.

### Task 10 - AI-tell scan
- [PASS] 0 hits for `verified by N agents | AI-verified | cross-checked by Claude` across all project artefacts (recursive scan, excluding the three role output files).

### Task 11 - Checkpoint schema
- [WARN] `checkpoint.json` does not exist at project root. README "Status: in_eda" suggests an earlier-stage state file may have been intended; absence of the file is a missing-artefact warning, not a content failure.

### Project #1-#8 deliverables presence (additional check)
- [PASS] `deliverables/co2_xgboost.pkl` (saved tuned model, 2.5 MB) present.
- [PASS] `deliverables/metrics.json` (per-model train/val/test metrics, RF feature-importance top-15) present.
- [PASS] `deliverables/feature_importance_rf.png` and `deliverables/residuals_xgb_baseline.png` present.
- [PASS] `deliverables/presentation.html` (220 KB, self-contained except DOI hyperlinks) present.

## Blockers

None. CrossRef API responded for all 5 sampled DOIs.

## Role A complete
