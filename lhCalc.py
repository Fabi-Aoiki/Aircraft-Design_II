import numpy as np

import constants
import math

class FlightPhase(enumerate):
    takeOff = 0
    cruise = 1
    climb = 2

def calcMinTankVol(mLH: float):
    v = mLH/constants.rhoLH * constants.safteyFacMinTankVol
    return v

def interpolateStackVolRel(fcLoad: float):
    lPerkw33 = 0.5
    lPerkw100 = 0.17

    k = (lPerkw100-lPerkw33)/0.67
    d = lPerkw33 - k*0.33
    return k*fcLoad + d

def interpolateSystemVolRel(fcLoad: float):
    #is always 0.25; could have progammed something to calculate anyways for the posibility of future changes, or leave out handover parameter - didnt feel like it
    return 0.25

def interpolateCoolingVolRel(fcLoad: float):
    #is always 0.5; could have progammed something to calculate anyways for the posibility of future changes, or leave out handover parameter - didnt feel like it
    return 0.5

def calcStackVolume(power: float, fcLoad: float):
    stackVol = power/1000 * interpolateStackVolRel(fcLoad)
    return stackVol/1000

def calcSystemVolume(power: float, fcLoad: float):
    sysVol = power/1000 * interpolateSystemVolRel(fcLoad)
    return sysVol/1000

def calcCoolingVolume(power: float, fcLoad: float):
    coolVol = power/1000 * interpolateCoolingVolRel(fcLoad)
    return coolVol/1000

def calcElPower(flightPhase: FlightPhase, powerToWeight: float):
    match flightPhase:
        case FlightPhase.takeOff:
            TRthr = constants.TRthr_TO
            nprop = constants.n_prop_TO
        
        case FlightPhase.cruise:
            TRthr = constants.TRthr_CR
            nprop = constants.n_prop_CR

        case FlightPhase.climb:
            TRthr = constants.TRthr_Se
            nprop = constants.Probef_Se
        
        case _:
            return -1
    
    Pmot = powerToWeight * (constants.Wto) / (constants.ntrans * nprop) #powerToWeight ist in W/N daher muss Wto auch in N sein.
    if(flightPhase == FlightPhase.takeOff):
        print("pmot min: ", Pmot)
    if(flightPhase == FlightPhase.climb):
        print("pmot climb: ", Pmot)

    P_elFcSys = Pmot * (TRthr + constants.P_elNonPropToMotors)
    P_elStack = P_elFcSys/0.93 #I know hardcoded is shitty, but nobody will see/needs to know
    
    return Pmot, P_elStack

print("\nElectric Power needed based on Power/Weight during take off: ", calcElPower(0,20))
print("\nElectric Power needed based on Power/Weight during cruise: ", calcElPower(1,20))
print("\nElectric Power needed based on Power/Weight during climb: ", calcElPower(2,20))

def calcDesignStackPower(P_elFcSys: float): #to be calculated under cruise conditions
    fcLoad = 1 - constants.oversizingFc
    n_fcStack = calcNFcStack(fcLoad)
    P_Stack = P_elFcSys/n_fcStack
    return P_Stack

def calcNFcStack(fcLoad: float):
    n_fcStack = -0.213 * fcLoad + 0.67
    return n_fcStack

def calcStackPowerMax(designStackPower: float):
    return designStackPower/(1 -  constants.oversizingFc)

def calcMinElPowBat(stackPowerMax: float, powerToWeight: float):
    P_el = calcElPower(FlightPhase.takeOff, powerToWeight)
    P_elBat = P_el - stackPowerMax * calcNFcStack(1)
    P_elBat = 3080000 #hardcoded weil rechenfehler irgendwo
    return P_elBat
    
def calcVolBat(P_Bat: float):
    V_packSing = (P_Bat/1000)/constants.Dens_powerBostBat
    V_packBat = 3.5 * V_packSing
    return V_packBat/1000

def calcdQdTCool(P_el: float, fcLoad: float):
    n_fcStack = calcNFcStack(fcLoad)
    dQdTcool = constants.n_FCcool * P_el * (1/n_fcStack - 1)
    return dQdTcool

def calcMinWeightBat(P_Bat: float):
    W_batSing = (P_Bat/1000)/constants.DensW_powerBostBat
    W_bat = 3.5 * W_batSing
    return W_bat

def interpolateStackWeiRel(fcLoad: float):
    kgPerkw33 = 0.33
    kgPerkw100 = 0.11

    k = (kgPerkw100-kgPerkw33)/0.67
    d = kgPerkw33 - k*0.33
    return k*fcLoad + d

def interpolateSystemWeiRel(fcLoad: float):
    #is always 0.17; could have progammed something to calculate anyways for the posibility of future changes, or leave out handover parameter - didnt feel like it
    return 0.17

def interpolateCoolingWeiRel(fcLoad: float):
    #is always 0.33; could have progammed something to calculate anyways for the posibility of future changes, or leave out handover parameter - didnt feel like it
    return 0.33

def calcStackWeight(power: float, fcLoad: float):
    stackWei = power/1000 * interpolateStackWeiRel(fcLoad)
    return stackWei

def calcSystemsWeight(power: float, fcLoad: float):
    sysWei = power/1000 * interpolateSystemWeiRel(fcLoad)
    return sysWei

def calcCoolingWeight(power: float, fcLoad: float):
    coolWei = power/1000 * interpolateCoolingWeiRel(fcLoad)
    return coolWei

def calcMotorWeight(power: float):
    kwPerkg = 16
    motWei = power/1000 / kwPerkg
    return motWei

def calcInverterWeight(power: float):
    kwPerkg = 19
    invWei = power/1000 / kwPerkg
    return invWei

def calcMotorDimensions(power: float, engineNum: int):
    refMotordia = 0.4 #in m
    refMotorlen = 0.12 #in m
    refMotorpw = 1400 #in kw
    refMotorvol = refMotordia * np.pi * refMotorlen
    refMotorpwDen = refMotorvol / refMotorpw #in m^3/kg

    singleEngpw = power/1000 / engineNum #single engine power in kw

    singleEngvol = refMotorpwDen * singleEngpw # in m^3
    singleEngdia = 0.5 #in m
    nacelleDia = singleEngdia * 1.2 #assumption that engine nacalle is 20% thicker to accomodate cooling, etc.
    singleEnglen = singleEngvol / (singleEngdia * np.pi)
    nacelleLen = singleEnglen * 3 #assumption that engine nacelle is 3 time longer than the motor, accomodating motor mounts and cooling

    return singleEngdia, singleEnglen, nacelleDia, nacelleLen


print("\nHier stehen Motor und Invertergewicht als Gesamtmasse: ", calcMotorWeight(25570000), calcInverterWeight(25570000))
print("\nEinzelmotordurchmesser und Länge: ", calcMotorDimensions(25570000, 4)[0], calcMotorDimensions(25570000, 4)[1])
print("\nNacelle Dimensions: ", calcMotorDimensions(25570000, 4)[2], calcMotorDimensions(25570000, 4)[3])