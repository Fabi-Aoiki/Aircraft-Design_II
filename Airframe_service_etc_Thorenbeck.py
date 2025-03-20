import numpy as np
import constants as con
import pandas as pd
import math
import isa


def Calc_Wieg():
    kieg = con.kieg
    WDE = con.mOE_s
    RD = con.RC #Fehler aber nicht bessser möglich (Ja scheiße)

    Wieg = kieg * WDE **(5/9) * RD **(1/4)

    return(Wieg)



def Calc_Whp(): #Berechnung nach Formel 8-38, Berechnung Hydraulics and Pneumatics
    WDE = con.mOE_s
    Whp = 0.011 * WDE + 181 #kg

    return(Whp)



def Calc_Wel(): #Berechnung nach Formel 8-40, Berechnung Electrical, Annahme über die Nutzung der DC formel da ohnehin sehr abweichend für LH2
    
    Wto = con.Wto_stretch/9.806
    Wel = 0.02 * Wto + 181 #kg

    return(Wel)


def Calc_Wfurn(): # Berechnung 8.4.3.d nach Formel 8-44 oder nach Tabelle 8-12
    # mZF = we.mZF
    # W_furn = 0.196 * mZF**(0.91)

    WDE = con.mOE_s
    W_furn_1 = 9.1 * WDE**(0.285) # for propeller

    #W_furn_2 = 29.9 * 72 + 25.4 * 30 # mass per seating block times block (page 76, table 3-2)

    W_furn_3 = 113.4 + 29.5 # 1 x main meal galley + 1 x coffee bar

    W_furn_4 = 136 * 7 # mass per toilet x amount of toilets

    S_cf = 200 # m^2, muss noch nachgesehen werden
    W_furn_5 = 0.94 * S_cf**(1.15)

    V_pc = 200 # m^3, muss noch nachgesehen werden
    V_ch = 200 # m^3, muss noch nachgesehen werden
    W_furn_6 = 3.69 * (V_pc + V_ch)**(1.14)

    W_furn_7 = 1.28 * V_ch

    W_furn_8 = 0 # kein convertible

    W_furn_9 = 18.1 + 1.09 * 276 # 276 pax

    Wto = con.Wto_stretch/9.806
    W_furn_10 = 0.0030 * Wto

    W_furn_11 = 0.453 * (276 + 6 + 2) # pax + stewards + pilots

    W_furn = W_furn_1 + W_furn_3 + W_furn_4 + W_furn_5 + W_furn_6 + W_furn_7 + W_furn_8 + W_furn_9 + \
    W_furn_10 + W_furn_11 + """W_furn_2""" 

    return(W_furn)


def Calc_Weight_AC_Thoren():
    W_AC_T = 14 * con.l_cab**(1.28)
    return(W_AC_T)

def Calc_Weight_AC():
    W_T = Calc_Weight_AC_Thoren()

    Q_p = con.Q_ppax * con.pax_s
    Q_lh = con.Q_lhi

    fac = (Q_p - Q_lh) / Q_p # Correction Factor through cooling by LH

    W_AC = W_T *fac

    return(W_AC)
