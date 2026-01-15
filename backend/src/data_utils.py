import yfinance as yf
import pandas as pd
import os

def fetch_nifty_spot(period="60d", interval="5m"):
    """Downloads NIFTY 50 Spot data."""
    print(f"Downloading NIFTY data (Period: {period}, Interval: {interval})...")
    ticker = "^NSEI"
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    
    if data.empty:
        print("❌ Error: No NIFTY data found.")
        return None
    
    data.reset_index(inplace=True)
    # Fix column names if they are multi-level
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    
    os.makedirs("data", exist_ok=True)
    data.to_csv(f"data/nifty_spot_{interval}.csv", index=False)
    print(f"✅ NIFTY saved. Rows: {len(data)}")
    return data

def fetch_india_vix(period="60d", interval="5m"):
    """Downloads INDIA VIX data."""
    print(f"Downloading INDIA VIX (Period: {period}, Interval: {interval})...")
    ticker = "^INDIAVIX"
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    
    if data.empty:
        print("❌ Error: No VIX data found.")
        return None
    
    data.reset_index(inplace=True)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
        
    data.to_csv(f"data/india_vix_{interval}.csv", index=False)
    print(f"✅ VIX saved. Rows: {len(data)}")
    return data

def load_and_merge_data(spot_file, vix_file):
    """Merges Spot and VIX into one file."""
    print("Merging data...")
    if not os.path.exists(spot_file) or not os.path.exists(vix_file):
        print("❌ Error: Files not found. Run downloads first.")
        return

    spot = pd.read_csv(spot_file)
    vix = pd.read_csv(vix_file)
    
    # Convert dates
    spot['Datetime'] = pd.to_datetime(spot['Datetime'], utc=True)
    vix['Datetime'] = pd.to_datetime(vix['Datetime'], utc=True)
    
    # Merge
    merged = pd.merge(spot, vix, on='Datetime', how='inner', suffixes=('', '_vix'))
    merged.ffill(inplace=True)
    
    output_file = "data/nifty_final_clean.csv"
    merged.to_csv(output_file, index=False)
    print(f"✅ MERGE SUCCESS! Final Data saved to {output_file}")
    print(f"   Total Rows: {len(merged)}")

if __name__ == "__main__":
    # 1. Download Both
    fetch_nifty_spot(period="5d", interval="5m")
    fetch_india_vix(period="5d", interval="5m")
    
    # 2. Merge
    load_and_merge_data("data/nifty_spot_5m.csv", "data/india_vix_5m.csv")