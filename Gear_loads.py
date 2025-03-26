import numpy as np
import constants as con
import pandas as pd
import math
import isa
import main

def Nose_max():
    FNO_max = 0.15 * con.Wto_stretch

    return(FNO_max)


def Nose_load(L_N,L_M):
    L_COG = main.x_CoG - L_N
    FG = main.Momenten_Summe['Weights']

    L_M = L_M - L_N

    FM = (FG*L_COG)/L_M

    FN = FG - FM

    f =  FN / Nose_max()




    return(FN, f)

print(Nose_max())
print(f"NOSE LOAD = {Nose_load(5,36.765)}")

