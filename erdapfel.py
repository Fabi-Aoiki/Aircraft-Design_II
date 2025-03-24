import matplotlib.pyplot as plt
import main
import constants as con
import numpy as np

# loading phase

x_CoG_OE = main.x_CoG
m_OE = main.Momenten_Summe['Weights']

# limits

    # max nose gear load

x = np.linspace(28.39, 30.35, 100)
y = 553928 / (34.828 - x)
plt.plot(x, y, "-", label = "Max Nose Gear Load")

# fueling

px = list()
py = list()

px.append(x_CoG_OE)
py.append(m_OE)
px.append(x_CoG_OE)
py.append(m_OE + con.m_fStr)

plt.plot(px, py, 'o')
plt.plot(px, py, '-', label = "Fueling")

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

x_alt = x_CoG_OE

for i in range(1, n_row+1):
    j = n_row - i + 1
    if j > 31:
        m_cur = m_OE + con.m_fStr + m_row_econ * i
        x_cur = x_row_51-pitch_econ*(i-1)
        x_neu = (x_alt*(m_cur-m_row_econ) + x_cur*m_row_econ)/ m_cur
        px.append(x_neu)
        py.append(m_cur)
        x_alt = x_neu
    elif j == 31:
        m_cur = m_OE + con.m_fStr + m_row_econ * i
        x_cur = x_row_31
        x_neu = (x_alt*(m_cur-m_row_econ) + x_cur*m_row_econ)/ m_cur
        px.append(x_neu)
        py.append(m_cur)
        x_alt = x_neu
    elif j < 31 and j > 15:
        m_cur = m_OE + con.m_fStr + m_row_econ * i
        x_cur = x_row_30-pitch_econ*(i-1)
        x_neu = (x_alt*(m_cur-m_row_econ) + x_cur*m_row_econ)/ m_cur
        px.append(x_neu)
        py.append(m_cur)
        x_alt = x_neu
    elif j <= 15:
        m_cur = m_OE + con.m_fStr + m_row_econ * 36 + m_row_prem*(i-36)
        x_cur = x_row_15-pitch_prem*(i-1)
        x_neu = (x_alt*(m_cur-m_row_econ) + x_cur*m_row_econ)/ m_cur
        px.append(x_neu)
        py.append(m_cur)
    else:
        print("Wrong row index reached. Please review.")

plt.plot(px, py, "-", label = "Boarding")

# cargo loading



xmin = 27.5
xmax = 32.5
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