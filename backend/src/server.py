from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import sys

# --- IMPORT YOUR ROBOT SKILLS ---
# We append the current directory to path to make sure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_utils import fetch_nifty_spot, fetch_india_vix, load_and_merge_data
    from features import calculate_technical_indicators
    from regime import detect_market_regimes
except ImportError as e:
    print(f"⚠️ Warning: Could not import modules. Error: {e}")

app = Flask(__name__)
CORS(app)

# Ensure data directory exists
DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATA_PATH = os.path.join(DATA_DIR, 'nifty_ready_to_trade.csv')

# --- HELPER: The "Self-Healing" Function ---
def run_pipeline():
    """Downloads data, calculates features, and saves the CSV."""
    print("🔄 Pipeline Started: Downloading fresh data...")
    
    # 1. Download (Fetches Max 60 Days)
    fetch_nifty_spot() # Uses the new function that gets 60d
    # Note: If you have a separate VIX fetcher, ensure it also gets 60d or matches the index
    # For this submission, relying on the generated data from data_utils is safest.
    
    # 2. Merge
    # We assume these files are saved to 'data/' by your fetch functions
    spot_path = os.path.join(DATA_DIR, "nifty_spot_5min.csv")
    
    # If you have VIX data, merge it. If not, we might skip merging or use a placeholder.
    # For now, we will proceed assuming the data_utils handles the creation of the files.
    
    # 3. Feature Engineering
    # We load the spot data we just downloaded
    if os.path.exists(spot_path):
        df = pd.read_csv(spot_path)
        
        # Calculate Technicals (RSI, EMA, etc.)
        df_features = calculate_technical_indicators(df)
        
        # Detect Regimes (AI)
        df_ready = detect_market_regimes(df_features)
        
        # 4. Save Final
        df_ready.to_csv(DATA_PATH, index=False)
        print("✅ Pipeline Complete: Data saved to disk.")
        return df_ready
    else:
        print("❌ Error: Spot data file not found after download.")
        return None

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
            
            # --- THE FIX: Send EVERYTHING (No .tail limit) ---
            # We fill NaNs with 0 to ensure JSON compatibility
            df_clean = df.copy().fillna(0)
            
            # Return the full dataset (records format is best for Recharts)
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
            return jsonify({"error": "Pipeline failed to generate data"}), 500
    except Exception as e:
        print(f"❌ Refresh Failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port)