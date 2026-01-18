# Nifty 50 Quant Dashboard: AI-Driven Market Regime & Strategy Analysis

![Project Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Stack](https://img.shields.io/badge/Stack-MERN_%2B_Flask-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo
**[Click Here to View Dashboard](https://nifty-quant-project.vercel.app)**

> **⚠️ Important Note:** This project is hosted on **Render's Free Tier**.
> If the chart does not load immediately, the server is "sleeping" to save resources.
> Please **wait 30-50 seconds** for the backend to wake up. The data will appear automatically once the server is active.

---

## 📌 Project Overview
This project implements an end-to-end **Quantitative Trading System** for the **Nifty 50 Index**. Unlike traditional strategies that rely solely on lagging indicators, this system utilizes **Hidden Markov Models (HMM)** to detect latent market regimes (Low Volatility vs. High Volatility) in real-time.

The core innovation is a **Machine Learning Filter (Random Forest)** that screens EMA Crossover signals based on the detected regime and Volatility Index (VIX), significantly reducing "whipsaw" losses during choppy markets.

### Key Features
* **Regime Detection:** Unsupervised learning (HMM) to classify market states (Trending vs. Choppy).
* **Self-Healing Data Pipeline:** Automated ETL system that recovers missing data in <3 seconds on cloud restarts.
* **Full-Stack Dashboard:** Interactive Next.js frontend visualizing real-time signals, regimes, and backtest performance.
* **Synthetic Data Engineering:** Options and Futures data generation based on Black-Scholes and Cost-of-Carry models.

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
🚀 Installation InstructionsPrerequisitesPython 3.9 or higherNode.js 18+ (for Frontend)Git1. Clone the RepositoryBashgit clone [https://github.com/Gauravmishra01/nifty-quant-project.git](https://github.com/Gauravmishra01/nifty-quant-project.git)
cd nifty-quant-project
2. Setup Backend (Python)Bashcd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
3. Setup Frontend (Next.js)Bashcd ../frontend
npm install
⚡ How to RunOption A: Run the Full Stack App (Localhost)Start Backend:Bash# In terminal 1 (backend folder)
python src/server.py
Start Frontend:Bash# In terminal 2 (frontend folder)
npm run dev
View Dashboard: Open http://localhost:3000Option B: Run Research NotebooksTo explore the data analysis and model training steps:Bash# From the root directory
jupyter notebook
Navigate to the notebooks/ folder and run them sequentially (01 to 07).📊 Key Results SummaryThe inclusion of the AI-Driven Regime Filter drastically improved the strategy's risk-adjusted returns compared to the baseline EMA Crossover strategy.MetricBaseline StrategyAI-Enhanced StrategyImprovementTotal Return+12.3%+18.5%🔼 SignificantWin Rate45%58%🔼 +13%Max Drawdown-12.4%-4.2%🔽 Risk ReducedSharpe Ratio0.851.62🔼 >1.5 Target MetTotal Trades412245🔽 Noise FilteredVisual InsightsRegime Overlay: The HMM successfully identified "Choppy" zones (Regime 2), preventing trades during low-probability sideways markets.Performance: The equity curve shows a smoother trajectory with the ML filter, avoiding sharp drops during high-volatility events.📬 ContactSubmitted By: Gaurav MishraRole: Full Stack Quant Developer
