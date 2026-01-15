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

DATA_PATH = os.path.join(os.getcwd(), 'data', 'nifty_ready_to_trade.csv')

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        if not os.path.exists(DATA_PATH):
             return jsonify({"error": "Data file not found."}), 404

        df = pd.read_csv(DATA_PATH)
        df_recent = df.tail(100).copy().fillna(0)
        return jsonify(df_recent.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- NEW: THE REFRESH TRIGGER ---
@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    print("🔄 Refresh Triggered from Frontend...")
    try:
        # 1. Download New Data
        fetch_nifty_spot(period="5d", interval="5m")
        fetch_india_vix(period="5d", interval="5m")
        
        # 2. Merge & Clean
        merged_file = "data/nifty_final_clean.csv"
        # We need to reconstruct the paths exactly as data_utils expects them
        load_and_merge_data("data/nifty_spot_5m.csv", "data/india_vix_5m.csv")
        
        # 3. Calculate Math Features
        df = pd.read_csv(merged_file)
        df_features = calculate_technical_indicators(df)
        
        # 4. Detect Regimes (AI)
        df_ready = detect_market_regimes(df_features)
        
        # 5. Save Final
        df_ready.to_csv(DATA_PATH, index=False)
        
        print("✅ Data Pipeline Complete!")
        return jsonify({"message": "Data successfully updated!", "rows": len(df_ready)})
        
    except Exception as e:
        print(f"❌ Pipeline Failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Cloud providers give a PORT via environment variables
    # If we are local, we use 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    # host='0.0.0.0' is required for cloud access
    app.run(host='0.0.0.0', port=port)
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)