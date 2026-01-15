import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_and_plot(df):
    """
    Detects outliers and plots the Strategy performance.
    """
    print("📊 Generating Analysis Plots...")
    
    # 1. Detect Outliers using Z-Score
    # (Value - Mean) / Standard_Deviation
    df['z_score'] = (df['returns'] - df['returns'].mean()) / df['returns'].std()
    
    # Define Outliers: Z-score > 2 or < -2 (2 Standard Deviations away)
    outliers = df[np.abs(df['z_score']) > 2]
    
    print(f"🔎 Found {len(outliers)} market anomalies (Outliers).")
    
    # 2. SETUP PLOT
    plt.figure(figsize=(15, 10))
    
    # --- Subplot 1: Price & Outliers ---
    plt.subplot(2, 1, 1) # 2 Rows, 1 Column, Plot #1
    plt.plot(df['Datetime'], df['Close'], label='NIFTY Price', color='blue', alpha=0.6)
    
    # Mark the anomalies with Red Dots
    plt.scatter(outliers['Datetime'], outliers['Close'], color='red', label='Anomaly', s=50, zorder=5)
    
    plt.title(f"NIFTY 50 Price with Anomalies (Z-Score > 2)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # --- Subplot 2: Strategy Equity Curve ---
    # We need to run strategy logic first if it's not saved in file, 
    # but since we are just plotting, let's assume we want to see Volatility here instead.
    plt.subplot(2, 1, 2) # Plot #2
    plt.plot(df['Datetime'], df['volatility'], label='Market Volatility', color='orange')
    plt.title("Market Volatility (Risk)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 3. Save Plot
    plt.savefig("plots/market_analysis.png")
    print("✅ Plot saved to 'plots/market_analysis.png'")

if __name__ == "__main__":
    try:
        # Load data
        data = pd.read_csv("data/nifty_ready_to_trade.csv")
        # Convert Datetime back to proper format (CSV loses it)
        data['Datetime'] = pd.to_datetime(data['Datetime'])
        
        analyze_and_plot(data)
    except FileNotFoundError:
        print("❌ Error: Run src/regime.py first!")