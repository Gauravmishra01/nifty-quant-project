import pandas as pd
import numpy as np

def run_strategy(df, initial_capital=100000):
    """
    Runs a simple EMA Crossover strategy and calculates PnL.
    """
    print("⚡ Running Backtest Strategy...")
    
    # 1. Generate Signals
    # Buy (1) when EMA_9 > EMA_21
    # Sell (-1) when EMA_9 < EMA_21
    df['signal'] = 0
    df.loc[df['ema_9'] > df['ema_21'], 'signal'] = 1
    df.loc[df['ema_9'] < df['ema_21'], 'signal'] = -1
    
    # "Position" is what we actually hold. 
    # If signal is 1, we hold +1 share. If -1, we hold -1 share.
    df['position'] = df['signal'].shift(1) # We enter trade on the NEXT candle after signal
    
    # 2. Calculate Returns
    # Market Return: (Price_Now - Price_Prev) / Price_Prev
    df['market_returns'] = df['Close'].pct_change()
    
    # Strategy Return: Position * Market Return
    # If I am Long (+1) and market goes up (+1%), I make +1%.
    # If I am Short (-1) and market goes down (-1%), I make +1%.
    df['strategy_returns'] = df['position'] * df['market_returns']
    
    # 3. Calculate Equity Curve (Money Growth)
    # cumprod() calculates cumulative compound interest
    df['equity_curve'] = initial_capital * (1 + df['strategy_returns']).cumprod()
    
    # 4. Calculate Performance Metrics
    total_return = df['equity_curve'].iloc[-1] - initial_capital
    return_pct = (total_return / initial_capital) * 100
    
    # Count trades (whenever position changes)
    trades = df['position'].diff().fillna(0).abs()
    num_trades = trades.sum()
    
    print("-" * 30)
    print(f"💰 INITIAL CAPITAL: ₹{initial_capital}")
    print(f"💰 FINAL EQUITY:    ₹{df['equity_curve'].iloc[-1]:.2f}")
    print(f"📈 TOTAL RETURN:    {return_pct:.2f}%")
    print(f"🔄 TOTAL TRADES:    {int(num_trades)}")
    print("-" * 30)
    
    # Save detailed trade log for analysis
    df.to_csv("results/backtest_results.csv", index=False)
    print("✅ Results saved to 'results/backtest_results.csv'")
    
    return df

if __name__ == "__main__":
    try:
        # Load the data prepared by the Regime Detection step
        data = pd.read_csv("data/nifty_ready_to_trade.csv")
        run_strategy(data)
    except FileNotFoundError:
        print("❌ Error: Run src/regime.py first!")