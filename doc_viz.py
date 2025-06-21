from matplotlib import pyplot as plt
import numpy as np
import csv


def get_data(filename):
    range_km = []
    payload = []
    fuel = []
    tom = []
    doc = []
    ask = []
    capital = []
    crew = []
    maintenance = []
    fuel_cost = []
    payload_handling = []
    landing_fee = []
    atc_fee = []

    with open(filename) as data_base:
        heading = next(data_base)
        reader = csv.reader(data_base)
        for row in reader:
            range_km.append(float(row[1]))
            payload.append(float(row[2]))
            fuel.append(float(row[3]))
            tom.append(float(row[4]))
            doc.append(float(row[5]))
            ask.append(float(row[6]))
            capital.append(float(row[8]))
            crew.append(float(row[9]))
            maintenance.append(float(row[10]))
            fuel_cost.append(float(row[11]))
            payload_handling.append(float(row[12]))
            landing_fee.append(float(row[13]))
            atc_fee.append(float(row[14]))

    return range_km, payload, fuel, tom, doc, ask, capital, crew, maintenance, fuel_cost, payload_handling, \
        landing_fee, atc_fee


# ----- LOAD DATA ------ #

path_Baseline = './out.csv'

baseline = get_data(path_Baseline)

list_data = [baseline]
names = ['Baseline']

Optimal_Range = 2650

# ----- Payload Range ------ #

plt.figure(1, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(baseline[0], baseline[1], label='Baseline')
# plt.plot(concept[0], concept[1], label='Concept')
plt.ylabel('Mass [kg]')
plt.xlabel('Range [km]')
plt.plot([Optimal_Range*1.852, Optimal_Range*1.852], [0, 26000], '--', color='grey', label='Design Range')
plt.ylim([0, 35000])
plt.xlim([0, 3500*1.852])
plt.legend()
plt.grid()
plt.savefig('Figures/payload_range.png', bbox_inches='tight')


# ----- Weights Range ------ #


plt.figure(2, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(baseline[0], baseline[3], color='tab:blue', label='Baseline')
# plt.plot(concept[0], concept[3], color='tab:orange', label='Concept')
plt.ylabel('Mass [kg]')
plt.xlabel('Range [km]')
plt.plot([Optimal_Range*1.852, Optimal_Range*1.852], [0, 120000], '--', color='grey', label='Design Range')
plt.ylim([20000, 120000])
plt.xlim([0, 3500*1.852])
plt.legend()
plt.grid()
plt.savefig('Figures/tom_range.png', bbox_inches='tight')


# ----- DOC Range ------ #


plt.figure(3, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(baseline[0], baseline[5], color='tab:blue', label='Baseline')
# plt.plot(concept[0], concept[5], color='tab:orange', label='Concept')
plt.ylabel('CASK [€]')
plt.xlabel('Range [km]')
plt.plot([Optimal_Range*1.852, Optimal_Range*1.852], [0, 0.0633], '--', color='grey', label='Design Range')
plt.ylim([0, 0.15])
plt.xlim([0, 3500*1.852])
plt.legend()
plt.grid()
plt.savefig('Figures/cask_range.png', bbox_inches='tight')


# ----- DOC and Payload Range (Christoph) ------ #

plt.clf()
plt.cla()

fig, ax1 = plt.subplots()

ax1.plot(baseline[0], baseline[5], color='tab:blue', label='CASK')
ax1.set_ylabel('CASK (€)')
ax1.set_xlabel('Range (km)')

ax2 = ax1.twinx()
ax2.plot(baseline[0], baseline[1], color='tab:red', label='Payload')
ax2.set_ylabel('Payload (kg)')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')

ax1.grid(True) 
ax1.set_ylim(0, 0.2)
plt.xlim(0,6900)

plt.savefig('Figures/cask_payload_range.png', bbox_inches='tight')


# ----- Breakdown at Design Range ------ #

range_loc = baseline[0].index(Optimal_Range*1.852)


costs = ('Capital', 'Crew', 'Maintenance', 'Fuel', 'Payload Hand.', 'Landing Fees', 'ATC Fees')

x = np.arange(len(costs))
bar_width = 0.5
multiplier = 1.5

fig, ax = plt.subplots(figsize=(15, 8), dpi=120)

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

for j, case in enumerate(list_data):
    offset = bar_width * multiplier
    rects = ax.bar(x[0] + offset, case[6][range_loc]/1e6, bar_width, color=colors[j], label=names[j])
    rects = ax.bar(x[0] + offset + 1, case[7][range_loc]/1e6, bar_width, color=colors[j])
    rects = ax.bar(x[0] + offset + 2, case[8][range_loc]/1e6, bar_width, color=colors[j])
    rects = ax.bar(x[0] + offset + 3, case[9][range_loc]/1e6, bar_width, color=colors[j])
    rects = ax.bar(x[0] + offset + 4, case[10][range_loc]/1e6, bar_width, color=colors[j])
    rects = ax.bar(x[0] + offset + 5, case[11][range_loc]/1e6, bar_width, color=colors[j])
    rects = ax.bar(x[0] + offset + 6, case[12][range_loc]/1e6, bar_width, color=colors[j])

    multiplier += 1

    print(names[j], case[4][range_loc])

ax.set_ylabel('Yearly Cost [Millions of €]')

ax.legend(loc='upper left', ncols=4)
ax.set_xticks(x + 1.5*bar_width, costs[:7])
ax.set_ylim(0, 25)
plt.savefig('Figures/breakdown.png', bbox_inches='tight')
plt.show()
