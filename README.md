![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Regression](https://img.shields.io/badge/task-regression-yellowgreen) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

# Vehicle CO2 Emissions Regression

Predicts CO2 emissions (g/km) from vehicle technical specifications using gradient boosting regression with full feature analysis.

---

## Task

**Regression**

---

## Architecture

```
Vehicle Specs CSV → Feature Engineering → XGBoost Regressor → Residual Analysis → Policy Insights
```

---

## Key Features

- CO2 (g/km) prediction from engine size, cylinders, fuel type, transmission
- Polynomial and interaction features for non-linear emission effects
- Fuel type comparison (gasoline, diesel, ethanol, hybrid)
- Residual analysis and prediction intervals
- Regulatory context: EU Fleet CO2 targets under EC Regulation 2019/631

---

## Dataset

[EU Vehicle CO2 Emissions (Kaggle / EC dataset)](https://www.kaggle.com/datasets/debajyotipodder/co2-emission-by-vehicles)

---

## Project Structure

```
├── src/
│   ├── model_baseline.py      # Baseline model
│   └── model_advanced.py      # Advanced model
├── notebooks/
│   └── 01_EDA.ipynb           # Exploratory analysis
├── manuscripts/
│   └── manuscript.md          # IMRaD writeup
├── reports/
│   └── references.md          # Verified references
├── deliverables/
│   └── presentation.html      # Self-contained HTML
├── data/
│   └── README.md              # Dataset download instructions
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/Sandyyy123/vehicle-co2-emissions-regression.git
cd vehicle-co2-emissions-regression
pip install -r requirements.txt

# See data/README.md for dataset download
jupyter notebook notebooks/01_eda.ipynb
# or run modeling:
jupyter notebook notebooks/03_modeling.ipynb
python src/model_advanced.py
```

---

## Tech Stack

`scikit-learn · XGBoost · pandas · matplotlib`

---

## Author

**Dr. Sandeep Grover** — PhD Data Science, independent ML researcher, Mössingen, Germany.

---

## License

MIT
