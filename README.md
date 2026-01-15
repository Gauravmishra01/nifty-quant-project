# NIFTY 50 Quantitative Trading Engine 📈

A Full-Stack Quantitative Analysis system built with Python. It automates the entire workflow from data ingestion to Machine Learning based trade filtering.

## 🚀 Features

- **Automated Data Pipeline:** Fetches NIFTY Spot & INDIA VIX data using `yfinance`.
- **Regime Detection:** Uses **Hidden Markov Models (HMM)** to classify market conditions (Bullish/Bearish/Sideways).
- **Algorithmic Trading:** Implements a vectorized EMA Crossover strategy.
- **ML Filtering:** Uses a **Random Forest Classifier** (Accuracy: ~56%) to filter false trading signals.
- **Anomaly Detection:** Statistical Z-Score analysis to identify market shocks.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Libraries:** Pandas, NumPy, Scikit-Learn, HMMlearn, Matplotlib, Yfinance.

## 📂 Project Structure

- `src/`: Source code for data, features, and strategy.
- `data/`: Storage for historical CSV data.
- `models/`: Saved Machine Learning models (`.pkl`).
- `plots/`: Generated analysis charts.

## ⚡ How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Pipeline:**
    ```bash
    python src/data_utils.py  # Download Data
    python src/features.py    # Generate Indicators
    python src/regime.py      # Detect Regimes
    python src/strategy.py    # Backtest Strategy
    python src/ml_models.py   # Train AI
    ```

## 📊 Results

- **ML Accuracy:** 56%
- **Strategy Return:** 0.09% (5-Day Test Period)
