import yfinance as yf
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# Define the stock symbols and date range
stock_symbols = ['FNGU', 'FNGD']
start_date = '2021-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')  # Today's date


# Function to fetch historical data
def fetch_historical_data(symbol, start, end):
    stock_data = yf.download(symbol, start=start, end=end)
    return stock_data

class Window:

    def __init__(self):
        # Initialize tkinter
        self.root = tk.Tk()
        self.root.geometry("500x500")

        # Selection box for symbols
        self.selectionBox = ttk.Combobox(state="readOnly", values=stock_symbols)
        self.selectionBox.place(x=10, y=50)

        #Display start and end dates
        self.start_label = tk.Label(self.root, text="Start Date: " + start_date)
        self.end_label = tk.Label(self.root, text="End date: " + end_date)
        self.start_label.place(x=10,y=10)
        self.end_label.place(x=10, y=30)

        # Loop for tkinter
        self.root.mainloop()

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
    Window()