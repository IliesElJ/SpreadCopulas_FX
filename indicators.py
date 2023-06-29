#region imports
from AlgorithmImports import *
import pickle
import pandas as pd
import datetime
import zlib
#endregion

# Time

def isLOpen(time):

    if (time.hour < 5 and time.hour >= 1):   ItIs = True
    else:   ItIs = False

    return ItIs
    
def isNYOpen(time):

    if (time.hour < 10 and time.hour >= 7):   ItIs = True
    else:   ItIs = False

    return ItIs

def isOpen(time):
    return isLOpen(time) or isNYOpen(time)


# Price


def BeFVG(bars, FVG_POINT=1):
    signal = bars[0].High < bars[2].Low and bars[1].Close < bars[1].Open
    if signal:  entry = FVG_POINT * bars[2].Low + (1-FVG_POINT) * bars[0].High
    else:   entry = 0
    return signal, entry

def BuFVG(bars, FVG_POINT=1):
    signal = bars[0].Low < bars[2].High and bars[1].Close > bars[1].Open
    if signal:  entry = (1-FVG_POINT) * bars[2].High + (FVG_POINT) * bars[0].Low
    else:   entry = 0
    return signal, entry

def SwingH(bars):
    signal = bars[1].High > bars[0].High and bars[1].High > bars[2].High 
    signal = signal and bars[2].Close > bars[2].Open 
    return signal, bars[1].High

def SwingL(bars):
    signal = bars[1].Low < bars[0].Low and bars[1].Low < bars[2].Low 
    signal = signal and bars[2].Close > bars[2].Open 
    return signal, bars[1].Low

def check_setup(sls, shs, short=True):
    if short and shs[0] > sls[0] and shs[0] > sls[0] and shs[0] > shs[1]:
        return True
    else:
        return False
