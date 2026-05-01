# Exploration Report 1 - Schema, Missing Values, Basic Stats

**Project:** 05 CO2 emissions by vehicles
**Track:** Data Analyst, difficulty 6/10
**Date:** 2026-05-01
**Notebook:** `notebooks/01_eda.ipynb` (executed end-to-end)

## 1. Problem statement (from `brief.pdf`)

Identifying the vehicles that emit the most CO2 matters because the technical characteristics behind those emissions can be flagged early. Predicting CO2 emission for new vehicle series before they reach market would allow regulators and manufacturers to anticipate non-compliance with EU fleet targets (e.g. 95 g/km, 2021).

The brief asks for three reports: an exploration / preprocessing report, a modeling report, and a final report. This document is exploration #1.

## 2. Source and dataset description

| Item | Value |
|------|-------|
| Origin | data.gouv.fr - "Emissions de CO2 et de polluants des vehicules commercialises en France" (carlab snapshot) |
| Files in `data/` | `carlab-mars-2013-complete.zip`, `carlab-mars-2014-complete.zip`, `carlab-annuaire-variable.xlsx` (variable dictionary, 26 entries) |
| Primary CSV | `cl_JUIN_2013-complet3.csv` (June 2013 snapshot) |
| Secondary CSV | `mars-2014-complete.csv` (March 2014 snapshot, used as cross-year sanity check) |
| Encoding | latin-1, separator `;` |
| Granularity | one row per vehicle Type-Variante-Version (TVV) marketed in France |

Both files describe the same domain (technical characteristics, fuel consumption, CO2 and pollutant emissions) but use different column naming conventions: 2013 uses human-readable French headers, 2014 uses short machine-style headers (`lib_mrq`, `cod_cbr`, `co2`, etc.). The Excel dictionary maps the 2014 names to definitions and units.

## 3. Shape

| Dataset | Rows | Columns | Notes |
|---------|------|---------|-------|
| 2013 (primary) | 44,850 | 26 | Loads cleanly, all numeric columns parsed as numbers |
| 2014 (secondary) | 55,044 | 26 (after dropping 4 trailing empty `Unnamed:` columns) | Fuel consumption stored with European decimals (`,`), parsed as `object` and needs conversion |

## 4. Schema with column types (2013, primary)

| # | Column | Dtype | n_unique | Role |
|---|--------|-------|----------|------|
| 1 | Marque | object | 51 | brand (categorical) |
| 2 | Modele dossier | object | 458 | dossier model name |
| 3 | Modele UTAC | object | 419 | UTAC test model name |
| 4 | Designation commerciale | object | 3,582 | trade name (high-cardinality, near-identifier) |
| 5 | CNIT | object | 44,191 | national ID code (effectively unique row key) |
| 6 | Type Variante Version (TVV) | object | 28,781 | type-variant-version code |
| 7 | Carburant | object | 13 | fuel type (ES, GO, EH, EE, GN, etc.) |
| 8 | Hybride | object | 2 | hybrid yes/no |
| 9 | Puissance administrative | int64 | 62 | French fiscal horsepower |
| 10 | Puissance maximale (kW) | float64 | 223 | rated max power |
| 11 | Boite de vitesse | object | 16 | gearbox code (M 6, A 5, A 7...) |
| 12 | Consommation urbaine (l/100km) | float64 | 204 | urban fuel consumption |
| 13 | Consommation extra-urbaine (l/100km) | float64 | 91 | extra-urban consumption |
| 14 | Consommation mixte (l/100km) | float64 | 135 | combined consumption |
| 15 | **CO2 (g/km)** | float64 | 264 | **target variable** |
| 16 | CO type I (g/km) | float64 | 593 | CO test result |
| 17 | HC (g/km) | float64 | 71 | hydrocarbon emissions |
| 18 | NOX (g/km) | float64 | 219 | NOx emissions |
| 19 | HC+NOX (g/km) | float64 | 180 | combined HC+NOx |
| 20 | Particules (g/km) | float64 | 16 | particulate emissions |
| 21 | masse vide euro min (kg) | int64 | 859 | min curb weight |
| 22 | masse vide euro max (kg) | int64 | 937 | max curb weight |
| 23 | Champ V9 | object | 13 | EURO emission standard |
| 24 | Date de mise a jour | object | 3 | update date (mostly `juin-13`) |
| 25 | Carrosserie | object | 10 | body type |
| 26 | gamme | object | 7 | vehicle range / segment |

## 5. Missing values

Only 10 columns of 26 carry any missing values. The pollutant test columns drive the bulk of the gaps; the target itself is essentially complete.

| Column | n_missing | % missing |
|--------|-----------|-----------|
| HC (g/km) | 34,447 | 76.80% |
| HC+NOX (g/km) | 10,659 | 23.77% |
| Particules (g/km) | 3,142 | 7.01% |
| CO type I (g/km) | 303 | 0.68% |
| NOX (g/km) | 303 | 0.68% |
| Champ V9 | 235 | 0.52% |
| Consommation urbaine (l/100km) | 42 | 0.09% |
| Consommation extra-urbaine (l/100km) | 42 | 0.09% |
| **CO2 (g/km)** | **39** | **0.09%** |
| Consommation mixte (l/100km) | 39 | 0.09% |

The very high HC missing rate is structural: HC alone is reported only on petrol vehicles, while diesel vehicles report the combined `HC+NOX` figure. Treating these two as alternative columns (one or the other populated by fuel type) will be cleaner than imputing HC for diesels.

The 39 rows with missing target will be dropped for modeling; they correspond mostly to electric variants where the CO2 field was left blank.

## 6. Target distribution: `CO2 (g/km)`

| Statistic | Value |
|-----------|-------|
| count (non-null) | 44,811 |
| mean | 198.91 g/km |
| std | 39.01 |
| min | 27 g/km (Chevrolet Volt, Opel Ampera, plug-in hybrids) |
| 25% | 187 |
| median | 203 |
| 75% | 221 |
| max | 572 g/km (Aston Martin One-77) |

**Outliers (IQR rule, fences [136, 272]):** 5,458 rows (12.18%) sit outside the fence. These are not data errors but a long right tail of high-performance and luxury vehicles (Aston Martin, top-trim Mercedes G-Class) plus a left tail of plug-in hybrids and electrics. They should be kept in modeling but flagged; a log or robust regression may help.

Distribution shape: roughly bell-shaped around 200 g/km with a heavy right tail and a thin left mode below 80 g/km (hybrids / electrics). A meaningful share of vehicles already sits below the EU 2021 fleet target of 95 g/km, mostly small diesels and hybrids.

## 7. Key observations

1. **Fuel consumption and CO2 are nearly collinear.** Pearson correlation with CO2: combined consumption 0.960, extra-urban 0.971, urban 0.907. This is a physics identity (CO2 is fuel burnt times a stoichiometric constant), so consumption columns cannot be treated as independent predictors. Two modeling regimes follow naturally: (a) "with consumption" - very strong baseline, useful for QA / interpolation, and (b) "design-only" - drop consumption, predict CO2 from mass, power, fuel type, body, transmission. Regime (b) is the one that answers the brief's question about anticipating emissions for new vehicle series.

2. **Mass and power matter, in that order.** Curb weight correlates 0.69 with CO2; max power 0.36; fiscal power 0.48. Mass is the cleaner mechanical predictor. A heavier vehicle needs more energy to move, so this is expected.

3. **Categorical splits are strong.** Median CO2 by fuel: gasoline (ES) 173 g/km vs diesel (GO) 206 g/km vs hybrid (EH) 153 g/km vs electric/range-extender (EE) near 27 g/km. Median CO2 by body: minibus 211, coupe 164, berline 138, monospace compact 132. Range (`gamme`): luxe 164, economique 112. These two features alone capture most of the between-segment variance.

4. **Pollutant tests are not predictors of CO2.** HC, NOx, particulates, CO type I have correlations between -0.33 and +0.27 with CO2. They live on a separate emission axis and should be excluded from the CO2 regressor (or kept only as auxiliary targets in a multi-output model).

5. **Identifier columns must be dropped.** `CNIT` (44,191 unique values across 44,850 rows), `TVV` (28,781), and `Designation commerciale` (3,582) are near-identifiers and would let a tree memorise the training set rather than learn structure.

## 8. Cross-year sanity check (March 2014)

| Statistic | June 2013 | March 2014 |
|-----------|-----------|------------|
| n | 44,811 | 55,010 |
| mean | 198.9 | 201.7 |
| std | 39.0 | 34.0 |
| min | 27 | 13 |
| median | 203 | 205 |
| max | 572 | 572 |

The two snapshots are distributionally consistent (mean shifts by ~3 g/km, medians within 2 g/km). The 2014 snapshot adds ~10k rows but the same domain is described, so concatenating the years after harmonising column names and fixing the European-decimal formatting is a viable extension for `02_features.ipynb`.

## 9. Failures and caveats

- The 2014 CSV declares `utf-8` in some byte-order marks but contains non-UTF-8 bytes in French model names; reading it requires `latin-1`.
- The 2014 CSV ends each line with a trailing semicolon, producing 4 empty `Unnamed:` columns that are dropped in code.
- Numeric columns in 2014 (`puiss_max`, `conso_*`, pollutant columns) use `,` as decimal separator and parse as `object`; conversion is deferred to the feature notebook.
- No file failed to load.

## 10. Next-step inputs for `exploration_2.md` and `exploration_3.md`

- Distributions for every numeric feature, log-CO2 transform check.
- Pairwise scatter and partial-correlation plots controlling for fuel type.
- Feature engineering: combined power-to-weight ratio, hybrid/EV indicator, EURO standard ordinal encoding, gearbox type vs ratio count split.
- Preprocessing pipeline draft: drop identifier columns, group rare fuel codes, one-hot or target-encode `Carburant` / `Carrosserie` / `gamme`, decide on imputation strategy for HC vs HC+NOX.
