import constants as cons
import numpy as np

xACnT_MAC = 0.25 - 0.1 - 0.05
xACnT_MAC_08 = 0.25 - 0.1 - 0.05 + 0.055 #Shift due to MACH number 0.8

MAC = cons.MAC
S_T = 29.4
S = 197.5
#rTAC=25.670
rTAC=28.67 # 3 Meters

def deg_to_rad(deg):
    rad = np.pi / 180 * deg
    return rad

def sigma (xn_MAC, xcg_MAC):
    sigma = xn_MAC - xcg_MAC
    if sigma >= 0.05:
        print("\nWithin Static Stabbility Limit! sigma = ", sigma)
        return sigma
    else:
        print("\nOutside of Static Stability Limit! sigma = ", sigma)
        return sigma

def c_Li(AR, phi_50, M):
    phi_50 = deg_to_rad(phi_50) #degree to radiant converter
    c_Li = np.pi * AR / (1 + np.sqrt(1 + (AR/2)**2 * ((np.tan(phi_50))**2 + (1 - M**2))))
    return c_Li

def daw_danT (rTAC, M):
    b = 44.4
    b_v = 5.37
    daw_danT = 1.75 * round(c_Li(cons.AR, 19, M), 3) / (np.pi * cons.AR * (cons.taper * rTAC * 2 / b)**0.25 * (1 + b_v * 2 / b))
    return daw_danT

def xn_MAC (rTAC, M):

    c_LT = c_Li(cons.AR_h, 20, M)
    c_LnT = c_Li(cons.AR, 19, M)
    daw_danT_ = daw_danT(rTAC, M)
    c_L = c_LnT * (1 + c_LT/c_LnT * S_T/S * 0.95 * (1 - daw_danT_))

    xn_MAC = xACnT_MAC + rTAC/MAC * S_T/S * 0.95 * c_LT/c_L * (1 - daw_danT_)

    #print("c_LT: ", c_LT, "\nc_LnT: ", c_LnT, "\ndaw_danT: ", daw_danT_, "\nc_L: ", c_L)
    return xn_MAC

def sigma (xn_MAC, xcg_MAC):
    sigma = xn_MAC - xcg_MAC
    if sigma >= 0.05:
        print("\nWithin Static Stabbility Limit! sigma = ", sigma)
        return sigma
    else:
        print("\nOutside of Static Stability Limit! sigma = ", sigma)
        return sigma

#print(xn_MAC(27.9, cons.ma_max))
def xn_MAC_Mach_08 (rTAC, M):

    c_LT = c_Li(cons.AR_h, 20, M)
    c_LnT = c_Li(cons.AR, 19, M)
    daw_danT_ = daw_danT(rTAC, M)
    c_L = c_LnT * (1 + c_LT/c_LnT * S_T/S * 0.95 * (1 - daw_danT_))

    xn_MAC_08 = xACnT_MAC_08 + rTAC/MAC * S_T/S * 0.95 * c_LT/c_L * (1 - daw_danT_)

    #print("c_LT: ", c_LT, "\nc_LnT: ", c_LnT, "\ndaw_danT: ", daw_danT_, "\nc_L: ", c_L)
    return xn_MAC_08



print(xn_MAC(rTAC, cons.ma_max))