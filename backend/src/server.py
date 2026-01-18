from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import sys

# --- 1. SETUP PATHS ---
# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- 2. STRICT IMPORTS ---
# We import directly. If these fail, the server will log the specific error.
from data_utils import fetch_nifty_spot
from features import calculate_technical_indicators
# from regime import detect_market_regimes # (Uncomment if you have this file working)

app = Flask(__name__)
CORS(app)

# Ensure data directory exists
DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATA_PATH = os.path.join(DATA_DIR, 'nifty_ready_to_trade.csv')

# --- HELPER: The "Self-Healing" Function ---
def run_pipeline():
    print("🔄 Pipeline Started: Downloading fresh data...")
    
    # 1. Download Data (Max 60 Days)
    df = fetch_nifty_spot()
    
    if df is None or df.empty:
        print("❌ Error: Failed to fetch spot data.")
        return None

    # 2. Calculate Features
    print("📊 Calculating Indicators...")
    try:
        df_features = calculate_technical_indicators(df)
    except Exception as e:
        print(f"❌ Error in Feature Engineering: {e}")
        return None

    # 3. (Optional) Detect Regimes
    # If you have the regime file, use it here. 
    # For now, we will add a default regime to prevent errors.
    if 'regime' not in df_features.columns:
        df_features['regime'] = 0 
    
    # 4. Save Final
    df_features.to_csv(DATA_PATH, index=False)
    print("✅ Pipeline Complete: Data saved to disk.")
    return df_features

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # 1. Self-Healing: If file is missing, create it!
        if not os.path.exists(DATA_PATH):
            print("📉 Data file missing. Auto-running pipeline...")
            run_pipeline()

        # 2. Load the data
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)
            
            # Send EVERYTHING (No .tail limit)
            df_clean = df.copy().fillna(0)
            return jsonify(df_clean.to_dict(orient='records'))
        else:
             return jsonify({"error": "Data could not be generated."}), 500
        
    except Exception as e:
        print(f"❌ Error in get_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    print("🔄 Manual Refresh Triggered...")
    try:
        df_ready = run_pipeline()
        if df_ready is not None:
            return jsonify({"message": "Data successfully updated!", "rows": len(df_ready)})
        else:
            return jsonify({"error": "Pipeline failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port)