# NIFTY 50 Quantitative Trading Engine 📈

A Full-Stack Quantitative Analysis system built with Python. It automates the entire workflow from data ingestion to Machine Learning based trade filtering.

---

## 🌟 Overview

This repository provides all the tools and methodology required for performing quantitative trading analysis specifically for the NIFTY 50 index. Using data-driven techniques, it offers robust features including regime detection, algorithmic trading, and AI-driven market signal filtering.

---

## 🚀 Features

- **Automated Data Pipeline:** Fetches NIFTY Spot & INDIA VIX data using `yfinance`.
- **Regime Detection:** Uses **Hidden Markov Models (HMM)** to classify market conditions (Bullish/Bearish/Sideways).
- **Algorithmic Trading:** Implements a vectorized EMA Crossover strategy.
- **ML Filtering:** Uses a **Random Forest Classifier** (Accuracy: ~56%) to filter false trading signals.
- **Anomaly Detection:** Statistical Z-Score analysis to identify market shocks.
- **Interactive Charts:** Leverages Matplotlib for detailed visualizations.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Libraries:** Pandas, NumPy, Scikit-Learn, HMMlearn, Matplotlib, Yfinance.
- **IDE Recommended:** VSCode/PyCharm.

---

## 📂 Project Structure

- `src/`: Source code for data, features, and strategy.
- `data/`: Storage for historical CSV data.
- `models/`: Saved Machine Learning models (`.pkl`).
- `plots/`: Generated analysis charts.

---

## ⚡ How to Run

To quickly replicate the project on your local machine:

1. **Clone the repository:**
  ```bash
  git clone https://github.com/Gauravmishra01/nifty-quant-project.git
  cd nifty-quant-project
  ```
2. **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
3. **Run the Data Pipeline:**
  ```bash
  python src/data_utils.py  # Download Data
  python src/features.py    # Generate Indicators
  python src/regime.py      # Detect Regimes
  python src/strategy.py    # Backtest Strategy
  python src/ml_models.py   # Train AI
  ```

---

## 📊 Results

Quantify your trading outcomes:

- **ML Model Accuracy:** 56%
- **Backtested Strategy Return:** 0.09% (over a 5-day test period).
- **Visual Insights:** Regime state transitions, Anomalous Movements, and Trading Entry/Exit points visualized.

---

## 🧩 Future Enhancements

- **Real-Time Streamlined Data Pipeline.**
- **Improve AI Model Accuracy (Current 56%.**)
- **Addition of new Machine strategies optimization!**
