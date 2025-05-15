import matplotlib.pyplot as plt
import numpy as np
import constants as cons


enlargementFactor = 1.12 #1.07 for take off and 1.12 for landing
cLmaxWpts = [9.6, 1.07]
#cLmaxW = [19.8, 1.913]

SF_S = 0.78
phi25 = 21.4

def calc_d (x, y, gradient):
    return y - x * gradient

def lin(x,grad,d):
    return grad * x + d

def lin_rev(y,grad,d):
    return (y - d)/grad

def lin_curve_pts (x1, y1, gradient, xmin, ymax):
    x_list = []
    y_list = []

    d = calc_d(x1, y1, gradient)

    x_list.append(xmin)
    y_list.append(lin(xmin,gradient,d))

    x_list.append(lin_rev(ymax,gradient,d))
    y_list.append(ymax)

    return x_list, y_list

def calc_a0 (a1, cl1, gradient):
    d = calc_d(a1, cl1, gradient)
    a0 = gradient * 0 + d
    return a0

def a_Cl_max (cLmax, dClda, a0, daClmax):
    return cLmax / dClda + a0 + daClmax

def dCl_da (a1, a2, cl1, cl2): #calculates the average gradient with 4 points
    return (cl1 - cl2) / (a1 -a2)

def dcl_da_F(dCl_da, cEnlargmentFactor, SF_S): #calculates new gradient due to extended flaps
    return dCl_da * ((cEnlargmentFactor-1) * SF_S + 1)

def dcl_Fphi (dClF, SF_S, phi25): #calculates dCL,F,phi25 at a0 + 6° due to extended flaps corrected for sweep
    return dClF * SF_S * np.cos(np.deg2rad(phi25))

def dclmax_Fphi (dClMaxF, SF_S, phi25): #calculates dCLma,F,phi25 due to extended flaps corrected for sweep
    return dClMaxF * SF_S * (np.cos(np.deg2rad(phi25)))**2

def plot_cl_a (aArray, clArray, clMax, aClMax, color: str, name: str):

    color_full_str: str = 'tab:'+color

    plt.plot(aArray, clArray, color=color_full_str)
    plt.axhline(y=clMax, color='tab:grey', label=name, linestyle='--')
    plt.scatter(np.rad2deg(aClMax), clMax, color=color_full_str, label=name, zorder=2)
    return 0

#Wing without flaps and or slats
cLmaxW = cLmaxWpts[1]
aCLmaxW = cLmaxWpts [0]
a0W = np.deg2rad(-2.2)
a06 = a0W + np.deg2rad(6)
daClmax = np.deg2rad(2.6) #diagram on slide 8

dClda = dCl_da(a0W, np.deg2rad(aCLmaxW), 0, cLmaxW)
aClMaxW = a_Cl_max(cLmaxW, dClda, a0W, daClmax)

aArrayW = np.array(np.rad2deg(lin_curve_pts(a0W, 0, dClda, a0W, cLmaxW)[0]))
clArrayW = np.array(lin_curve_pts(a0W, 0, dClda, a0W, cLmaxW)[1])

#Wing with flaps
dClF = 1.68 #improve value accuracy
dClMaxF = 1.01*1.47 #improve value accuracy

dCldaF = dcl_da_F(dClda, enlargementFactor, SF_S)
cLa06F = dcl_Fphi(dClF, SF_S, phi25) + lin(a06, dClda, calc_d(a0W, 0, dClda))
cLmaxF = cLmaxW + dclmax_Fphi(dClMaxF, SF_S, phi25)
aClMaxF = lin_rev(cLmaxF, dCldaF, calc_d(a06, cLa06F, dCldaF)) + daClmax

aArrayF = np.array(np.rad2deg(lin_curve_pts(a06, cLa06F, dCldaF, a0W, cLmaxF)[0]))
clArrayF = np.array(lin_curve_pts(a06, cLa06F, dCldaF, a0W, cLmaxF)[1])

#Wing with flaps and slats
dClMaxS = 0.5 #check value
cLmaxS = cLmaxF + dClMaxS
dCldaS = dCldaF
aClMaxS = lin_rev(cLmaxS, dCldaS,calc_d(a06, cLa06F, dCldaF)) + daClmax
#dCldaS = dCl_da(a06, aClMaxS_lin, cLa06F, cLmaxS)

aArrayS = np.array(np.rad2deg(lin_curve_pts(a06, cLa06F, dCldaS, a0W, cLmaxS)[0]))
clArrayS = np.array(lin_curve_pts(a06, cLa06F, dCldaS, a0W, cLmaxS)[1])

#plotting
plot_cl_a(aArrayW, clArrayW, cLmaxW, aClMaxW, "blue", "CL_max_Wing")
plot_cl_a(aArrayS, clArrayS, cLmaxS, aClMaxS, "red", "CL_max_Slats")
plot_cl_a(aArrayF, clArrayF, cLmaxF, aClMaxF,"orange", "CL_max_Flaps")


plt.grid()
plt.show()

