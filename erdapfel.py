import matplotlib.pyplot as plt
import main
import constants as con
import numpy as np
import Static_Stability_Limit


# function x_CoG to x_CoG_MAC / MAC

def xCOG_percMAC(x_CoG):
    x_MAC = 32.660
    MAC = con.MAC
    x_CoG_MAC = x_CoG - x_MAC
    percMAC = x_CoG_MAC / MAC * 100



# loading phase

x_CoG_OE = main.x_CoG
m_OE = main.Momenten_Summe['Weights']

# limits

    # max nose gear load

x = np.linspace(28.39, 30.35, 100)
y = 553928 / (34.828 - x)
plt.plot(x, y, "-", label = "Max Nose Gear Load", color = "black", linestyle = ":")

    # min nose gear load

plt.plot([33.34, 33.34], [m_OE, main.W_Take_off], "-", label = "Min Nose Gear Load", color = "black", linestyle = "--")

Static_Stability_Limit.xn_MAC(27.9, con.ma_max)    # neutral point

pass # 40.8 %

Static_Stability_Limit.xn_MAC_Mach_08(27.9, con.ma_max) #AC 08

pass # blabla

# fueling

px = list()
py = list()

px.append(x_CoG_OE)
py.append(m_OE)
px.append(x_CoG_OE)
py.append(m_OE + con.m_fStr)

plt.plot(px, py, '-', label = "Fueling", color = "red")

# boarding

m_row_econ = 6*83 + 3*12 # kg
m_row_prem = 4*83 + 2*12 # kg
n_row = 15 + 15 + 1 + 20 # amount of rows
x_row_51 = 52.619 # distance in x direction for row bla from tip
x_row_31 = 36.034
x_row_30 = 34.891
x_row_15 = 19.554
pitch_econ = 32*2.54/100
pitch_prem = 36*2.54/100

px = list()
py = list()

px.append(x_CoG_OE)
py.append(m_OE + con.m_fStr)

x_row = list()
m_row = list()

for i in range(15):
    x_row.append(x_row_15-14*pitch_prem+i*pitch_prem)
    m_row.append(m_row_prem)
for i in range(15):
    x_row.append(x_row_30-14*pitch_econ+i*pitch_econ)
    m_row.append(m_row_econ)
for i in range(1):
    x_row.append(x_row_31)
    m_row.append(m_row_econ)
for i in range(20):
    x_row.append(x_row_51-19*pitch_econ+i*pitch_econ)
    m_row.append(m_row_econ)

x_old = x_CoG_OE
m_old_it0 = m_OE + con.m_fStr

for i in range(len(x_row)):
    m_old = m_old_it0 + sum(m_row[50-i:])
    m_new = m_old + m_row[50-i]
    x_new = 1/m_new * (x_old * m_old + x_row[50-i] * m_row[50-i])
    px.append(x_new)
    py.append(m_new)
    x_old = x_new
    m_old = m_new

plt.plot(px, py, "-", label = "Boarding", color = "green")

# cargo loading

n_ld = 12
x_ld = list()

for i in range(0, n_ld):
    x_ld.append(54.786-n_ld*1.536+1.536/2+1.536*i)

m_cargo = 6656 # kg
m_ld = m_cargo / n_ld

m_old_it0 = m_new
x_old = x_new

px = [x_old]
py = [m_old_it0]

for i in range(len(x_ld)):
    m_old = m_old_it0 + m_ld*i
    m_new = m_old + m_ld
    x_new = 1/m_new * (x_old * m_old + x_ld[i] * m_ld)
    px.append(x_new)
    py.append(m_new)
    x_old = x_new
    m_old = m_new

plt.plot(px, py, "-", label = "Cargo Loading", color = "blue")

# plot

xmin = 28.0
xmax = 34.0
ymin = m_OE
ymax = main.W_Take_off
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)

plt.xlabel('x (m)')
plt.ylabel('m (kg)')
plt.title('Loading Phase')
plt.legend()
plt.grid(True)

plt.show()











# unloading phase

x_CoG_TO = x_new

# limits

    # max nose gear load

x = np.linspace(28.39, 30.35, 100)
y = 553928 / (34.828 - x)
plt.plot(x, y, "-", label = "Max Nose Gear Load", color = "black", linestyle = ":")

    # min nose gear load

plt.plot([33.34, 33.34], [m_OE, main.W_Take_off], "-", label = "Min Nose Gear Load", color = "black", linestyle = "--")

# unfueling

px = list()
py = list()

px.append(x_CoG_TO)
py.append(main.W_Take_off)
px.append(x_CoG_TO)
py.append(main.W_Take_off - con.m_fStr)

plt.plot(px, py, '-', label = "Unfueling", color = "red")

# cargo unloading

n_ld = 12
x_ld = list()

for i in range(0, n_ld):
    x_ld.append(54.786-n_ld*1.536+1.536/2+1.536*i)

m_cargo = 6656 # kg
m_ld = m_cargo / n_ld

m_old_it0 = main.W_Take_off - con.m_fStr
x_old = x_CoG_TO

px = [x_old]
py = [m_old_it0]

for i in range(len(x_ld)):
    m_old = m_old_it0 - m_ld*i
    m_new = m_old - m_ld
    x_new = 1/m_new * (x_old * m_old - x_ld[n_ld-i-1] * m_ld)
    px.append(x_new)
    py.append(m_new)
    x_old = x_new
    m_old = m_new

plt.plot(px, py, "-", label = "Cargo Unloading", color = "blue")

# disembarking

m_row_econ = 6*83 + 3*12 # kg
m_row_prem = 4*83 + 2*12 # kg
n_row = 15 + 15 + 1 + 20 # amount of rows
x_row_51 = 52.619 # distance in x direction for row bla from tip
x_row_31 = 36.034
x_row_30 = 34.891
x_row_15 = 19.554
pitch_econ = 32*2.54/100
pitch_prem = 36*2.54/100

px = list()
py = list()

px.append(x_new)
py.append(m_new)

x_old = x_new
m_old_it0 = m_new 

for i in range(len(x_row)):
    m_old = m_old_it0 - sum(m_row[:i])
    m_new = m_old - m_row[i]
    x_new = 1/m_new * (x_old * m_old - x_row[i] * m_row[i])
    px.append(x_new)
    py.append(m_new)
    x_old = x_new
    m_old = m_new

plt.plot(px, py, "-", label = "Disembarking", color = "green")

# plot

xmin = 28.0
xmax = 34.0
ymin = m_OE
ymax = main.W_Take_off
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)

plt.xlabel('x (m)')
plt.ylabel('m (kg)')
plt.title('Unloading Phase')
plt.legend()
plt.grid(True)

plt.show()