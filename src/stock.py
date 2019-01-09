
from datetime import datetime, timedelta
from math import isnan

import logging
import os
import pandas as pd

data = [ 
    {'Stock Symbol': 'TEA', 'Type': 'Common', 'Last Dividend': 0, 'Fixed Dividend': '', 'Par Value': 100},
    {'Stock Symbol': 'POP', 'Type': 'Common', 'Last Dividend': 8, 'Fixed Dividend': '', 'Par Value': 100},
    {'Stock Symbol': 'ALE', 'Type': 'Common', 'Last Dividend': 23, 'Fixed Dividend': '', 'Par Value': 60},
    {'Stock Symbol': 'GIN', 'Type': 'Preferred', 'Last Dividend': 8, 'Fixed Dividend': 0.02, 'Par Value': 100},
    {'Stock Symbol': 'JOE', 'Type': 'Common', 'Last Dividend': 13, 'Fixed Dividend': '', 'Par Value': 250}]

trade_book = []

logging.basicConfig(filename=os.path.join(os.path.split(os.getcwd())[0], "stock.log"), format='%(asctime)s | %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Stock_Exchange(object):
    """
    Sample stock exchange class
    """
    def __init__(self):
        self.df = pd.DataFrame(data)

    def calculate_dividend(self, price, stock_symbol):
        """
        Calculates Dividend Yield for stock symbol using its given price.
        :param price: Price of the stock
        :type price: Integer

        :param stock_symbol: Stock Symbol
        :type stock_symbol: String

        :returns: Dividend yield
        """
        logger.debug(' ************** Calculate Dividend ************** ')
        div_yield = 0.0
        calc_type = self.df[(self.df['Stock Symbol'] == stock_symbol)]['Type']
        last_dividend = self.df[(self.df['Stock Symbol'] == stock_symbol)]['Last Dividend']
        fixed_dividend = self.df[(self.df['Stock Symbol'] == stock_symbol)]['Fixed Dividend']
        par_val = self.df[(self.df['Stock Symbol'] == stock_symbol)]['Par Value']
        if price > 0:
            if str(calc_type.iloc[0]) == 'Preferred':
                if not isnan(fixed_dividend):
                    div_yield = (float(float(fixed_dividend)) * float(par_val))/price
            else:
                div_yield = float(last_dividend)/price
        logger.info("For price %s and stock symbol %s dividend yield is %s" %(price, stock_symbol, div_yield))
        return div_yield

    def calculate_pe(self, price, stock_symbol):
        """
        Calculates P/E ratio
        :param price: Price of the stock
        :type price: Integer

        :param stock_symbol: Stock Symbol
        :type stock_symbol: String

        :returns: P/E Ratio
        """
        logger.debug(' ************** Calculate P/E Ratio ************** ')
        pe_ratio = 0
        last = self.df[(self.df['Stock Symbol'] == stock_symbol)]['Last Dividend']
        if float(last) > 0:
            pe_ratio = price/float(last)
        logger.info("For price %s and stock symbol %s P/E Ratio is %s" %(price, stock_symbol, pe_ratio))
        return pe_ratio

    def register_trade(self, price, stock_symbol, quantity, trade_type):
        """
        Registers new trade information
        :param price: Price of the stock
        :type price: Integer

        :param stock_symbol: Stock Symbol
        :type stock_symbol: String
        
        :param quantity: Quantity
        :type quantity: Integer

        :param trade_type: Trade type-Buy or Sell
        :type trade_type: String
        """
        logger.debug(' ************** Register Trade ************** ')
        trade_book.append([stock_symbol, price, quantity, trade_type, datetime.now()])
        logger.info("New trade registered for stock symbol %s with trade type %s is %s" %(stock_symbol, trade_type, trade_book))

    def volume_weight_stock_price(self, stock_symbol):
        """
        Calculates volume weighted stock price
        :param stock_symbol: Stock Symbol
        :type stock_symbol: String
        
        :returns: Volume Weighted Stock Price
        """
        logger.debug(' ************** Calculate Volume weight stock price ************** ')
        vol_weighted_stock_price = 0
        self.df = pd.DataFrame(trade_book)
        timediff = datetime.now() - timedelta(minutes=5)
        if not self.df.empty:
            filtered_df = self.df[
                (self.df[0] == stock_symbol) & (self.df[4] < datetime.now()) & (self.df[4] > timediff)]
            sum_of_price = filtered_df[1].sum()
            sum_of_quantity = filtered_df[2].sum()
            vol_weighted_stock_price = (sum_of_price * sum_of_quantity) / sum_of_quantity
        logger.info("For stock symbol %s Volume weighted stock price is %s" %(stock_symbol, vol_weighted_stock_price))
        return vol_weighted_stock_price

    def geometric_mean(self):
        """
        Calculates Geometric mean of given 5 stock symbols in the table
        :returns: Geometric Mean
        """
        logger.debug(' ************** Calculate Geometric Mean ************** ')
        tea = self.volume_weight_stock_price('TEA')
        pop = self.volume_weight_stock_price('POP')
        ale = self.volume_weight_stock_price('ALE')
        gin = self.volume_weight_stock_price('GIN')
        joe = self.volume_weight_stock_price('JOE')
        all_vwsp_prod = tea * pop * ale * gin * joe
        geometric_mean = all_vwsp_prod**(1/5)
        logger.info("Geometric mean for all stock symbols is %s" %geometric_mean)
        return geometric_mean


if __name__ == '__main__':
    se = Stock_Exchange()
    # Given any price as input, calculate the dividend yield
    se.calculate_dividend(15, 'TEA')
    se.calculate_dividend(5, 'POP')
    se.calculate_dividend(5, 'ALE')
    se.calculate_dividend(10, 'GIN')
    se.calculate_dividend(0, 'JOE')
    
    # Given any price as input, calculate the P/E Ratio
    se.calculate_pe(10, 'TEA')
    se.calculate_pe(5, 'POP')
    se.calculate_pe(5, 'ALE')
    se.calculate_pe(10, 'GIN')    
    se.calculate_pe(0, 'JOE')
    
    # Trade
    se.register_trade(2, 'TEA', 20, 'S')
    se.register_trade(1, 'POP', 5, 'B')
    se.register_trade(3, 'ALE', 15, 'B')
    se.register_trade(5, 'GIN', 10, 'B')
    se.register_trade(2, 'GIN', 10, 'S')
    se.register_trade(5, 'JOE', 2, 'B')

    # Volume weighted stock price
    se.volume_weight_stock_price('TEA')
    se.volume_weight_stock_price('JOE')
    
    # Geometric mean 
    se.geometric_mean()
    se = None
