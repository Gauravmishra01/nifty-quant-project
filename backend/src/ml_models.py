import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_ml_model(df):
    """
    Trains a Random Forest to predict if the price will go UP in the next 5 candles.
    """
    print("🧠 Training Machine Learning Model...")
    
    # 1. Create the "Target" (What we want to predict)
    # We want to know: Will price be higher 5 candles from now?
    # shift(-5) looks 5 rows into the future.
    df['future_close'] = df['Close'].shift(-5)
    
    # Target = 1 if Future Price > Current Price, else 0 (Binary Classification)
    df['target'] = (df['future_close'] > df['Close']).astype(int)
    
    # Drop the last 5 rows (because they don't have a 'future_close')
    df_clean = df.dropna().copy()
    
    # 2. Select Features (The inputs for the AI)
    # We use the indicators we built earlier
    features = ['rsi', 'volatility', 'regime', 'ema_9', 'ema_21', 'returns']
    
    X = df_clean[features]  # Input
    y = df_clean['target']  # Output (Target)
    
    # 3. Split Data (80% for training, 20% for testing)
    # We don't want the AI to memorize the answers, so we hide 20% of data to test it later.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    # 4. Train the Brain (Random Forest)
    # n_estimators=100 means we ask 100 "decision trees" to vote
    model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Test the Brain
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print("-" * 30)
    print(f"🎯 Model Accuracy: {accuracy:.2%}")
    print("-" * 30)
    print("Detailed Report:")
    print(classification_report(y_test, predictions))
    
    # Show Feature Importance (What did the AI care about most?)
    importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    print("\n🔍 What matters most to the AI?")
    print(importances)
    
    return model

if __name__ == "__main__":
    try:
        # Load the ready-to-trade data
        data = pd.read_csv("data/nifty_ready_to_trade.csv")
        train_ml_model(data)
    except FileNotFoundError:
        print("❌ Error: Run src/regime.py first!")