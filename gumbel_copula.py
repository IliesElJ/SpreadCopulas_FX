#region imports
from AlgorithmImports import *
#endregion
import numpy as np
import pickle
from copulas.bivariate import Gumbel


def load_copulas(qb):

    test = Gumbel()

    # Import the series from the Object Store
    copula_series_object_ = qb.ObjectStore.ReadBytes("copula_series_key")
    ecdf_series_object_ = qb.ObjectStore.ReadBytes("ecdfs_series_key")
    best_spread_series_object_ = qb.ObjectStore.ReadBytes("best_spread_series_key")

    copula_series = pickle.loads(copula_series_object_)
    ecdf_series = pickle.loads(ecdf_series_object_)
    best_spread_series = pickle.loads(best_spread_series_object_)

    return copula_series, ecdf_series, best_spread_series

def get_current_month_data(qb, copula_series, ecdf_series, best_spread_series, current_time):

    # Get the date a month later
    next_month_time = current_time + pd.DateOffset(months=1)

    # Access the data for the current month
    current_month_copula_series = copula_series[(copula_series.index >= current_time) & (copula_series.index < next_month_time)]
    current_month_ecdf_series = ecdf_series[(ecdf_series.index >= current_time) & (ecdf_series.index < next_month_time)]
    current_month_best_spread_series = best_spread_series[(best_spread_series.index >= current_time) & (best_spread_series.index < next_month_time)]
    
    if len(current_month_copula_series) == 0 or len(current_month_ecdf_series) == 0 or len(current_month_best_spread_series) == 0:
        qb.Log(f"No data available for current month: {current_time.strftime('%Y-%m')}")
        qb.Debug(f"No data available for current month: {current_time.strftime('%Y-%m')}")
        return np.nan, np.nan, np.nan

    return current_month_copula_series.iloc[0], current_month_ecdf_series.iloc[0], current_month_best_spread_series.iloc[0]
