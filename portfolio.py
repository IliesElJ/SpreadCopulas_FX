#region imports
from AlgorithmImports import *
#endregion


def CloseAllPositions(self, ORDER_TYPE, orderEvent, symbol, verbose=True):

    try:
        openOrders = self.Transactions.GetOpenOrders()
        openLimitOrders = [order for order in openOrders if (order.Type == ORDER_TYPE and order.Symbol == symbol)]

        if len(openLimitOrders)> 0:
            for x in openLimitOrders:
                self.Transactions.CancelOrder(x.Id) 
                if verbose: self.Debug(f"{orderEvent}: canceling order {x.Tag}")
        
        return 0

    except Exception as e:
        self.Log(f"Exception {e} occured when canceling positions")
        return -1

def SanityCheck(limitPrice, takeProfit, stopLoss, short, self, verbose=False):

    if short:  snt = (limitPrice > takeProfit) and (limitPrice < stopLoss)
    else:   snt = (limitPrice < takeProfit) and (limitPrice > stopLoss)

    if verbose:
        self.Log(f"Sanity check: {snt}")

    return snt

def GetSessionDuration(Resolution_):
    if Resolution_ == Resolution.Hour:
        return 7
    elif Resolution_ == Resolution.Minute:
        return 6*60
