import math
#from matplotlib import pyplot as plt

T0 = 288.15
p0 = 101325
A0 = -0.0065

T11 = 273.15 - 56.5
p11 = 22632
T20 = 273.15 - 56.5
p20 = 5475
A20=0.001

g0 = 9.80665
R = 287.052
gamma = 1.4
a0 = 340.294

S = 110.4
beta = 1.450 * 10 ** (-6)


def isa_model(h, dT):
    if h <= 11000:
        temp = T0 + A0 * h + dT
        p = p0*(1+(h * A0) / T0) ** (-g0 / (A0 * R))

    elif 11000 < h <= 20000:
        temp = T11 + dT
        p = p11 * math.exp(-g0/ (R * T11) * (h - 11000))
        #p = p11 * exp(-g0/(R*T11) * (h-11000))

    elif 20000 < h <= 32000:
        temp = T20 + A20 * (h-20000) + dT
        p = p20*(1+(A20*(h-20000))/T20)**(-g0/(A20*R))

    else:
        print('you are a submarine or too high')

    rho = p / (R * temp)
    a = (gamma * R * temp) ** (1 / 2)
    mu = beta * temp ** (3 / 2) / (temp + S)
    nu = mu / rho

    return p, temp, rho, a, mu, nu


