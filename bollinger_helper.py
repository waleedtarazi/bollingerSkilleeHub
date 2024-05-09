import numpy as np
import pandas as pd

# Upper/Lower bands
def bollinger_bands(data, window_size = 30):
    """
    Function to calculate Bollinger Bands for a given dataset.

    Parameters:
    - data: DataFrame containing stock data that contains 'Close' column.
    - window_size: Size of the window for calculating the moving average and STD.

    Returns:
    - DataFrame with 'upperBand' and 'lowerBand' columns added, representing the upper and lower Bollinger Bands.
    """
    simple_moving_avarage = data['Close'].rolling(window = window_size, ).mean()
    rolling_std = data['Close'].rolling(window = window_size).std()
    
    # add the two columns 
    data['upperBand'] = simple_moving_avarage + (2* rolling_std)
    data['lowerBand'] = simple_moving_avarage - (2* rolling_std)
    
    return data


# RSI 
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
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
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
def fetch_stock_data():
    """
    Function to fetch stock data from the right EndPoint

    Returns:
    - data: DataFrame containing stock data .
    """
    pass

# preprocessing the data 
def pre_processing_data(data):
    data = bollinger_bands(data)
    data = calculate_RSI(data)
    buy_price, sell_price = strategy(data)
    data['buy'] = buy_price
    data['sell'] = sell_price
    return data


    

