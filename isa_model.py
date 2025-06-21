############################################
#                                          #
# International Standard Atmosphere Model  #
#                                          #
############################################

from math import *
from matplotlib import pyplot as plt

# Reference conditions at Sea Level (h = 0)
T0 = 288.15     # Temperature at SL [K]
p0 = 101325     # Pressure at SL [Pa]
A0 = -0.0065    # Temp Gradient Troposphere

# Reference conditions at 11,000 m
T11 = 216.65    # Temperature at 11 km [K]
p11 = 22632     # Pressure at 11 km [Pa]

# Reference conditions at 20,000 m
T20 = 216.65    # Temperature at 20 km [K]
p20 = 5475      # Pressure at 20 km [Pa]
A20 = 0.001     # Temp gradient stratosphere

# Premises from the ISA model
g0 = 9.80665        # Acceleration of gravity [m/s²]
R = 287.052         # Gas constant for air
gamma = 1.4         # Specific heat ratio of air
S = 110.4           # Sutherland's reference temperature [K]
beta = 1.458e-6     # Sutherland's constant


# Inputs are altitude in meters and delta temperature in Kelvin

def isa_model(h, dT):
    if h <= 11000:              # Troposphere
        temp = T0 + A0*h + dT
        press = p0*(1+(A0*h)/T0)**(-g0/(A0*R))
    elif 11000 < h <= 20000:    # Tropopause
        temp = T11 + dT
        press = p11*exp(-g0/(R*T11) * (h-11000))
    elif 20000 < h <= 32000:    # Stratosphere
        temp = T20 + A20 * (h-20000) + dT
        press = p20*(1+(A20*(h-20000))/T20)**(-g0/(A20*R))
    else:
        print('Invalid altitude')
        return

    rho = press/(R*temp)
    a = sqrt(gamma*R*temp)
    mu = beta*temp**(3/2)/(temp+S)
    nu = mu/rho

    return press, temp, rho, a, mu, nu


# --- Sample Plots ---#

show_plots = False

if show_plots:
    H = []
    T = []
    T15 = []
    P = []
    rho = []
    rho15 = []
    a = []
    a15 = []
    dT = +15
    for altitude in range(0, 32000, 200):
        H.append(altitude)
        T.append(isa_model(altitude, 0)[1])
        T15.append(isa_model(altitude, dT)[1])
        P.append(isa_model(altitude, 0)[0])
        rho.append(isa_model(altitude, 0)[2])
        rho15.append(isa_model(altitude, dT)[2])
        a.append(isa_model(altitude, 0)[3])
        a15.append(isa_model(altitude, dT)[3])

    plt.figure(0)
    plt.plot(T, H, label='ISA')
    plt.plot(T15, H, label='ISA' + str(dT))
    plt.grid()
    plt.legend()
    plt.ylabel('Altitude [m]')
    plt.xlabel('Temperature [K]')
    plt.ylim([0, 32000])
    plt.xlim([180, 320])

    plt.figure(1)
    plt.plot(rho, H, label='ISA')
    plt.plot(rho15, H, label='ISA'+str(dT))
    plt.grid()
    plt.legend()
    plt.ylabel('Altitude [m]')
    plt.xlabel('Density [kg/m³]')
    plt.ylim([0, 32000])
    plt.xlim([0, 1.4])

    plt.figure(2)
    plt.plot(a, H, label='ISA')
    plt.plot(a15, H, label='ISA'+str(dT))
    plt.grid()
    plt.legend()
    plt.ylabel('Altitude [m]')
    plt.xlabel('Speed of Sounds [m/s]')
    plt.ylim([0, 32000])
    plt.xlim([270, 350])

    plt.show()
    plt.close()
