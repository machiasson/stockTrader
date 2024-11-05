import pandas as pd
import numpy as np
import json
from datetime import datetime

# Load historical data from JSON
def load_historical_data(symbol):
    with open(f"{symbol}_historical_data.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Backtest the Bollinger Bands strategy
def backtest_strategy(df, window=20, num_std_dev=2, initial_balance=100000):
    # Calculate Bollinger Bands
    df['Middle Band'] = df['Close'].rolling(window=window).mean()
    df['Upper Band'] = df['Middle Band'] + (df['Close'].rolling(window=window).std() * num_std_dev)
    df['Lower Band'] = df['Middle Band'] - (df['Close'].rolling(window=window).std() * num_std_dev)

    # Initialize signal and position columns
    df['Signal'] = 0
    df.loc[window:, 'Signal'] = np.where(df['Close'][window:] < df['Lower Band'][window:], 1, 0)  # Buy signal
    df.loc[window:, 'Signal'] = np.where(df['Close'][window:] > df['Upper Band'][window:], -1, df['Signal'][window:])  # Sell signal
    df['Position'] = df['Signal'].diff()

    # Initialize variables for backtesting
    balance = initial_balance
    shares = 0
    trade_log = []

    # Iterate through the DataFrame to simulate trades
    for index, row in df.iterrows():
        # Buy signal
        if row['Position'] == 1:  # Buy
            shares_to_buy = balance // row['Close']  # Buy as many shares as possible
            balance -= shares_to_buy * row['Close']
            trade_log.append({
                'Date': row['Date'],
                'Symbol': 'FNGU',
                'Action': 'BUY',
                'Price': row['Close'],
                'Shares': shares_to_buy,
                'Transaction Amount': shares_to_buy * row['Close'],
                'Gain/Loss': 0,
                'Balance': balance
            })
            shares += shares_to_buy

        # Sell signal
        elif row['Position'] == -1 and shares > 0:  # Sell
            balance += shares * row['Close']  # Sell all shares
            gain_loss = (shares * row['Close']) - (shares * row['Close'])  # Gain/Loss calculation
            trade_log.append({
                'Date': row['Date'],
                'Symbol': 'FNGU',
                'Action': 'SELL',
                'Price': row['Close'],
                'Shares': shares,
                'Transaction Amount': shares * row['Close'],
                'Gain/Loss': gain_loss,
                'Balance': balance
            })
            shares = 0

    # Final balance calculation
    if shares > 0:
        # If there are remaining shares, sell them at the last available price
        balance += shares * df['Close'].iloc[-1]
        trade_log.append({
            'Date': df['Date'].iloc[-1],
            'Symbol': 'FNGU',
            'Action': 'SELL (EOD)',
            'Price': df['Close'].iloc[-1],
            'Shares': shares,
            'Transaction Amount': shares * df['Close'].iloc[-1],
            'Gain/Loss': (shares * df['Close'].iloc[-1]) - (shares * df['Close'].iloc[-1]),
            'Balance': balance
        })

    # Convert trade log to DataFrame
    trade_log_df = pd.DataFrame(trade_log)

    # Calculate total gain/loss and returns
    total_gain_loss = balance - initial_balance
    total_return = (balance / initial_balance - 1) * 100

    # Calculate number of trading days
    trading_days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    annual_return = (1 + (total_return / 100)) ** (365 / trading_days) - 1
    annual_return *= 100  # Convert to percentage

    # Save trade log to CSV
    trade_log_df.to_csv('trade_log.csv', index=False)

    # Print results
    print(f"Total Gain/Loss: ${total_gain_loss:.2f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Annual Return: {annual_return:.2f}%")
    print(f"Final Balance: ${balance:.2f}")

# Main execution
if __name__ == "__main__":
    symbol = 'FNGU'
    df = load_historical_data(symbol)
    df['Date'] = pd.to_datetime(df['Date'])  # Convert Date to datetime
    df.sort_values('Date', inplace=True)  # Sort by Date
    backtest_strategy(df)
