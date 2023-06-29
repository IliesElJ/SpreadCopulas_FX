# region imports
from AlgorithmImports import *
import datetime
import pandas as pd
import pickle
import numpy as np
from copulas.bivariate import Gumbel
from gumbel_copula import *
# endregion

            
class CryingBrownBat(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        
        # Set OANDA Brokerage
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)

        # List of forex pairs
        forex_pairs = ['CADUSD', 'CHFUSD', 'EURUSD', 'GBPUSD', 'JPYUSD', 'NZDUSD', 'AUDUSD']
        commodities = ['XAUUSD', 'XAGUSD', 'WTICOUSD', 'BCOUSD', 'CORNUSD', 'SOYBNUSD', 'XPDUSD', 'XPTUSD', 'NATGASUSD', 'SUGARUSD']


        # Add Forex data
        for pair in forex_pairs:
            self.AddForex(pair, Resolution.Hour)
        for pair in commodities:
            self.AddCfd(pair, Resolution.Hour)

        self.copula_series, self.ecdf_series, self.best_spread_series = load_copulas(self)

        self.Log('Successfully imported copulas from QC ObjectStore')
        self.Debug('Successfully imported copulas from QC ObjectStore')

    def OnData(self, data: Slice):

        # Get the current date
        current_time = self.Time

        current_copula, current_ecdfs, current_pair = get_current_month_data(self, self.copula_series, self.ecdf_series, self.best_spread_series, current_time)

        if pd.isna(current_copula) or pd.isna(current_ecdfs) or pd.isna(current_pair):
            self.Log("One or more of the current values (copula, ecdfs, pair) are nan.")
            return

        # Extract the tickers from the current pair
        ticker1, ticker2 = current_pair[0], current_pair[1]

        # Get the closing prices
        if ticker1 not in data.QuoteBars or ticker2 not in data.QuoteBars:
            return
        
        close_price1 = data.QuoteBars[ticker1].Close
        close_price2 = data.QuoteBars[ticker2].Close

        self.Log(f"Best spread at {current_time}: {current_pair}")
        self.Debug(f"Best spread at {current_time}: {current_pair}")

        # Apply the ECDFs
        u = current_ecdfs[0](close_price1)
        v = current_ecdfs[1](close_price2)

        # Calculate partial derivatives
        h_a = float(current_copula.partial_derivative(np.column_stack((u, v))))
        h_b = float(current_copula.partial_derivative(np.column_stack((v, u))))

        self.Log(f"Partial Derivative U: {h_a}, Partial Derivative V: {h_b}")
        self.Debug(f"Partial Derivative U: {h_a}, Partial Derivative V: {h_b}")

        # Defining the partial derivatives' thresholds to use 
        const = 0.1
        const_2 = 0.1
                
        # Check conditions and place orders
        if h_a < const and h_b > 1 - const:
            # Open long S1 and short S2
            self.SetHoldings(ticker1, 0.1)
            self.SetHoldings(ticker2, -0.1)
        elif h_a > 1 - const and h_b < const:
            # Open short S1 and long S2
            self.SetHoldings(ticker1, -0.1)
            self.SetHoldings(ticker2, 0.1)
        elif abs(h_a - 0.5) < const_2 and abs(h_b - 0.5) < const_2:
            # Close both positions
            self.Liquidate(ticker1)
            self.Liquidate(ticker2)

        return
