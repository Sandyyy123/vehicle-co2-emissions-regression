# Project 5 — CO2 emissions by vehicles

**Track:** Data Analyst · **Difficulty:** 6/10 · **Status:** in_eda

## Goal

Identify which vehicle technical characteristics drive CO2 emissions, and build a predictive model that anticipates emissions for new vehicle series before they reach market.

## Datasets

| Source | Scope | Size | Use |
|--------|-------|------|-----|
| [data.gouv.fr - Émissions CO2 et polluants 2013](https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/) | French market 2013 (passenger cars) | ~2 MB | Primary dataset |
| [EEA - CO2 cars emission monitoring](https://www.eea.europa.eu/data-and-maps/data/co2-cars-emission-20) | All EU new cars yearly | 1+ GB per year | Secondary, for cross-year trends |

## Target variable

`co2_emissions_g_per_km` (continuous, regression task).

## Deliverables (Liora full format)

Per-brief minimum is 3 reports, but treated as a full DS-style deliverable:

- [ ] `reports/exploration_1.md` — schema, missing values, basic stats
- [ ] `reports/exploration_2.md` — distributions, correlations, target analysis, viz
- [ ] `reports/exploration_3.md` — feature engineering hypotheses, preprocessing plan
- [ ] `reports/modeling_1.md` — baseline (linear regression)
- [ ] `reports/modeling_2.md` — tree-based (Random Forest, XGBoost, LightGBM)
- [ ] `reports/modeling_3.md` — final model, error analysis, feature importance
- [ ] `reports/architecture.md` — data flow, batch scoring design, model serving notes
- [ ] `reports/final_report.md` — executive summary, findings, business impact, demo

## Notebooks

- [ ] `notebooks/01_eda.ipynb`
- [ ] `notebooks/02_features.ipynb`
- [ ] `notebooks/03_modeling.ipynb`
- [ ] `notebooks/04_evaluation.ipynb`

## Demo / artifacts

- [ ] Streamlit dashboard or static HTML report with predictions
- [ ] Model card (`deliverables/model_card.md`)
- [ ] Final report PDF

## Open questions

1. French 2013 only or pan-EU multi-year? Start with 2013, extend if time.
2. Problem framing: regression on g/km vs classification (low/mid/high emitter buckets)? Default = regression.
3. Compliance angle: any link to EU CO2 fleet targets (95 g/km 2021)? Add as discussion in final report.
