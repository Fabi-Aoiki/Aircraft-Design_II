# ----------------------------------- #
#                                     #
#   Direct Operating Cost Functions   #
#                                     #
# ----------------------------------- #

from math import *
import numpy as np


def capital_cost(oew, w_eng, n_eng):
    # Fixed parameters:
    p_oew = 1150.0          # Price/kg OEW
    p_eng = 1550.0          # Price/kg Engines
    ir = 0.05               # Interest rate
    f_rv = 0.15             # Residual value factor
    f_ins = 0.005           # Insurance rate
    dp = 12                 # Depreciation Period [Years]
    # Annuity factor
    a = ir*(1-f_rv*(1/(1+ir))**dp)/(1-(1/(1+ir))**dp)

    # Capital cost
    k_hfe = 0.31            # Price increase for alternative propulsion system

    c_airframe = (oew-n_eng*w_eng)*p_oew*1.1
    c_engine = w_eng*n_eng*p_eng*1.3
    c_cap = (a+f_ins)*(1+k_hfe)*(c_airframe + c_engine)

    return c_cap, round((c_engine/(c_airframe+c_engine)), 3)


def crew_cost(pax):
    # Fixed parameters:
    cc = 5.0                # Crew complement
    salary_fa = 60000.0     # Salary flight attendant [€/year]
    salary_fc = 300000.0    # Salary cockpit crew [€/year]

    # Salary increase factor
    f_sinc = (1 + 0.03) ** 12
    # Personnel cost
    c_crew = cc*(salary_fa*np.ceil(pax/50) + 2*salary_fc) * f_sinc

    return c_crew


def maintenance_cost(oew, n_eng, slst, range_d, v_cruise):
    # Fixed parameters:
    lr = 50.0               # Labor Rate [€/h]
    burden = 2              # Cost burden
    oew_ton = oew/1000
    t_flight = (range_d * 1000 / v_cruise) / 3600

    # Material cost (airframe):
    mc_mat = oew_ton*(0.21*t_flight + 13.7) + 57.5

    # Personnel cost (airframe):
    mc_per = lr*(1+burden)*((0.655 + 0.01*oew_ton)*t_flight + 0.254 + 0.01*oew_ton)

    # Engine total maintenance cost:
    mc_eng = n_eng*(1.5*slst/9810+30.5*t_flight+10.6)

    # Maintenance increase factor
    f_minc = (1 + 0.02) ** 12

    # Maintenance cost:
    k_fhe_maint = 0.47      # Correction factor for alternative propulsion technology
    c_maint = (mc_mat + mc_per + mc_eng)*(1 + k_fhe_maint)*f_minc

    return c_maint


def flight_cycles(v_cruise, range_d):
    # Fixed parameters:
    pot = 8760.             # Potential yearly operating time
    dt = 2748.8             # Yearly forced downtime
    t_block = 1.83          # Block time supplement per flight
    t_flight = (range_d * 1000 / v_cruise) / 3600
    ot = pot - dt           # Yearly operating time (EU average: 6011.2)

    # Flight Cycles
    hfe_correction = -0.07     # HFE Correction of -7% flight cycles due to longer fueling times. Set 0 for kerosene.
    fc = ot/(t_flight+t_block)*(1 - hfe_correction)

    return fc


def route_costs(fc, w_fuel, payload, mtow, range_d):
    # Fixed parameters:
    p_f = 2.7                # Fuel price [€/kg]       For kerosene: 0.808 €/kg  For LH2: 2.7 €/kg
    p_pl = 0.015             # Handling fees [€/kg]
    p_l = 0.015              # Landing fees [€/kg]

    c_fuel = fc*p_f*w_fuel
    c_payload = fc*p_pl*payload*(1 + 0.02) ** 12
    c_landing = fc*p_l*mtow*(1 + 0.02) ** 12
    c_atc = fc * 1 * range_d * sqrt(mtow / 50000)

    return c_fuel, c_payload, c_atc, c_landing

