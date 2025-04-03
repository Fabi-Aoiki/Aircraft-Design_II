import numpy as np
import constants as con
import pandas as pd
import math

import isa



def Calc_fus():
    kwf = con.kwf
    vD = con.vD
    lt = con.lt
    bf = con.bf
    hf = con.hf
    SG = con.SG

    Wf_base = kwf * (vD * (lt)/(bf + hf))**(0.5)*SG**(1.2)
    Wf = Wf_base * (1 + 0.08 + 0.07)

    return(Wf)

print(Calc_fus())




