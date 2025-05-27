############################################
#                                          #
#     Axial Momentum Theory - Example      #
#                                          #
############################################

from math import *
import numpy as np
from isa import isa_model as isa
from matplotlib import pyplot as plt


# --- Axial Momentum Theory --- #


def propeller_eta(area, v_75, h):
    a1 = 0.002   # Drag divergence criterion
    a2 = 15      # Drag divergence exponential growth factor
    M_dd = 0.9  # Drag divergence Mach number at r/R = 0.75

    U = np.linspace(1, 300, 300)
    M = U / isa(h, 0)[3]
    J = U/(omega*d)

    dU = []
    T = []
    Ploss = []

    for u in U:
        du = []
        du.append(30)
        err = 1
        u_EAS = u * sqrt(isa(h, 0)[2] / isa(0, 0)[2])

        while err >= 0.001:
            du.append((1000 * P0 / (2 * isa(h, 0)[2] * area * ((u + du[-1]) ** 2)) + du[-1]) / 2)
            err = abs((du[-1] - du[-2]) / du[-2])
            # print(err)
        dU.append(du[-1])

        thrust = isa(h, 0)[2] * area * (u + dU[-1]) * 2 * dU[-1]

        # --- Transonic Loss --- #
        Ue = sqrt((u + du[-1]) ** 2 + v_75 ** 2)
        Me = Ue / isa(h, 0)[3]

        Ploss.append(0.5 * isa(h, 0)[2] * S_blade * Ue ** 3 * a1 * exp(a2 * (Me - M_dd)) / 1000)

        ADD_SPEED_CORRECTION = True

        if ADD_SPEED_CORRECTION:
            if u_EAS <= V_cr_design and u/isa(h, 0)[3] < M_cr:
                T.append(thrust)
            elif u_EAS <= V_cr_design and u/isa(h, 0)[3] > M_cr:
                t_loss = 1 - ((u/isa(h, 0)[3] - M_cr) / u/isa(h, 0)[3]) ** 2
                T.append(thrust*t_loss)
            elif u_EAS > V_cr_design:
                t_loss = 1 - ((u_EAS - V_cr_design) / u_EAS) ** 2
                T.append(thrust*t_loss)
        else:
            T.append(thrust)

    w = T * U / 1000
    eta_p = w / Pshaft
    eta_ploss = (w - Ploss)/Pshaft

    T_new = 1000*(w - Ploss)/U

    return T_new, eta_p, eta_ploss, U, M, J


# --- Propeller Parameters --- #

d = 4.24            # diameter [m]
A = pi*(d/2)**2     # disk area [m²]
rpm = 1050          # rotational velocity [rpm]
n = rpm/60          # // [rps]
omega = 2*pi*n      # // [rad/s]
V_tip = omega*d/2   # Tip velocity [m/s]
V_75 = V_tip*0.75   # Velocity at r/R = 0.75
sigma = 0.25        # Solidity [-]
S_blade = sigma*A   # Blade area [m²]
V_cr_design = 231   # Design cruise speed [m/s]
M_cr = 0.785        # Design cruise Mach number [-]

Pbr = 5607            # Engine break power [kW]
Pshaft = 0.98 * Pbr   # Shaft power at sea-level [kW], w/ n_trans = 0.98
P0 = 0.935 * Pshaft   # Jet power at Sea-level [kW], w/ n_transfer = 0.935


# --- Analysis --- #

perf_0 = propeller_eta(A, V_75, 0)
perf_1 = propeller_eta(A, V_75, 2500)
perf_2 = propeller_eta(A, V_75, 5000)
perf_3 = propeller_eta(A, V_75, 7500)
perf_4 = propeller_eta(A, V_75, 10000)
perf_5 = propeller_eta(A, V_75, 12192)

# --- Sea Level Disc Loading --- #

disc_loading_0 = perf_0[0][0]/A

print('\nDisc loading at static condition, sea-level: ' + str(np.round(disc_loading_0, 0)) + ' N/m²')


plt.figure(0)
plt.plot(perf_0[4], perf_0[2], label="0 m")
plt.plot(perf_1[4], perf_1[2], label="2500 m")
plt.plot(perf_2[4], perf_2[2], label="5000 m")
plt.plot(perf_3[4], perf_3[2], label="7500 m")
plt.plot(perf_4[4], perf_4[2], label="10000 m")
plt.plot(perf_5[4], perf_5[2], label="FL 400")
plt.ylabel("Propeller Efficiency [-]")
plt.xlabel("M [-]")
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.grid()
plt.legend()

plt.figure(1)
plt.plot(perf_0[3], perf_0[2], label="0 m")
plt.plot(perf_1[3], perf_1[2], label="2500 m")
plt.plot(perf_2[3], perf_2[2], label="5000 m")
plt.plot(perf_3[3], perf_3[2], label="7500 m")
plt.plot(perf_4[3], perf_4[2], label="10000 m")
plt.plot(perf_5[3], perf_5[2], label="FL 400")
plt.ylabel("Propeller Efficiency [-]")
plt.xlabel("U [m/s]")
plt.xlim([0, 300])
plt.ylim([0, 1])
plt.grid()
plt.legend()

plt.figure(2)
plt.plot(perf_0[4], 0.1*perf_0[0], label="0 m")
plt.plot(perf_1[4], 0.1*perf_1[0], label="2500 m")
plt.plot(perf_2[4], 0.1*perf_2[0], label="5000 m")
plt.plot(perf_3[4], 0.1*perf_3[0], label="7500 m")
plt.plot(perf_4[4], 0.1*perf_4[0], label="10000 m")
plt.plot(perf_5[4], 0.1*perf_5[0], label="FL 400 m")
plt.ylabel("Thrust [daN]")
plt.xlabel("M [-]")
plt.xlim([0, 1])
plt.ylim([0, 10000])
plt.grid()
plt.legend()

if __name__ == "__main__":
    plt.show()
plt.close()
plt.close()
plt.close()