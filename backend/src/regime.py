import pandas as pd
import numpy as np
from hmmlearn.hmm import GaussianHMM
import joblib

def detect_market_regimes(df, n_states=3):
    """
    Uses Hidden Markov Models (HMM) to find market regimes.
    Updated to be more robust against 'Positive Definite' errors.
    """
    print("🤖 Training AI to detect Market Regimes...")
    
    df_clean = df.dropna().copy()
    
    # FIX 1: Scale the data so numbers aren't too small
    # We multiply by 100 to make them "percentages" (e.g., 0.01 becomes 1.0)
    # This helps the math solver avoid crashing.
    X = df_clean[['returns', 'volatility']].values * 100
    
    # FIX 2: Use covariance_type="diag" instead of "full"
    # "diag" is much more stable for financial data
    # min_covar=0.001 adds a tiny bit of "noise" to prevent divide-by-zero errors
    model = GaussianHMM(n_components=n_states, 
                        covariance_type="diag", 
                        n_iter=100, 
                        random_state=42,
                        min_covar=0.001)
    
    # Train
    model.fit(X)
    
    # Predict
    hidden_states = model.predict(X)
    
    # Add to dataframe
    df_clean['regime'] = hidden_states
    
    # Save model
    joblib.dump(model, "models/hmm_model.pkl")
    
    print(f"✅ Regimes Detected! Found {n_states} distinct market moods.")
    print(df_clean['regime'].value_counts())
    
    return df_clean

if __name__ == "__main__":
    try:
        data = pd.read_csv("data/nifty_features.csv")
        data_with_regime = detect_market_regimes(data)
        
        data_with_regime.to_csv("data/nifty_ready_to_trade.csv", index=False)
        print("✅ SUCCESS: Data saved to 'data/nifty_ready_to_trade.csv'")
    except Exception as e:
        print(f"❌ Error: {e}")