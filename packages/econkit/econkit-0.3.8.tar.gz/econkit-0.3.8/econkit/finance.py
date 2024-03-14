## Stock ##
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

def stock(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
    """
    Download stock data, calculate returns, and return as a pandas DataFrame.
    The data is saved in a CSV file within a specified folder named 'Stocks'.

    Parameters:
    ticker_symbol: The stock symbol (e.g., 'AAPL').
    start_date: The start date in DD-MM-YYYY format (e.g., '01-01-2020').
    end_date: The end date in DD-MM-YYYY format (e.g., '31-12-2020').
    interval: The data interval. Valid intervals include '1d', '5d', '1wk', '1mo', '3mo'.
    """

    def convert_date_format(date_string):
        """
        Convert date from DD-MM-YYYY to YYYY-MM-DD format.
        """
        return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')

    start_date = convert_date_format(start_date)
    end_date = convert_date_format(end_date)

    # Download stock data from Yahoo Finance
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)

    # Calculate % growth of Adjusted Close price
    stock_data['Returns'] = stock_data['Adj Close'].pct_change()

    folder_name = "Stocks"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = f"{folder_name}/{ticker_symbol}_{interval}.csv"
    stock_data.to_csv(file_name)

    return stock_data


## Returns ##
import pandas as pd

def returns(data):
    """
    Calculate the percentage change for each numeric column in a DataFrame,
    except for the 'Date' column, and return a new DataFrame with the same headers.

    Parameters:
    - data: pandas DataFrame

    Returns:
    - pandas DataFrame with percentage changes for numeric columns
    """
    # Create a new DataFrame with the same headers as 'data'
    new_df = pd.DataFrame(columns=data.columns)

    # Copy the 'Date' column to the new DataFrame
    new_df['Date'] = data['Date']
    
    for column in data.columns:
        if column != 'Date' and pd.api.types.is_numeric_dtype(data[column]):
            new_df[column] = data[column].pct_change() * 100

    return new_df
    
## Weights ##
import pandas as pd
import numpy as np

def weights(stocks, extra):
    """
    Creates portfolios where each stock is fully weighted in one portfolio, 
    and additional portfolios have random weights.

    Parameters:
    stocks (pandas.DataFrame): DataFrame with stock returns.
    extra (int): Number of additional portfolios with random weights.

    Returns:
    pandas.DataFrame: A DataFrame with portfolio weights for each stock.
    """
    num_stocks = len(stocks.columns)
    total_portfolios = num_stocks + extra
    portfolio_names = [f'P{i+1}' for i in range(total_portfolios)]

    # Initialize DataFrame for weights
    weights_df = pd.DataFrame(index=stocks.columns, columns=portfolio_names)

    # Assign full weight to each stock in one portfolio
    for i, stock in enumerate(stocks.columns):
        weights_df.iloc[:, i] = 0
        weights_df.at[stock, f'P{i+1}'] = 1

    # Assign random weights for the additional portfolios
    for i in range(num_stocks, total_portfolios):
        random_weights = np.random.random(num_stocks)
        normalized_weights = random_weights / random_weights.sum()
        weights_df[f'P{i+1}'] = normalized_weights

    return weights_df

## Portfolios ##
import pandas as pd
import numpy as np

def annualize_metric(metric, periods_per_year):
    """Annualize a daily metric such as return or standard deviation."""
    return metric * np.sqrt(periods_per_year)

def portfolios(weights, returns, period='daily'):
    """
    Calculate the expected return and volatility of portfolios.

    :param weights: DataFrame containing the weights of each stock in each portfolio.
    :param returns: DataFrame containing the returns of each stock.
    :param period: String indicating the time period ('daily', 'weekly', 'monthly').
    :return: DataFrame with portfolio names, expected returns, and volatility.
    """
    periods_per_year = {'daily': 252, 'weekly': 52, 'monthly': 12}
    portfolio_returns = returns.dot(weights)

    # Calculate expected portfolio return and volatility
    expected_return = portfolio_returns.mean() * periods_per_year[period]
    volatility = portfolio_returns.std() * np.sqrt(periods_per_year[period])

    # Create a DataFrame for expected return and volatility
    portfolio_metrics = pd.DataFrame({
        'Portfolio': weights.columns,
        'Expected Returnc (%)': expected_return * 100,
        'Volatility (%)': volatility * 100
    })

    return portfolio_metrics.set_index('Portfolio')

# Example usage:
# Assuming weights_df is your weights DataFrame and returns_df is your returns DataFrame
# portfolios(weights_df, returns_df, 'daily')


