from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import sys

# --- IMPORT YOUR ROBOT SKILLS ---
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
    
    # 1. Download
    fetch_nifty_spot(period="5d", interval="5m")
    fetch_india_vix(period="5d", interval="5m")
    
    # 2. Merge
    # Note: We assume these files are saved to 'data/' by your fetch functions
    spot_path = os.path.join(DATA_DIR, "nifty_spot_5m.csv")
    vix_path = os.path.join(DATA_DIR, "india_vix_5m.csv")
    
    # Run merge logic
    load_and_merge_data(spot_path, vix_path)
    
    # 3. Features & AI
    clean_path = os.path.join(DATA_DIR, "nifty_final_clean.csv")
    df = pd.read_csv(clean_path)
    df_features = calculate_technical_indicators(df)
    df_ready = detect_market_regimes(df_features)
    
    # 4. Save Final
    df_ready.to_csv(DATA_PATH, index=False)
    print("✅ Pipeline Complete: Data saved to disk.")
    return df_ready

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # --- THE FIX: If file is missing, create it! ---
        if not os.path.exists(DATA_PATH):
            print("📉 Data file missing. Auto-running pipeline...")
            run_pipeline()

        # Now load the file (it is guaranteed to exist now)
        df = pd.read_csv(DATA_PATH)
        df_recent = df.tail(100).copy().fillna(0)
        return jsonify(df_recent.to_dict(orient='records'))
        
    except Exception as e:
        print(f"❌ Error in get_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    print("🔄 Manual Refresh Triggered...")
    try:
        df_ready = run_pipeline()
        return jsonify({"message": "Data successfully updated!", "rows": len(df_ready)})
    except Exception as e:
        print(f"❌ Refresh Failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port)