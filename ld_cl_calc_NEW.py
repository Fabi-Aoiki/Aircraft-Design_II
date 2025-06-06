import numpy as np
import matplotlib.pyplot as plt
import isa as isa
import constants as con
import Drag_AD2 as drag

#Funktion
#########################################################################################################################################
def rho (h, dT):
    return isa.isa_model(h, dT)[2]

def speed_of_sound(h, dT):
    return isa.isa_model(h, dT)[3]

def calc_cl(weight, rho, v):
    return 2 * (weight * 0.99) / (rho * 197.5 * v ** 2)

def CalcAnaDrag(M, h):
    # fuselage drag estimation (page 12 in pdf)

    l_f = con.l_fus_s  # length fuselage
    vel = M * isa.isa_model(h, con.dt)[3]  # cruise speed in m/s
    Re = vel * l_f / isa.isa_model(h, con.dt)[5]  # Reynolds number
    C_Ftu = 0.455 / (np.log10(Re)) ** 2.58  # friction coefficient turbulent flow
    d_f = 0.5 * (con.bf + con.hf)  # averaged diameter of the fuselage
    k_f = 2.2 * (d_f / l_f) ** 1.5 + 3.8 * (d_f / l_f) ** 3  # pressure drag factor
    k_lgb = 1 / 5 * k_f  # penalty factor for the landing gear boxes
    S_w = 197.5  # wing area
    S_fwet = con.SG  # fuselage wetted area (might need to be updated due to new landing gear pods)
    c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w  # fuselage drag coefficient

    # nacelle drag estimation (page 13 in pdf)

    l_n = 2  # length nacelle (meters)
    Re = vel * l_f / isa.isa_model(h, con.dt)[5]  # Reynolds number
    C_Ftu = 0.455 / (np.log10(Re)) ** 2.58  # friction coefficient turbulent flow
    d_n = 1.2  # diameter nacelle (meters)
    k_n = 2.2 * (d_n / l_n) ** 1.5 + 3.8 * (d_n / l_n) ** 3  # pressure drag factor
    S_nwet = (d_n ** 2 * 3.1416 / 4 + d_n * 3.1416 * l_n) * con.N_E  # wetted surface of all four nacelles
    c_Dn = C_Ftu * (1 + k_f) * S_nwet / S_w  # fuselage drag coefficient

    # compressible drag estimation (page 11 in pdf)

    #DeltaC_D = 0.0  # for M = 0.6

    return (c_Df + c_Dn)

def calc_cd_comp(cl, m, mdd):
    cd_0 = 0.01673 - 0.0072
    k = 1 / (10 * np.pi * 0.99) #curvefitting factor
    m_dd = mdd / (np.cos(np.deg2rad(21.4)))
    return cd_0 + k * cl ** 2 + 0.002 * np.exp(60 * (m - m_dd))



#####################################
######### DIAGRAMM CL_CD ############
#####################################

for h in [0, 2500, 5000, 7500, 10000, 12000]:
    m_list = []
    m_list_plot = []
    cd_list = []
    cl_list = []
    ld_list = []
    datenpunkte = 2000

    # filling M_list
    for i in range(1, datenpunkte, 1):
        m_max = 0

        if h >= 7500:
            m_max = 0.95
        else:
            m_max = 154 / np.sqrt(rho(h,0)/rho(0,0))/speed_of_sound(h,0)

        m_list.append(m_max * i / (datenpunkte - 1))

    for mdd in [0.758]:
        for m in m_list:
            cl = calc_cl(con.Wto_stretch, rho(h, 0), speed_of_sound(h, 0) * m)

            if cl > 1.07:
                continue

            cl_list.append(cl)
            cd = calc_cd_comp(cl, m, mdd) + CalcAnaDrag(m, h)
            cd_list.append(cd)
            ld_list.append(cl/cd)
            m_list_plot.append(m)

    cd = np.array(cd_list)
    cl = np.array(cl_list)
    plt.plot(cd, cl, label = "CD(CL) for different Mach numbers @ " + str(h) + " m", zorder = 12200 - h)


plt.scatter(calc_cd_comp(calc_cl(con.Wto_stretch, rho(12000, 0), speed_of_sound(12000, 0)*0.785), 0.785, 0.758) + CalcAnaDrag(0.785, 12000),calc_cl(con.Wto_stretch, rho(12000, 0), speed_of_sound(12000, 0)*0.785), color='orange',label="Cruise Design Point", zorder = 24000)
plt.plot(drag.cd_indu_all_list, drag.cl_indu_all_list, label="CD(CL) as simulated at M = 0.6", zorder = 0)
plt.xlabel("CD")
plt.ylabel("CL")
plt.legend()
plt.xlim(0,0.08)
#plt.ylim(-1.1, 1.15)
plt.grid()
plt.show()
plt.close()


#####################################
######### DIAGRAMM LD_CL ############
#####################################

for h in [0, 2500, 5000, 7500, 10000, 12000]:
    m_list = []
    m_list_plot = []
    cd_list = []
    cl_list = []
    ld_list = []
    datenpunkte = 2000

    # filling M_list
    for i in range(1, datenpunkte, 1):
        m_max = 0

        if h >= 7500:
            m_max = 0.95
        else:
            m_max = 154 / np.sqrt(rho(h,0)/rho(0,0))/speed_of_sound(h,0)

        m_list.append(m_max * i / (datenpunkte - 1))

    for mdd in [0.758]:
        for m in m_list:
            cl = calc_cl(con.Wto_stretch, rho(h, 0), speed_of_sound(h, 0) * m)

            if cl > 1.07:
                continue

            cl_list.append(cl)
            cd = calc_cd_comp(cl, m, mdd) + CalcAnaDrag(m, h)
            cd_list.append(cd)
            ld_list.append(cl/cd)
            m_list_plot.append(m)

    ld = np.array(ld_list)
    cl = np.array(cl_list)
    plt.plot(cl, ld, label = "LD(CL) for different Mach numbers @ " + str(h) + " m", zorder = 200 + h)

plt.xlim(0, 1.25)
plt.ylim(0,22.5)
plt.xlabel("CL")
plt.ylabel("L/D")
plt.legend()
plt.grid()
plt.show()


#######################################
######### DIAGRAMM LD_Mach ############
#######################################

for h in [0, 2500, 5000, 7500, 10000, 12000]:
    m_list = []
    m_list_plot = []
    cd_list = []
    cl_list = []
    ld_list = []
    datenpunkte = 2000

    # filling M_list
    for i in range(1, datenpunkte, 1):
        m_max = 0

        if h >= 7500:
            m_max = 0.95
        else:
            m_max = 154 / np.sqrt(rho(h,0)/rho(0,0))/speed_of_sound(h,0)

        m_list.append(m_max * i / (datenpunkte - 1))

    for mdd in [0.758]:
        for m in m_list:
            cl = calc_cl(con.Wto_stretch, rho(h, 0), speed_of_sound(h, 0) * m)

            if cl > 1.07:
                continue

            cl_list.append(cl)
            cd = calc_cd_comp(cl, m, mdd) + CalcAnaDrag(m, h)
            cd_list.append(cd)
            ld_list.append(cl/cd)
            m_list_plot.append(m)

    ld = np.array(ld_list)
    m = np.array(m_list_plot)
    plt.plot(m, ld, label = "LD(CL) for different Mach numbers @ " + str(h) + " m", zorder = 200 + h)

plt.xlim(0, 1.25)
plt.ylim(0,22.5)
plt.xlabel("Mach Number")
plt.ylabel("L/D")
plt.legend()
plt.grid()
plt.show()