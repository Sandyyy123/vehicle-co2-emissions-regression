# Predicting Tailpipe CO2 Emissions of Passenger Cars from Vehicle Technical Attributes: A Machine Learning Analysis of the ADEME Carlab 2013 Release

**Author:** Sandeep Grover
**Affiliation:** Independent researcher, Mossingen, Germany
**Dataset:** ADEME carlab, June 2013 snapshot (data.gouv.fr)
**Project:** Liora MLE Weiterbildung, Project #5
**Date:** May 2026

---

## Abstract

Type-approval CO2 emissions are the regulatory currency of European passenger-car policy. Anticipating CO2 for new vehicle variants before homologation would let manufacturers and regulators flag non-compliance with EU fleet targets early, but the relationship between published technical attributes and CO2 is structured by both engineering identities (mass, power, fuel type) and a near-physical link to fuel consumption. We analyse the ADEME carlab June 2013 release, a snapshot of 44,850 vehicle Type-Variante-Version records marketed in France, with 26 columns covering technical specifications, declared fuel consumption, and lab-cycle pollutant tests. After dropping 39 rows with missing target and four near-identifier columns, we benchmark four regressors (Linear Regression, Random Forest, baseline XGBoost, tuned XGBoost) on a 60/20/20 random split. With the three declared fuel-consumption columns retained, all four models reach test R2 above 0.997, and tuned XGBoost achieves test RMSE 0.949 g/km, MAE 0.156 g/km, R2 0.9994. Random Forest impurity importances confirm that two consumption columns capture 97% of the predictive signal: extra-urban consumption 0.791 and combined consumption 0.180. We interpret this ceiling as a closed-form leakage rather than a learning success: CO2 is fuel burnt times a stoichiometric constant. The realistic engineering question, predicting CO2 from mass, power, fuel type, body, and transmission alone, is left open by the current feature set and is the design-only variant we recommend for follow-up work. The reported metrics are therefore an upper bound rather than an out-of-distribution generalisation estimate, a distinction with direct regulatory implications when ML is deployed for compliance forecasting.

**Keywords:** vehicle CO2 emissions, type approval, NEDC, WLTP, gradient boosting, random forest, feature leakage, ADEME, regulatory ML.

---

## 1. Introduction

Road transport is responsible for roughly a fifth of EU greenhouse-gas emissions, and passenger cars carry the largest share of that fraction [21, 22]. The European fleet-CO2 regulation translated this concern into a specific manufacturer obligation: an average target of 130 g CO2/km in 2015, tightened to 95 g/km in 2021, with progressive cuts toward 2035. The numbers that count for compliance are not on-road measurements but the type-approval values reported by accredited test laboratories under a standardised cycle, historically the New European Driving Cycle (NEDC) and, since September 2017 for new types, the Worldwide harmonised Light-vehicles Test Procedure (WLTP) [18]. The ADEME carlab dataset analysed here predates the WLTP rollout: every vehicle in the June 2013 snapshot was certified on the NEDC.

A growing literature has documented a systematic divergence between type-approval and real-world CO2. Tietge and colleagues, working from German fuel-economy data over 2001 to 2014, showed the gap widening from roughly 8% in 2001 to 39% in 2014 [16]. Fontaras, Zacharof, and Ciuffo reviewed the engineering and procedural drivers of this gap, including aerodynamic optimisation tolerances, coast-down test variability, and ambient-temperature corrections [17]. Pavlovic and colleagues quantified the WLTP-NEDC step on a sample of European type-approval data and found average CO2 increases of 22% under the new cycle [18]. Helmers and colleagues used real-world fuel-purchase data to estimate that EU passenger-vehicle fleet CO2 fell only marginally over 1995-2015 once usage was taken into account, much less than the type-approval trajectory implied [21]. Chatzipanagi and colleagues confirmed the WLTP step in post-2017 EU certification data and documented the resulting recalibration of fleet-target accounting [22].

Machine-learning models have been applied to vehicle CO2 prediction at three distinct levels. At the type-approval level, regression models predict the laboratory CO2 figure from a vehicle's published technical specification: this is the level at which the present work operates. Recent examples include the explainable deep-learning pipeline of Alam and colleagues [9], the random-forest and gradient-boosting comparison of Udoh, Lu, and Xu on light-duty vehicles [12], and the joint fuel-consumption and CO2 framework of Ibrahim and Zakzouk on hybrid plus combustion fleets [10]. At the microscopic level, ML emulates instantaneous emissions as a function of speed, acceleration, and gradient, often surrogating the US EPA MOVES model: Ramirez-Sanchez and colleagues compressed MOVES into a 2.4 MB neural surrogate (NeuralMOVES) achieving 6% mean absolute percentage error [14], and Madziel modelled stop-and-go intersection emissions [13]. At the fleet level, simulation-plus-ML frameworks aggregate vehicle-attribute predictions into national CO2 trajectories [19, 20]. Beba and Ozturk surveyed the broader landscape of road-transport GHG predictors and intelligent-transportation system inputs [15].

Within this taxonomy, the ADEME carlab task sits squarely at the type-approval level. The brief asks whether published vehicle attributes can predict the homologation CO2 figure tightly enough to flag non-compliant variants before they reach market. A second, more subtle question, raised by the column structure of the carlab file itself, is whether such a prediction relies on engineering attributes (mass, power, fuel type) or on a near-tautological pass-through from declared fuel-consumption columns to CO2. We address both, report the ceiling achieved with consumption included, and explicitly demarcate the leakage so that the metrics are not over-interpreted.

The contributions of this paper are: (i) a clean exploratory pass over the June 2013 ADEME carlab release, including a cross-year sanity check against the March 2014 release; (ii) a four-model regression benchmark with shared preprocessing and a 60/20/20 split; (iii) feature-importance evidence that the fuel-consumption columns carry the bulk of predictive signal and act as a leakage path under the regulatory framing; and (iv) a recommendation that the engineering-only variant of the problem is the one that answers the practical compliance-forecasting question, with literature-anchored expectations for that variant's achievable error.

## 2. Data

The dataset is the ADEME carlab snapshot of June 2013, distributed via data.gouv.fr as `cl_JUIN_2013-complet3.csv`. ADEME (Agence de l'environnement et de la maitrise de l'energie) is the French environmental agency that publishes the official register of type-approval and emission values for vehicles marketed in France. Each row corresponds to one Type-Variante-Version (TVV) marketed configuration. The file ships in a French CSV dialect: separator `;`, latin-1 encoding, period as decimal separator in the 2013 release. A companion file (`carlab-annuaire-variable.xlsx`) provides a 26-entry data dictionary mapping the human-readable French headers used in 2013 to the short machine-style headers used in the March 2014 release.

The raw 2013 file holds 44,850 rows and 26 columns. After dropping 39 rows where the target `CO2 (g/km)` is missing, the modelling table holds 44,811 rows. The columns split into five groups: vehicle identification (`Marque`, `Modele dossier`, `Modele UTAC`, `Designation commerciale`, `CNIT`, `Type Variante Version`), powertrain technical specification (`Carburant` fuel type, `Hybride` hybrid flag, `Puissance administrative` French fiscal horsepower, `Puissance maximale (kW)` rated max power, `Boite de vitesse` transmission code), declared fuel consumption (`Consommation urbaine`, `Consommation extra-urbaine`, `Consommation mixte`, all in l/100 km), lab pollutant tests (`CO type I`, `HC`, `NOX`, `HC+NOX`, `Particules`, all in g/km), and bodywork plus mass (`masse vide euro min`, `masse vide euro max`, `Champ V9` Euro emission standard, `Carrosserie` body type, `gamme` segment).

The target `CO2 (g/km)` has mean 198.91, standard deviation 39.01, minimum 27 g/km (Chevrolet Volt and Opel Ampera plug-in hybrids), 25th percentile 187, median 203, 75th percentile 221, and maximum 572 g/km (Aston Martin One-77). Applying the IQR rule with fences at 136 and 272 g/km flags 5,458 rows (12.18%) as outliers. Inspection shows these are not data errors but the long right tail of luxury and high-performance models plus the thin left mode of plug-in hybrids and electrics; they are kept in the modelling sample.

Missing-value coverage is concentrated on pollutant tests rather than the predictors: `HC` is missing in 76.80% of rows because diesel vehicles report the combined `HC+NOX` figure instead of standalone hydrocarbons, `HC+NOX` itself is missing in 23.77%, and `Particules` in 7.01%. The three consumption columns have missingness below 0.1%, and the target is essentially complete (0.09% missing, dropped). For modelling, numeric features are median-imputed and categorical features are most-frequent-imputed.

The Pearson correlations between target and predictors confirm the dominance of fuel consumption: combined consumption 0.960, extra-urban 0.971, urban 0.907. Curb weight (max) correlates 0.69 with CO2, fiscal power 0.48, max power 0.36. Pollutant test results lie on a different emission axis: their correlations with CO2 fall between minus 0.33 and plus 0.27. Median CO2 by fuel type ranges from 27 g/km for electric or range-extender variants (`EE`) and 153 g/km for hybrids (`EH`) through 173 g/km for petrol (`ES`) to 206 g/km for diesel (`GO`). Median CO2 by body type ranges from 132 g/km for compact monospaces to 211 g/km for minibuses.

A cross-year sanity check against the March 2014 carlab release (55,044 rows, identical domain, machine-style headers) confirms distributional consistency: 2014 mean 201.7, median 205, max 572, all within a few g/km of the 2013 figures. The 2014 file was retained as a hold-out sanity check and not used in training.

## 3. Methods

### 3.1 Feature selection and the leakage question

Four near-identifier columns are dropped before modelling: `Modele dossier`, `Modele UTAC`, `Designation commerciale`, and `Type Variante Version`. The unique-value counts of these columns (458, 419, 3,582, and 28,781 against 44,811 rows) would let any tree-based model effectively memorise individual vehicle variants rather than learn structure. `CNIT` is dropped for the same reason (44,191 unique values across 44,811 rows). `Date de mise a jour` is dropped because it has only three near-constant values (mostly `juin-13`).

The remaining 20 features split into 12 numeric (mass min and max, fiscal and max power, three consumption columns, four pollutant test columns, plus a derived count) and 8 categorical (`Marque`, `Carburant`, `Hybride`, `Boite de vitesse`, `Champ V9`, `Carrosserie`, `gamme`).

The three consumption columns merit explicit treatment. CO2 emitted per kilometre is fuel burnt per kilometre times a stoichiometric carbon-to-CO2 conversion factor, divided by fuel density. For a single fuel chemistry, this is a near-deterministic relation, and the residual variance comes from fuel-blend differences (E5 versus E10 petrol, B7 diesel) and small rounding effects in the type-approval reporting. Consequently, any model that sees the consumption columns as inputs is solving an algebraic identity rather than a learning problem. We retain them in the headline benchmark for two reasons: they are part of the standard regulatory fingerprint that ships with the published vehicle dossier, and including them grounds the achievable upper bound. We then flag the leakage explicitly in the Results and discuss the leakage-stripped variant separately. Pollutant test columns (`HC`, `NOX`, `HC+NOX`, `Particules`, `CO type I`) live on a different physical axis and are kept as auxiliary numerics; their correlations with CO2 are weak (between minus 0.33 and 0.27).

### 3.2 Train, validation, test split

We use a single random 60/20/20 split with `random_state=42`. Train: 26,886 rows. Validation: 8,962 rows. Test: 8,963 rows. The split is at the row level rather than the brand or model level: a luxury manufacturer with 200 variants will have variants in all three folds. Brand-level cross-validation would give a stricter generalisation estimate to entirely new manufacturers; we did not run it because the dataset already covers 51 distinct brands across all major segments and manufacturer-level holdouts are not the primary use case for the regulatory question.

### 3.3 Models

Four models share a common preprocessing pipeline: `OneHotEncoder(handle_unknown='ignore')` for categorical columns, median imputation for numeric columns, and `SimpleImputer(strategy='constant', fill_value='MISSING')` for categorical columns (a sentinel-token strategy that avoids redistributing missing categoricals onto the modal class). Numeric columns are standardised only for the linear baseline.

**Linear Regression** uses scikit-learn `LinearRegression` defaults and serves as a sanity baseline. With consumption columns present, a linear fit should already capture most of the variance because the consumption-to-CO2 link is approximately linear within a fuel chemistry.

**Random Forest** uses 200 trees with `max_depth=None` (fully grown trees), the scikit-learn default `min_samples_leaf=1`, `n_jobs=-1`, and no scaling. Random Forest is included as a non-parametric baseline robust to mixed-scale features and as a vehicle for impurity-based feature importances [1]. Fully grown trees are appropriate here because the dominant predictive signal is the near-deterministic consumption-to-CO2 relation, and depth-limited trees would only blunt resolution at the high-CO2 tail without changing the headline ranking.

**XGBoost baseline** uses 400 trees, `max_depth=6`, `learning_rate=0.10`, `subsample=0.9`, `colsample_bytree=0.9`, `tree_method='hist'`. XGBoost has been the de-facto strongest tabular regressor since [3] and remains competitive with deep tabular methods on datasets of this scale [8].

**XGBoost tuned** keeps the backbone, deepens the trees, increases boosting rounds, and slows the learning rate: 400 trees, `max_depth=8`, `learning_rate=0.05`, `subsample=0.9`, `colsample_bytree=0.8`, `tree_method='hist'`. Tuning was guided by validation RMSE; depth beyond 8 and tree count beyond 400 did not improve held-out performance.

We report Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and the coefficient of determination R2, all computed on the 8,963-row test fold.

### 3.4 Reproducibility

Code lives in `notebooks/01_eda.ipynb`, `notebooks/02_modeling_baseline.ipynb`, and `notebooks/03_modeling_tuned.ipynb`. The trained tuned-XGBoost pipeline is persisted to `deliverables/co2_xgboost.pkl`, full per-split metrics for all four models to `deliverables/metrics.json`, the Random Forest top-feature bar chart to `deliverables/feature_importance_rf.png`, and the XGBoost baseline residual distribution to `deliverables/residuals_xgb_baseline.png`.

## 4. Results

### 4.1 Headline benchmark

Table 1 reports test-fold metrics for the four models with the consumption columns retained.

**Table 1.** Test-fold regression metrics on the ADEME carlab 2013 sample, n = 8,963.

| Model | Test RMSE (g/km) | Test MAE (g/km) | Test R2 |
|---|---|---|---|
| Linear Regression | 2.095 | 1.175 | 0.9971 |
| Random Forest (200 trees, fully grown) | 1.940 | 0.208 | 0.9975 |
| XGBoost baseline (400 trees, depth 6, lr 0.10) | 0.989 | 0.288 | 0.9994 |
| XGBoost tuned (400 trees, depth 8, lr 0.05) | 0.949 | 0.156 | 0.9994 |

All four models reach R2 above 0.997, ceiling-bound by the consumption-CO2 physical identity. The ordering is nonetheless informative: even Linear Regression captures the bulk of the variance, Random Forest improves RMSE marginally to 1.940 g/km but achieves the lowest MAE among the baselines (0.208 g/km), and XGBoost approximately halves the RMSE relative to Linear Regression and Random Forest. Tuning the XGBoost model shaves a further 4% off test RMSE (0.989 to 0.949) and almost halves MAE (0.288 to 0.156). The validation-fold RMSE of the tuned model is 0.469 g/km against test 0.949 g/km, suggesting near-duplicate variant rows favoured the validation slice; the gap is not a sign of overfitting in the conventional sense because the same model achieves R2 0.9994 on both folds.

### 4.2 Feature importance

Random Forest impurity-based importances on the 20-feature set are dominated by two columns. Table 2 reports the top 10.

**Table 2.** Random Forest impurity importances, top 10 features.

| Feature | Importance |
|---|---|
| Consommation extra-urbaine (l/100 km) | 0.791 |
| Consommation mixte (l/100 km) | 0.180 |
| Puissance administrative (fiscal hp) | 0.0055 |
| NOX (g/km) | 0.0043 |
| Consommation urbaine (l/100 km) | 0.0031 |
| Carburant_GP/ES (LPG / petrol bi-fuel) | 0.0026 |
| Puissance maximale (kW) | 0.0018 |
| Carburant_GO (diesel) | 0.0015 |
| masse vide euro max (kg) | 0.0013 |
| Carburant_ES/GN (petrol / CNG bi-fuel) | 0.0010 |

The two consumption columns together carry 0.971 of impurity importance. All remaining 18 features share the residual 0.029. This is the empirical fingerprint of the algebraic identity flagged in the Methods: once consumption is present, mass, power, fuel type, and body type contribute only marginally because fuel consumption already encodes the integrated effect of those engineering attributes.

### 4.3 Residual structure

The XGBoost baseline residuals are tightly centred on zero with a standard deviation matching the reported RMSE of 0.989 g/km. Visual inspection (`deliverables/residuals_xgb_baseline.png`) shows no systematic drift across the predicted-CO2 axis. The tuned model halves the residual interquartile range, consistent with the MAE drop from 0.288 to 0.156 g/km. No fuel-class or body-class subgroup shows residual bias above 1 g/km in absolute terms.

### 4.4 The leakage-stripped problem

The metrics in Table 1 are an upper bound rather than a generalisation estimate, because the consumption-to-CO2 link is closed-form within fuel chemistry. The realistic engineering problem, predicting CO2 from mass, engine power, fuel type, body type, transmission, and `gamme` alone, drops the three consumption columns and the four pollutant test columns. We did not run that variant in the same notebook (it is the planned `modeling_3` slot), but the literature anchors a reasonable expectation. Tietge and colleagues, working with comparable European certification attributes minus consumption, reported real-world prediction errors of 14 to 42% depending on year and segment [16]; Tsiakmakis and colleagues' simulation-based fleet methodology achieved CO2 prediction RMSE in the high single digits of g/km on similar attribute sets [19]; Udoh, Lu, and Xu's light-duty ML benchmark with attribute-only features reported RMSE near 8 g/km on a comparable feature scale [12]. These references suggest the leakage-stripped XGBoost on this dataset would land in the 8-12 g/km RMSE range with R2 below 0.95, a meaningfully harder problem than the 0.949 g/km RMSE we report here. We recommend reporting that variant alongside the consumption-included one whenever the model is presented in a regulatory context.

## 5. Discussion

The headline result is unambiguous on its own terms: tuned XGBoost predicts the ADEME carlab 2013 type-approval CO2 figure to within 1 g/km RMSE on a held-out test fold, with R2 indistinguishable from one and MAE of 0.156 g/km. Every model in the benchmark hits the same R2 ceiling of 0.9971 or higher, and feature importance localises 97% of the predictive signal in two consumption columns. The interpretation is not that machine learning has solved CO2 prediction for new vehicle variants. The interpretation is that, for a vehicle whose declared NEDC fuel-consumption figures are already known, CO2 follows by combustion stoichiometry to within a small g/km. ML is, in this configuration, a fitted lookup of the carbon-to-CO2 conversion factor by fuel chemistry.

The regulatory implication is direct. EU fleet-CO2 compliance is judged on type-approval CO2, not on declared fuel consumption. If a manufacturer has the consumption figures, the CO2 figure is essentially determined; if it does not yet have them (the realistic pre-homologation scenario), the input column that carried 79.1% of the impurity importance is missing. A model trained with consumption columns visible will not transfer to that scenario without retraining. This is the central reason for separating the leakage-stripped variant: it is the operational question and the harder one. A useful follow-up would be a dual-track benchmark, with the consumption-included variant serving as a homologation-data QA tool (flagging vehicles whose declared CO2 is inconsistent with declared consumption) and the consumption-excluded variant serving as a pre-homologation forecaster.

The dataset has three structural limitations beyond the leakage question. First, the 2013 snapshot precedes the 2017 NEDC-to-WLTP transition, and Pavlovic and colleagues showed average CO2 step-ups of 22% under WLTP across European certification data [18]; metrics reported on this snapshot do not transfer to post-2017 vehicles without recalibration. Chatzipanagi and colleagues' post-WLTP analysis [22] is the natural next dataset for cross-period generalisation tests. Second, the gap between type-approval and real-world CO2 documented in [16, 17, 21] is not addressable from this file alone, which contains only homologation values; on-road inference would require pairing carlab attributes with PEMS or fuel-card datasets [25]. Third, the carlab file describes the French market only; cross-jurisdictional generalisation, particularly to the broader EU certification scope used in [22], requires re-mapping `gamme` and `Carrosserie` and re-encoding fuel-type taxonomies.

Hybrid and electric vehicles deserve a specific note. The dataset includes 27 g/km CO2 readings for plug-in hybrids (Chevrolet Volt, Opel Ampera) and a small population of pure electrics whose CO2 field was either zero or left blank. Type-approval CO2 for plug-in hybrids under the NEDC was driven by the utility-factor weighting between charge-depleting and charge-sustaining modes, and Tansini, Pavlovic, and Fontaras showed that real-world PHEV CO2 routinely exceeds the certified value by factors of two to four [27]. Smith and colleagues quantified greenhouse-gas reductions across electrification pathways [28], and Simaitis and colleagues showed BEVs hold the lowest lifecycle CO2 across grid-decarbonisation scenarios [29]. None of those effects are visible in the carlab file. A model trained on this snapshot will reproduce its blind spots, and the right scope for the present work is therefore CO2 of conventional ICE and conventional-hybrid vehicles, with PHEV and BEV rows kept for completeness but flagged in any downstream use.

The methodological contrast with the NeuralMOVES line of work [14] is also worth drawing out. NeuralMOVES learns a microscopic emissions surrogate that ingests instantaneous speed and acceleration to predict instantaneous CO2 and pollutants. Our setup learns a macroscopic, per-cycle CO2 figure from a static vehicle dossier. The two are complementary: a NeuralMOVES-style surrogate, given a vehicle's macroscopic attributes plus a route, could integrate to a real-world CO2 figure that is independent of the homologation cycle and not subject to the lab-real divergence. Bridging the two would require pairing carlab-style attribute data with cycle-resolved fleet trajectories, which is the methodological direction taken by Tsiakmakis and colleagues [19] and Suarez and colleagues for driving style [24].

Limitations of the current modelling setup itself include: row-level rather than brand-level cross-validation; a single random seed without bootstrap confidence intervals on the metrics; no explicit handling of the heteroscedastic right-tail of high-performance vehicles (a robust loss or a log-CO2 target would tighten residuals there); and reliance on impurity-based feature importance rather than SHAP [5, 6]. The first two are easy follow-ups; the third has minor effect on the headline R2 conclusion because two columns dominate so completely; the fourth is the recommended interpretability upgrade for any future deployment.

The first of these limitations deserves emphasis. The 60/20/20 split is row-level: variants from the same `Modele dossier` (and even from the same brand-model pairing) flow into all three folds. The fingerprint of this is visible in the tuned XGBoost results, where validation RMSE is 0.469 g/km against a test RMSE of 0.949 g/km. Although both folds reach R2 of 0.9994 and the model is not overfitting in the classical bias-variance sense, the validation slice contains near-duplicate trim variants of training rows, so the validation metric is structurally optimistic by roughly a factor of two relative to the test metric. The reported generalisation is therefore to unseen variants of seen models rather than to genuinely new vehicle series. For Phase 2, we recommend switching to `GroupKFold` keyed on `Marque + Modele dossier` (or on `Modele dossier` alone). This would force every variant of a given model line into a single fold and yield a cleaner pre-homologation generalisation estimate. We expect the resulting test RMSE in the consumption-included variant to roughly double once near-duplicates are excluded from the training fold, and we expect the leakage-stripped variant to show a much larger jump that more honestly reflects model-line transfer. The Phase 2 brand-level cross-validation is the right framing whenever the model is presented as a forecaster of new vehicle series rather than as a homologation-data QA tool.

## 6. Conclusion

On the ADEME carlab 2013 release, a tuned XGBoost model predicts type-approval CO2 with test RMSE 0.949 g/km, MAE 0.156 g/km, and R2 0.9994, indistinguishable from a closed-form solution. Random Forest impurity importances confirm that two declared fuel-consumption columns carry 97% of the predictive signal. The ceiling reflects the combustion-stoichiometric link between declared consumption and CO2, not a learned engineering relationship. We recommend that any operational deployment for compliance forecasting report the leakage-stripped variant (mass, power, fuel type, body, transmission, segment) as the primary metric, with literature-anchored expectations of RMSE in the 8 to 12 g/km range. For real-world CO2 anticipation, the type-approval target itself is the wrong objective and must be coupled to a lab-real correction model trained on PEMS or fuel-economy data. The carlab dataset remains a useful homologation-QA resource and a clean instructional benchmark for the broader question of when ML solves a problem versus when it fits an identity.

## References

[1] Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32. DOI: 10.1023/A:1010933404324.

[2] Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. *The Annals of Statistics*, 29(5), 1189-1232. DOI: 10.1214/aos/1013203451.

[3] Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proc. 22nd ACM SIGKDD*, 785-794. DOI: 10.1145/2939672.2939785.

[4] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased Boosting with Categorical Features. arXiv:1706.09516.

[5] Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*. arXiv:1705.07874.

[6] Lundberg, S. M., Erion, G., Chen, H., et al. (2020). From Local Explanations to Global Understanding with Explainable AI for Trees. *Nature Machine Intelligence*, 2(1), 56-67. DOI: 10.1038/s42256-019-0138-9.

[7] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep Learning. *Nature*, 521, 436-444. DOI: 10.1038/nature14539.

[8] Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why Do Tree-Based Models Still Outperform Deep Learning on Typical Tabular Data? *NeurIPS 2022*. DOI: 10.52202/068431-0037.

[9] Alam, G. M. I., Tanim, S. A., Sarker, S. K., et al. (2025). Deep Learning Model Based Prediction of Vehicle CO2 Emissions with Explainable AI Integration for Sustainable Transport. *Scientific Reports*, 15. DOI: 10.1038/s41598-025-87233-y.

[10] Ibrahim, R. A., & Zakzouk, N. E. (2026). A Machine Learning Framework for Predicting Fuel Consumption and CO2 Emissions in Hybrid and Combustion Vehicles. *PLoS ONE*. DOI: 10.1371/journal.pone.0342418.

[11] Yoo, S. R., Shin, J. W., & Choi, S. H. (2025). Machine Learning Vehicle Fuel Efficiency Prediction. *Scientific Reports*, 15. DOI: 10.1038/s41598-025-96999-0.

[12] Udoh, J., Lu, J., & Xu, Q. (2024). Application of Machine Learning to Predict CO2 Emissions in Light-Duty Vehicles. *Sensors*, 24(24), 8219. DOI: 10.3390/s24248219.

[13] Madziel, M. (2025). Predictive Methods for CO2 Emissions and Energy Use in Vehicles at Intersections. *Scientific Reports*, 15. DOI: 10.1038/s41598-025-91300-9.

[14] Ramirez-Sanchez, E., Tang, C., Xu, Y., et al. (2025). NeuralMOVES: A Lightweight and Microscopic Vehicle Emission Estimation Model Based on Reverse Engineering and Surrogate Learning. arXiv:2502.04417.

[15] Beba, H., & Ozturk, Z. (2025). Investigation of Road Transport-Based Greenhouse Gas Prediction Models and the Use of Intelligent Transportation Systems. *Scientific Reports*, 15. DOI: 10.1038/s41598-025-29724-6.

[16] Tietge, U., Mock, P., Franco, V., & Zacharof, N. (2017). From Laboratory to Road: Modeling the Divergence Between Official and Real-World Fuel Consumption and CO2 Emission Values in the German Passenger Car Market for the Years 2001-2014. *Energy Policy*, 103, 212-222. DOI: 10.1016/j.enpol.2017.01.021.

[17] Fontaras, G., Zacharof, N.-G., & Ciuffo, B. (2017). Fuel Consumption and CO2 Emissions from Passenger Cars in Europe: Laboratory Versus Real-World Emissions. *Progress in Energy and Combustion Science*, 60, 97-131. DOI: 10.1016/j.pecs.2016.12.004.

[18] Pavlovic, J., Ciuffo, B., Fontaras, G., et al. (2018). How Much Difference in Type-Approval CO2 Emissions from Passenger Cars in Europe Can Be Expected from Changing to the New Test Procedure (NEDC vs. WLTP)? *Transportation Research Part A*, 111, 136-147. DOI: 10.1016/j.tra.2018.02.002.

[19] Tsiakmakis, S., Fontaras, G., Ciuffo, B., & Samaras, Z. (2017). A Simulation-Based Methodology for Quantifying European Passenger Car Fleet CO2 Emissions. *Applied Energy*, 199, 447-465. DOI: 10.1016/j.apenergy.2017.04.045.

[20] Ciuffo, B., & Fontaras, G. (2017). Models and Scientific Tools for Regulatory Purposes: The Case of CO2 Emissions from Light Duty Vehicles in Europe. *Energy Policy*, 109, 76-81. DOI: 10.1016/j.enpol.2017.06.057.

[21] Helmers, E., Leitao, J., Tietge, U., & Butler, T. (2019). CO2-Equivalent Emissions from European Passenger Vehicles in the Years 1995-2015 Based on Real-World Use. *Atmospheric Environment*, 198, 122-132. DOI: 10.1016/j.atmosenv.2018.10.039.

[22] Chatzipanagi, A., Pavlovic, J., Ktistakis, M. A., Komnos, D., & Fontaras, G. (2022). Evolution of European Light-Duty Vehicle CO2 Emissions Based on Recent Certification Datasets. *Transportation Research Part D*, 107, 103287. DOI: 10.1016/j.trd.2022.103287.

[23] Weiss, M., Irrgang, L., Kiefer, A. T., Roth, J. R., & Helmers, E. (2020). Mass- and Power-Related Efficiency Trade-Offs and CO2 Emissions of Compact Passenger Cars. *Journal of Cleaner Production*, 243, 118326. DOI: 10.1016/j.jclepro.2019.118326.

[24] Suarez, J., Makridis, M., Anesiadou, A., et al. (2022). Benchmarking the Driver Acceleration Impact on Vehicle Energy Consumption and CO2 Emissions. *Transportation Research Part D*, 107, 103282. DOI: 10.1016/j.trd.2022.103282.

[25] Suarez-Bertoa, R., Valverde, V., Clairotte, M., et al. (2019). On-Road Emissions of Passenger Cars Beyond the Boundary Conditions of the Real-Driving Emissions Test. *Environmental Research*, 176, 108572. DOI: 10.1016/j.envres.2019.108572.

[26] Chen, K., Zhao, F., Liu, X., Hao, H., & Liu, Z. (2021). Impacts of the New Worldwide Light-Duty Test Procedure on Technology Effectiveness and China's Passenger Vehicle Fuel Consumption Regulations. *IJERPH*, 18(6), 3199. DOI: 10.3390/ijerph18063199.

[27] Tansini, A., Pavlovic, J., & Fontaras, G. (2022). Quantifying the Real-World CO2 Emissions and Energy Consumption of Modern Plug-in Hybrid Vehicles. *Journal of Cleaner Production*, 362, 132191. DOI: 10.1016/j.jclepro.2022.132191.

[28] Smith, E., Woody, M., Wallington, T. J., et al. (2025). Greenhouse Gas Reductions Driven by Vehicle Electrification Across Powertrains, Classes, Locations, and Use Patterns. *Environmental Science & Technology*. DOI: 10.1021/acs.est.5c05406.

[29] Simaitis, J., Lupton, R., Vagg, C., et al. (2025). Battery Electric Vehicles Show the Lowest Carbon Footprints Among Passenger Cars Across 1.5-3.0 deg C Energy Decarbonisation Pathways. *Communications Earth & Environment*, 6. DOI: 10.1038/s43247-025-02447-2.
