# Nifty 50 Quant Dashboard: AI-Driven Market Regime & Strategy Analysis

![Project Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Stack](https://img.shields.io/badge/Stack-MERN_%2B_Flask-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Live Demo
**[Click Here to View Dashboard](https://nifty-quant-project.vercel.app)**

> **⚠️ Important Note:** This project is hosted on **Render's Free Tier**.  
> If the chart does not load immediately, the server might be "sleeping" to save resources.  
> Please **wait 30-50 seconds** for the backend to wake up. The data will appear automatically once the server is active.

---

## 📌 Project Overview
This project implements an end-to-end **Quantitative Trading System** for the **Nifty 50 Index**. Unlike traditional strategies that rely solely on lagging indicators, this system utilizes **Hidden Markov Models (HMM)** and **AI-driven filtering** to enhance performance.

The core innovation is a **Machine Learning Filter (Random Forest)** that screens EMA Crossover signals based on market regimes and Volatility Index (VIX), significantly reducing "whipsaw" losses and enhancing returns.

### Key Features
- **Regime Detection:** Unsupervised learning (HMM) to classify market states (Trending vs. Choppy).
- **Self-Healing Data Pipeline:** Automated ETL system that recovers missing data in under 3 seconds during cloud restarts.
- **Full-Stack Dashboard:** Interactive Next.js frontend visualizing real-time signals, regimes, and backtest performance.
- **Synthetic Data Engineering:** Automatic Options and Futures data generation based on Black-Scholes and Cost-of-Carry models.

---

## 📂 Repository Structure
This repository follows a modular data science structure alongside the full-stack application code.

```text
├── data/                  # Raw and Processed Data Files
│   ├── nifty_spot_5min.csv
│   ├── nifty_futures_5min.csv
│   └── nifty_options_5min.csv
│
├── notebooks/             # Jupyter Notebooks for Research & Analysis
│   ├── 01_data_acquisition.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_regime_detection.ipynb
│   ├── 05_baseline_strategy.ipynb
│   ├── 06_ml_models.ipynb
│   └── 07_outlier_analysis.ipynb
│
├── src/                   # Core Python Modules (Backend Logic)
│   ├── data_utils.py      # Data fetching and synthetic generation
│   ├── features.py        # Technical indicators (RSI, EMA, Bollinger)
│   ├── greeks.py          # Option Greeks calculation
│   ├── regime.py          # HMM Model logic
│   ├── strategy.py        # Signal generation logic
│   ├── backtest.py        # Performance evaluation engine
│   └── ml_models.py       # Random Forest training and inference
│
├── models/                # Serialized Machine Learning Models
│   ├── hmm_model.pkl
│   └── rf_classifier.pkl
│
├── results/               # Backtest Outputs and Logs
│   ├── backtest_summary.csv
│   └── trade_log.json
│
├── plots/                 # Generated Visualizations
│   ├── equity_curve.png
│   ├── regime_overlay.png
│   └── confusion_matrix.png
│
├── requirements.txt       # Python Dependencies
└── README.md              # Project Documentation
```

---

## 🚀 Installation Instructions

### Prerequisites

- Python 3.9 or higher
- Node.js 18+ (for Frontend)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Gauravmishra01/nifty-quant-project.git
cd nifty-quant-project
```

### 2. Setup Backend (Python)
```bash
cd backend
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend (Next.js)
```bash
cd ../frontend
npm install
```

---

## ⚡ How to Run

### Option A: Run the Full Stack App (Localhost)
**Start Backend:**
```bash
# In terminal 1 (backend folder)
python src/server.py
```

**Start Frontend:**
```bash
# In terminal 2 (frontend folder)
npm run dev
```

**View the Dashboard:**  
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Option B: Run Research Notebooks
To explore the data analysis and model training steps:
```bash
# From the root directory
jupyter notebook
```
Navigate to the `notebooks/` folder and run them sequentially (01 to 07).

---

## 📊 Key Results Summary
The inclusion of the **AI-Driven Regime Filter** drastically improved the strategy's **risk-adjusted returns**, compared to traditional EMA crossover strategies. Performance metrics include:

- **Sharpe Ratio:** Increased from 1.2 to 2.8
- **Max Drawdown Reduction:** 18%
- **Signal Accuracy:** Improved by 12.5%

Generated reports are available in the `results/` folder, and visualization images are in the `plots/` folder.

---

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
