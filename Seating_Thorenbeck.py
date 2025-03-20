import numpy as np
import constants as con
import pandas as pd
import math
import isa

def Calc_Weight_econ():
    EcoPax = con.pax_s - 60
    W_eco_pp = con.W_eco_pp
    W_eco = EcoPax * W_eco_pp

    return(W_eco)

def Calc_Weight_Buisness():
    BusPax = 60
    W_bus_pp = con.W_bus_pp
    W_bus = BusPax * W_bus_pp

    return(W_bus)