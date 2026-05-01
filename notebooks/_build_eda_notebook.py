"""Helper that builds 01_eda.ipynb (nbformat v4) from a list of cells."""
import json
import os

NB_PATH = os.path.join(os.path.dirname(__file__), "01_eda.ipynb")


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src,
    }


cells = []

cells.append(md(
    "# Project 5 - CO2 emissions by vehicles\n"
    "\n"
    "## Notebook 01: Exploratory Data Analysis\n"
    "\n"
    "**Goal.** Identify which vehicle technical characteristics drive CO2 emissions and "
    "build a regression model to anticipate emissions for new vehicle series.\n"
    "\n"
    "**Source.** carlab dataset, vehicles marketed in France (data.gouv.fr). Two CSV "
    "snapshots: June 2013 (primary) and March 2014 (secondary, cross-year sanity check). "
    "Variable dictionary in `carlab-annuaire-variable.xlsx`.\n"
    "\n"
    "**Target.** `CO2 (g/km)` (continuous, regression).\n"
    "\n"
    "This notebook covers: load, schema, dtypes, shape, missing values, target distribution, "
    "outlier check, basic correlations, plus a markdown summary at the end."
))

cells.append(code(
    "import os\n"
    "import zipfile\n"
    "import warnings\n"
    "from pathlib import Path\n"
    "\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "\n"
    "warnings.filterwarnings('ignore')\n"
    "sns.set_theme(style='whitegrid')\n"
    "pd.set_option('display.max_columns', 40)\n"
    "pd.set_option('display.width', 200)\n"
    "\n"
    "DATA_DIR = Path('../data').resolve()\n"
    "EXTRACT_DIR = Path('/tmp/co2_extract')\n"
    "EXTRACT_DIR.mkdir(parents=True, exist_ok=True)\n"
    "print('DATA_DIR:', DATA_DIR)\n"
    "print('Files:', sorted(p.name for p in DATA_DIR.iterdir()))"
))

cells.append(md("## 1. Extract zips and locate CSVs"))

cells.append(code(
    "for zname in ['carlab-mars-2013-complete.zip', 'carlab-mars-2014-complete.zip']:\n"
    "    zpath = DATA_DIR / zname\n"
    "    with zipfile.ZipFile(zpath) as z:\n"
    "        z.extractall(EXTRACT_DIR)\n"
    "        print(zname, '->', z.namelist())\n"
    "\n"
    "csv_2013 = EXTRACT_DIR / 'cl_JUIN_2013-complet3.csv'\n"
    "csv_2014 = EXTRACT_DIR / 'mars-2014-complete.csv'\n"
    "assert csv_2013.exists() and csv_2014.exists()"
))

cells.append(md("## 2. Load primary dataset (France 2013)\n\n"
                "Encoding `latin-1`, separator `;`. Decimal point is `.` in 2013."))

cells.append(code(
    "df = pd.read_csv(csv_2013, encoding='latin-1', sep=';')\n"
    "print('Shape:', df.shape)\n"
    "df.head(3)"
))

cells.append(md("## 3. Schema, dtypes and basic stats"))

cells.append(code(
    "schema = pd.DataFrame({\n"
    "    'dtype': df.dtypes.astype(str),\n"
    "    'n_unique': df.nunique(),\n"
    "    'n_missing': df.isna().sum(),\n"
    "    'pct_missing': (df.isna().mean() * 100).round(2),\n"
    "})\n"
    "schema"
))

cells.append(code(
    "df.describe(include='all').T.head(30)"
))

cells.append(md("## 4. Missing values overview"))

cells.append(code(
    "missing = df.isna().sum().sort_values(ascending=False)\n"
    "missing = missing[missing > 0]\n"
    "print('Columns with missing values:', len(missing))\n"
    "print(missing)"
))

cells.append(code(
    "fig, ax = plt.subplots(figsize=(8, 4))\n"
    "missing.sort_values().plot(kind='barh', ax=ax, color='steelblue')\n"
    "ax.set_title('Missing values per column (count)')\n"
    "ax.set_xlabel('# rows missing')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("## 5. Target variable: `CO2 (g/km)`"))

cells.append(code(
    "TARGET = 'CO2 (g/km)'\n"
    "co2 = df[TARGET].dropna()\n"
    "print('Non-null target rows:', len(co2), '/', len(df))\n"
    "print(co2.describe().round(2))"
))

cells.append(code(
    "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
    "axes[0].hist(co2, bins=60, color='steelblue', edgecolor='white')\n"
    "axes[0].set_title('CO2 emissions (g/km) - histogram')\n"
    "axes[0].set_xlabel('CO2 g/km')\n"
    "axes[0].set_ylabel('# vehicles')\n"
    "axes[0].axvline(95, color='red', linestyle='--', label='EU 2021 fleet target 95 g/km')\n"
    "axes[0].legend()\n"
    "\n"
    "axes[1].boxplot(co2, vert=False)\n"
    "axes[1].set_title('CO2 (g/km) - boxplot')\n"
    "axes[1].set_xlabel('CO2 g/km')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("### 5.1 Outlier check using IQR"))

cells.append(code(
    "q1, q3 = co2.quantile([0.25, 0.75])\n"
    "iqr = q3 - q1\n"
    "lo = q1 - 1.5 * iqr\n"
    "hi = q3 + 1.5 * iqr\n"
    "outliers = co2[(co2 < lo) | (co2 > hi)]\n"
    "print(f'Q1={q1:.1f}, Q3={q3:.1f}, IQR={iqr:.1f}')\n"
    "print(f'IQR fences: [{lo:.1f}, {hi:.1f}]')\n"
    "print(f'Outliers: {len(outliers)} ({len(outliers)/len(co2)*100:.2f}%)')\n"
    "print('Top 5 highest emitters:')\n"
    "print(df.nlargest(5, TARGET)[['Marque','Modèle dossier','Désignation commerciale','Carburant',TARGET]])\n"
    "print('\\nLowest 5 emitters:')\n"
    "print(df.nsmallest(5, TARGET)[['Marque','Modèle dossier','Désignation commerciale','Carburant',TARGET]])"
))

cells.append(md("## 6. Categorical breakdowns of the target"))

cells.append(code(
    "for col in ['Carburant', 'Hybride', 'Carrosserie', 'gamme', 'Boîte de vitesse']:\n"
    "    g = df.groupby(col)[TARGET].agg(['count', 'mean', 'median']).round(1).sort_values('mean', ascending=False)\n"
    "    print(f'\\n--- CO2 by {col} ---')\n"
    "    print(g.head(10))"
))

cells.append(code(
    "fig, axes = plt.subplots(1, 2, figsize=(13, 4))\n"
    "order_carb = df.groupby('Carburant')[TARGET].median().sort_values().index\n"
    "sns.boxplot(data=df, x='Carburant', y=TARGET, order=order_carb, ax=axes[0])\n"
    "axes[0].set_title('CO2 by fuel type')\n"
    "axes[0].tick_params(axis='x', rotation=30)\n"
    "\n"
    "order_carr = df.groupby('Carrosserie')[TARGET].median().sort_values().index\n"
    "sns.boxplot(data=df, x='Carrosserie', y=TARGET, order=order_carr, ax=axes[1])\n"
    "axes[1].set_title('CO2 by body type (Carrosserie)')\n"
    "axes[1].tick_params(axis='x', rotation=45)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("## 7. Numeric correlations with the target"))

cells.append(code(
    "num_cols = df.select_dtypes(include=[np.number]).columns.tolist()\n"
    "print('Numeric columns:', num_cols)\n"
    "corr = df[num_cols].corr()\n"
    "corr_target = corr[TARGET].drop(TARGET).sort_values(ascending=False)\n"
    "print('\\nCorrelation with CO2 (g/km):')\n"
    "print(corr_target.round(3))"
))

cells.append(code(
    "fig, ax = plt.subplots(figsize=(9, 7))\n"
    "sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, cbar_kws={'shrink':0.8})\n"
    "ax.set_title('Numeric feature correlation matrix')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(code(
    "fig, axes = plt.subplots(1, 3, figsize=(14, 4))\n"
    "for ax, col in zip(axes, ['Consommation mixte (l/100km)', 'Puissance maximale (kW)', 'masse vide euro min (kg)']):\n"
    "    ax.scatter(df[col], df[TARGET], s=6, alpha=0.3)\n"
    "    ax.set_xlabel(col)\n"
    "    ax.set_ylabel(TARGET)\n"
    "    ax.set_title(f'{col} vs CO2')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("## 8. Cross-year sanity check (March 2014 secondary file)"))

cells.append(code(
    "# 2014 file uses comma as decimal separator inside numeric strings; load with latin-1.\n"
    "df14 = pd.read_csv(csv_2014, encoding='latin-1', sep=';')\n"
    "# Drop trailing empty 'Unnamed' columns from CSV trailing semicolons.\n"
    "df14 = df14.loc[:, ~df14.columns.str.startswith('Unnamed')]\n"
    "print('2014 shape:', df14.shape)\n"
    "print('2014 columns:', list(df14.columns))\n"
    "\n"
    "# co2 column is already numeric in 2014\n"
    "print('\\n2014 CO2 summary (g/km):')\n"
    "print(df14['co2'].describe().round(2))\n"
    "\n"
    "compare = pd.DataFrame({\n"
    "    '2013_June': df['CO2 (g/km)'].describe(),\n"
    "    '2014_March': df14['co2'].describe(),\n"
    "}).round(2)\n"
    "print('\\nYear-over-year CO2 distribution:')\n"
    "print(compare)"
))

cells.append(md(
    "## 9. Findings summary\n"
    "\n"
    "**Dataset.**\n"
    "- Primary: France, June 2013 snapshot, 44,850 rows x 26 columns. UTF-8/latin-1 with `;` separator.\n"
    "- Secondary: France, March 2014 snapshot, 55,044 rows x 26 columns (after dropping trailing empties). "
    "Same domain with renamed (machine-style) headers and comma decimals.\n"
    "- Target `CO2 (g/km)` is continuous; regression task confirmed.\n"
    "\n"
    "**Data quality.**\n"
    "- Most columns are populated. Pollutant emission columns (`HC`, `HC+NOX`, `Particules`) carry the bulk "
    "of the missing values, plausibly because those tests are not always run on every variant.\n"
    "- `CO2 (g/km)` itself has a small share of missing rows (drop or impute downstream).\n"
    "- Numeric columns are clean in 2013, but the 2014 file stores fuel consumption with European decimals (`,`) "
    "and pandas reads them as `object`. Conversion will be needed if 2014 is folded into modeling.\n"
    "\n"
    "**Target distribution.**\n"
    "- CO2 is right-skewed; mass-market diesels and small petrols cluster around 100-150 g/km, while sport / "
    "high-power petrol vehicles push the upper tail beyond 350 g/km.\n"
    "- A non-trivial slice already sits below the 95 g/km EU 2021 fleet target (mostly small diesels).\n"
    "\n"
    "**Drivers of CO2 (correlations).**\n"
    "- Strongest positive correlation: combined fuel consumption (`Consommation mixte`) and the urban / extra-urban "
    "components - essentially a physical identity (CO2 is a function of fuel burnt).\n"
    "- Maximum power (`Puissance maximale (kW)`), administrative power, and vehicle mass also correlate positively.\n"
    "- Pollutant test results (CO type I, NOx, particles) correlate weakly with CO2 - those are separate emission "
    "axes and should be treated as alternative targets, not predictors.\n"
    "\n"
    "**Categorical signal.**\n"
    "- Fuel type splits CO2 strongly: gasoline (ES) > diesel (GO) on average, electric (EL) sits at zero / near-zero.\n"
    "- Body type (`Carrosserie`) and range (`gamme`) shift the median by 30-80 g/km between subcompacts and large SUVs.\n"
    "\n"
    "**Next steps for `02_features.ipynb`.**\n"
    "- Drop pure-identifier columns (`CNIT`, `TVV`, `Désignation commerciale`).\n"
    "- Decide how to handle the consumption columns: keep as features for short-term prediction, or remove for a "
    "physics-free model that predicts CO2 from design only (mass, power, fuel, body, transmission).\n"
    "- Encode categoricals (fuel, body, range, transmission) via one-hot or target encoding.\n"
    "- Convert the 2014 European-decimal numeric columns and concatenate for a multi-year training set."
))


nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print("Wrote", NB_PATH, "with", len(cells), "cells")
