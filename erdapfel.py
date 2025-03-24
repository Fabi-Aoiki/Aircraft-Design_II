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
m_row_prem = 42*83 + 2*12 # kg
n_row = 15 + 15 + 1 + 20 # amount of rows
x_row_51 = 50 # distance in x direction for row bla from tip
x_row_31 = 35
x_row_30 = 34
x_row_15 = 20
pitch_econ = 32*2.54/100
pitch_prem = 36*2.54/100

px = list()
py = list()

px.append(x_CoG_OE)
py.append(m_OE + con.m_fStr)

for i in range(1, n_row+1):
    j = n_row - i + 1
    if j > 31:
        x_new = (x_CoG_OE*(m_OE+con.m_fStr)+(x_row_51-pitch_econ*(i-1))*m_row_econ)/(m_OE + con.m_fStr + m_row_econ*i)
        px.append(x_new)
        py.append(m_OE + con.m_fStr + m_row_econ*i)
    elif j == 31:
        pass
    elif j < 31 and j > 15:
        pass
    elif j <= 15:
        pass
    else:
        print("Wrong row index reached. Please review.")
    
plt.plot(px, py, '-', label = "Boarding")

print(py)

# cargo loading

xmin = 20
xmax = 40
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