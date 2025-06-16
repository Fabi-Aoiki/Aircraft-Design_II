# skript für flight performance 2 basierend auf dem Handout

import Flight_Performance_1 as FP1
import matplotlib.pyplot as plt
import numpy as np

# INTEGRAL CLIMB PERFORMANCE
# sep_list = FP1.SEP_list_all
alti_list = FP1.alti_list
# sep_max_list = []

# for i in range(len(sep_list)):
#     max_sep = max(sep_list[i])
#     sep_max_list.append(max_sep)

# print(sep_max_list)

# manuelles rauslesen notwendig fürs erste
sep_max_list = [9.8, 9.3, 8.7, 8.1, 7.1, 5.7]
invert_sep_max_list = []
for sepMax in sep_max_list:
    invert_sep_max_list.append(1/sepMax)
plt.plot(alti_list, invert_sep_max_list)
plt.fill_between(alti_list, invert_sep_max_list, 0, alpha=0.3)

# accel after climb
plt.plot([12000, 12200], [1/5.7, 1/4.2])
plt.fill_between([12000, 12200], [1/5.7, 1/4.2], 0, alpha=0.3)


# ausrechnen climb time
climbTime = np.trapezoid(invert_sep_max_list, alti_list)
# jetzt einfach bisschen was dazu für acceleration auf pfusch
# faktor ausgemessen aus tuwel seiten
climbTime = climbTime + np.trapezoid([1/5.7, 1/4.2], [12000, 12200])

plt.xlabel("Altitude (m)")
plt.ylabel("1/SEP (s/m)")
plt.title("Climb Time = " + str(round(climbTime/60)) + " min")
plt.xlim(left=0)
if __name__ == "__main__":
    plt.show()
plt.close()


# climb distance berechnung
# jeweiligen geschwindigkeit beim sepMax
sep_max_vel_list = [100, 110, 122, 140, 158, 204]
for i in range(len(sep_max_vel_list)):
    sep_max_vel_list[i] = sep_max_vel_list[i] * invert_sep_max_list[i]

plt.plot(alti_list, sep_max_vel_list)
plt.fill_between(alti_list, sep_max_vel_list, 0, alpha=0.3)

# ausrechnen climb distance
climbDistance = np.trapezoid(sep_max_vel_list, alti_list)
# noch accel dazu
climbDistance = climbDistance * 1.06 # meters!

plt.xlabel("Altitude (m)")
plt.ylabel(r"$1/\gamma$ (-)")
plt.title("Climb Distance = " + str(round(climbDistance/1000)) + " km")
plt.xlim(left=0)
if __name__ == "__main__":
    plt.show()
plt.close()


# climb fuel berechnung
# sar_max_list = [1365, 1360, 1360, 1380, 1340, 1400]
# das ist viel zu gut so, muss ich manuell anpassen leider
sar_max_list = [1365-355, 1360-355, 1360-355, 1380-355, 1340-355, 1400-355]
invert_sar_max_list = []
for sarMax in sar_max_list:
    invert_sar_max_list.append(1/sarMax)
plt.plot(alti_list, invert_sar_max_list)
plt.fill_between(alti_list, invert_sar_max_list, 0, alpha=0.3)

# ausrechnen climb fuel
climbFuel = sum(invert_sar_max_list) / len(invert_sar_max_list) * climbDistance
# noch accel dazu
climbFuel = climbFuel * 1.06 # kilos!

plt.xlabel("Altitude (m)")
plt.ylabel("1/SAR (kg/m)")
plt.title("Climb Fuel = " + str(round(climbFuel)) + " kg")
plt.xlim(left=0)
if __name__ == "__main__":
    plt.show()
plt.close()