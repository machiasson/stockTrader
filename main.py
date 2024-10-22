import yfinance as yf
import json
from datetime import datetime


# Define the stock symbols and date range
stock_symbols = ['FNGU', 'FNGD']
start_date = '2021-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')  # Today's date


# Function to fetch historical data
def fetch_historical_data(symbol, start, end):
    stock_data = yf.download(symbol, start=start, end=end)
    return stock_data


# Fetch data for both symbols and store in a dictionary
data = {}
for symbol in stock_symbols:
    historical_data = fetch_historical_data(symbol, start_date, end_date)
    # Convert the DataFrame to a list of dictionaries with specific fields
    # Convert Timestamps to strings
    data[symbol] = historical_data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()
    data[symbol]['Date'] = data[symbol]['Date'].dt.strftime('%Y-%m-%d')  # Convert to string format
    data[symbol] = data[symbol].to_dict(orient='records')
   
    # Save each symbol's data to a separate JSON file
    output_file = f'{symbol}_historical_data.json'
    with open(output_file, 'w') as f:
        json.dump(data[symbol], f, indent=4)


    print(f"Data for {symbol} saved to {output_file}")