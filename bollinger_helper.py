import io
import numpy as np
import matplotlib.pyplot as plt
import yfinance
from enum import Enum

class data_symbol(Enum):
    AAPL = 'AAPL'
    TATASTEEL = 'TATASTEEL.NS'


# Upper/Lower bands
# in this function we calculate the data
def bollinger_bands(data, window_size = 20):
    """
    Function to calculate Bollinger Bands for a given dataset.

    Parameters:
    - data: DataFrame containing stock data that contains 'Close' column.
    - window_size: Size of the window for calculating the moving average and STD.

    Returns:
    - DataFrame with 'upperBand' and 'lowerBand' columns added, representing the upper and lower Bollinger Bands.
    """
    simple_moving_avarage = data['Close'].rolling(window = window_size, min_periods = 1 ).mean()
    rolling_std = data['Close'].rolling(window = window_size, min_periods = 1).std()
    
    # add the two columns 
    print("the rolling std: \n")
    print(rolling_std)
    print("SMA is : \n")
    print(simple_moving_avarage)
    data['upperBand'] = simple_moving_avarage + 2 * rolling_std
    data['lowerBand'] = simple_moving_avarage - 2 * rolling_std
    
    return data,simple_moving_avarage
    


# RSI 
# create
def calculate_RSI(data, window = 10):
    """
    Function to calculate the Relative Strength Index (RSI) for agiven dataset.
    
    Parameters:
    - data: DataFrame containing stock data that contains 'Close' column.
    - window: Size of the window for calculating average gain and average loss.
    
    Returns:
    - DataFrame with 'RSI', 'overBought', and 'overSold' columns added, representing the RSI values
      and overbought/oversold thresholds respectively.
    """
    # calculate the change of price 
    delta = data['Close'].diff()
    
    # seperate the gain and loss in the data
    gain = delta.where(delta > 0, 0)
    loss = delta.where(delta < 0, 0)
    
    # calculate RS
    avg_gain = gain.rolling(window = window, min_periods = 1).mean()
    avg_loss = loss.rolling(window = window, min_periods = 1).mean()
    RS = avg_gain / avg_loss
    
    # calculate the RSI
    RSI = 100 - (100/1+RS)
    data['RSI'] = RSI
    data['overBought'] = 70
    data['overSold'] = 30
    return data

# Strategy
def strategy(data):
    """
    Trading strategy based on Bollinger Bands and RSI.

    Parameters:
    - data: DataFrame containing stock data with 'Close', 'lowerBand', 'RSI', 'overSold', 'upperBand', 'overBought'.

    Returns:
    - buy_price: List of buy prices. NaN is appended if no buy signal is generated.
    - sell_price: List of sell prices. NaN is appended if no sell signal is generated.
    """
    position = 0 
    buy_price = []  
    sell_price = []  

    for i in range(len(data)):
        
        # Buy signal conditions: Close price below lower Bollinger Band and RSI below oversold threshold
        if data['Close'][i] < data['lowerBand'][i] and data['RSI'][i] < data['overSold'][i] and position == 0:
            position = 1 
            buy_price.append(data['Close'][i])  
            sell_price.append(np.nan) 
            
        # Sell signal conditions: Close price above upper Bollinger Band and RSI above overbought threshold
        elif data['Close'][i] > data['upperBand'][i] and data['RSI'][i] > data['overBought'][i] and position == 1:
            position = 0 
            sell_price.append(data['Close'][i])  
            buy_price.append(np.nan)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)

    return buy_price, sell_price

# Get the Data
def fetch_stock_data(stock_symbol):
    """
    Function to fetch stock data from Yahoo Finance API.

    Returns:
    - data: DataFrame containing historical stock data for AAPL with a 1-hour timeframe.
    """
    # Fetch AAPL stock data with a 1-hour timeframe by using Yahoo Finance API
    stock = yfinance.Ticker(stock_symbol)

    
    # Adjust the period and interval as we needed
    data = stock.history(period="12mo",
                        )
    
    return data

# preprocessing the data 
def pre_processing_data(data):
    data = bollinger_bands(data)
    data = calculate_RSI(data)
    buy_price, sell_price = strategy(data)
    data['buy'] = buy_price
    data['sell'] = sell_price
    return data

def make_plot(data,SMA_close):
# plotting
    fix, ax = plt.subplots(figsize=(12,10))
    plt.title("Bolling Bands + RSI ")
    plt.ylabel("Price USD")
    plt.xlabel("Date")

    ax.plot(data['Close'], label='Close price', alpha=.6, color='blue')
    ax.plot(SMA_close, label='simple moving 20-window price', alpha=.8, color='black')
    ax.plot(data['upperBand'], label='Uppder Band', alpha=.4, color='red')
    ax.plot(data['lowerBand'], label='Lower Band', alpha=.4, color='green')

    # ax.fill_between(data.index, data['upperBand'], data['lowerBand'], color='grey')
    ax.scatter(data.index, data['buy'], label="buy", alpha=1, marker='^', color='green')
    ax.scatter(data.index, data['sell'], label="sell", alpha=1, marker="v", color='red')

    plt.legend()
    img_buf = io.BytesIO()
    plt.savefig('bollinger_bands.png')
    plt.close()
    return img_buf


def make_analysis(stock_symbol):
    data = fetch_stock_data(stock_symbol)
    data,SMA_close = bollinger_bands(data)
    data = calculate_RSI(data)
    buy_price, sell_price = strategy(data)
    data['buy'] = buy_price
    data['sell'] = sell_price
    # img_buffer = make_plot(data,SMA_close)
    return data
    # return img_buffer
    




    

