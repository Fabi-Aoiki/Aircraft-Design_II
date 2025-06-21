# ----------------------------------------------------- #
#                                                       #
#     Direct Operating Costs - Aircraft Design II       #
#                                                       #
# ----------------------------------------------------- #

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from isa_model import isa_model as isa
import doc_model as doc


# ----- INPUTS ------- #

mach_cr = 0.785                 # Cruise Mach number [-]
alt_cr = 12000                  # Cruise altitude [m]
r_design = 2600                 # Design range [nm]
pax = 276                       # Number of passengers [-]
m_pax = pax*95                  # Total passengers mass [-]
mtom = 116658                   # MTOM [kg]
oem = 78832                     # OEM [kg]
eng_mass = 2500                 # Engine mass [kg]
stsl = 9000                     # Static thrust at sea-level [N]
m_cargo = 5000                  # Cargo mass [kg]
payload = m_pax + m_cargo       # Payload mass [kg]
m_fuel = 6606                   # Fuel mass [kg]
m_zf = mtom - m_fuel            # MZFM [kg]
n_eng = 4                       # Number of engines [-]
max_fuel = 9375                # Maximum fuel mass [kg] - Related to tank capacity!
m_cargo_fix = 0.8*m_cargo       # Mass of cargo that cannot be exchanged for fuel [kg]

E_RAS = 350.                                # Average revenue per available seat [€]
cargo_rate_kg = 0.6                         # Cargo rate for substitution [€/kg]
eq_pax = m_cargo*cargo_rate_kg/E_RAS        # Equivalent PAX for revenue of cargo weight

rev_rate_pax = 0.1                          # Revenue per available seat km [€/km]
pax_rate = rev_rate_pax/95                  # Passenger mass rate [€/kg.km]
cargo_rate = 95*pax_rate*eq_pax/m_cargo     # Cargo mass rate [€/kg,km]

rev_rate_kg = (cargo_rate*m_cargo + pax_rate*m_pax)/payload     # Average revenue rate per kg of payload [€/kg]

# ----- ANALYSIS ----- #

V_cruise = mach_cr*isa(alt_cr, 0)[3]        # Get cruise speed [m/s] from Mach number
nm2km = 1.852                               # Convert nm to km

max_payload = payload   # m_zf - oem

rc = int(10*round(0.1*max_fuel/(m_fuel/r_design), 0))
rb = int(10*round(0.1*((r_design/m_fuel)*(mtom - max_payload - oem)), 0))
mc = mtom - max_fuel - oem

PL = [max_payload, max_payload, mc, 0]          # Payload masses [kg]
R = [0, rb, rc, rc+100]                         # Range [nm]
# F_res = [0.031, 0.045, 0.048, 0.05]           # Percentage of fuel reserves wrt range diagram
F_res = [0, 0, 0, 0]                            # Reserves already included in fuel calculation!!

RANGE = []
dr = 10
for i in range(len(R)-1):
    for j in range(R[i]+dr, R[i+1]+dr, dr):
        RANGE.append(j)


pl_data = []
tom_data = []
fuel_data = []
range_nm = []
range_km = []
doc_r = []
doc_ask = []
doc_comp = []
engine_cap_frac = []
bepl = []
be_pax = []
seat_cost = []
pax_number = []

for r in RANGE:
    tom = mtom
    if r <= R[1]:
        m_fuel_res = r*(F_res[1] - F_res[0])/R[1] + F_res[0]
        tom = (mtom - (mtom - (oem + PL[0]) / (1 - m_fuel_res))) + r*(mtom - (oem + PL[0]) / (1 - m_fuel_res))/R[1]
        m_fuel = tom - (oem + PL[0] + m_fuel_res * tom)
        payload = max_payload
        pax = min(pax, int(payload/95))
    elif r <= R[2]:
        m_fuel_res = r * (F_res[2]-F_res[1])/(R[2]-R[1]) + F_res[1]-((F_res[2]-F_res[1])/(R[2]-R[1]))*R[1]
        payload = PL[1] + (r - R[1]) * (PL[2]-PL[1])/(R[2]-R[1])
        m_fuel = tom - (oem + payload + m_fuel_res * tom)
        pax = min(pax, int((payload - m_cargo_fix) / 95))
    elif r <= R[3]:
        tom = (r - R[2])*(-PL[2]/(R[3]-R[2])) + (R[2]*PL[3]/(R[3]-R[2]) + mtom)
        m_fuel_res = r * (F_res[3]-F_res[2])/(R[3]-R[2]) + F_res[2]-((F_res[3]-F_res[2])/(R[3]-R[2]))*R[2]
        payload = PL[2] + (r - R[2]) * (PL[3] - PL[2]) / (R[3] - R[2])
        m_fuel = tom - (oem + payload + m_fuel_res * tom)
        pax = int((payload - m_cargo_fix) / (m_pax / 95))
    else:
        break

    pl_data.append(payload)
    tom_data.append(tom)
    fuel_data.append(m_fuel)
    pax_number.append(pax)

    range_nm.append(r)
    range_km.append(r*nm2km)
    cycles = doc.flight_cycles(V_cruise, r*nm2km)
    C1 = round(doc.capital_cost(oem, eng_mass, n_eng)[0])
    C2 = round(doc.crew_cost(pax))
    C3 = round(doc.maintenance_cost(oem, n_eng, stsl, r*nm2km, V_cruise)*doc.flight_cycles(V_cruise, r*nm2km))
    [C4, C5, C6, C7] = doc.route_costs(doc.flight_cycles(V_cruise, r*nm2km), m_fuel, mtom-oem-m_fuel, mtom, r*nm2km)

    DOC = [C1, C2, C3, C4, C5, C6, C7]
    engine_cap_frac.append(doc.capital_cost(oem, eng_mass, n_eng)[1])
    doc_comp.append(DOC)

    doc_r.append(sum(DOC))
    if pax > 0:
        doc_ask.append(sum(DOC)/(cycles*r*nm2km*pax))
        seat_cost.append(sum(DOC)/(cycles*pax))
    else:
        doc_ask.append(doc_ask[-1])
        seat_cost.append(seat_cost[-1])

    bepl.append(sum(DOC)/(cycles*r*nm2km*rev_rate_kg))
    be_pax.append(sum(DOC)/(r*nm2km*cycles*rev_rate_pax))


comp_db = pd.DataFrame(doc_comp, columns=['Capital', 'Crew', 'Maintenance', 'Fuel', 'Payload Handling', 'Landing Fees',
                                          'ATC Fees'])
cost_db = pd.DataFrame(list(zip(range_nm, range_km, pl_data, fuel_data, tom_data, doc_r, doc_ask, engine_cap_frac)),
                       columns=['Range [NM]', 'Range [km]', 'Payload [kg]', 'Fuel [kg]', 'Take-off Mass [kg]',
                                'DOC', 'ASK', 'Engine Cost Share'])

costs_data = pd.concat([cost_db, comp_db], axis='columns')

costs_data.set_index("Range [NM]", inplace=True)
costs_data.to_csv('out.csv')

costs_at_sr = pd.Series(costs_data.loc[round(r_design/100, 0)*100, 'Capital':'ATC Fees'])

# Find min cost

opt_range = costs_data['ASK'].idxmin()

# Payload-Range Diagram

plt.figure(1, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(range_nm, pl_data, label='Payload')
plt.plot(range_nm, tom_data, label='Take-off Mass')
plt.plot(range_nm, fuel_data, label='Fuel')
plt.ylabel('Mass [kg]')
plt.xlabel('Range [nm]')
plt.plot([opt_range, opt_range], [0, 200000], '--', color='grey')
plt.ylim([0, 120000])
plt.xlim([0, 3500])
plt.legend()
plt.grid()
plt.savefig('Figures/payload_range.png', bbox_inches='tight')

# Cost-Range

plt.figure(2, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(range_nm, doc_ask, label='ASK')
plt.ylabel('Operating Costs [€/ASK]')
plt.xlabel('Range [nm]')
plt.ylim([0, 0.2])
plt.xlim([0, 3500])
plt.grid()
plt.savefig('Figures/cask.png', bbox_inches='tight')

# Costs Breakdown

set_range = opt_range   # Range in Nautical Miles

costs_at_sr = pd.Series(costs_data.loc[set_range, 'Capital':'ATC Fees'])

plt.figure(3, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.pie(costs_at_sr, labels=['Capital', 'Crew', 'Maintenance', 'Fuel', 'Payload Handling', 'ATC Fees', 'Landing Fees'],
        autopct='%1.1f%%', pctdistance=0.75, labeldistance=1.1,
        explode=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], shadow=False, startangle=20,
        colors=['#727a9a', '#838aa7', '#949ab4', '#a5abc2', '#b6bbcf', '#c7cbdc', '#d8dbe9'])
plt.title('DOC Breakdown at Operating Range - ' + str(set_range) + ' NM')

centre_circle = plt.Circle((0, 0), 0.50, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.savefig('Figures/cost_breakdown.png', bbox_inches='tight')

# Break-even

plt.figure(4, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(range_nm, pl_data, label='Payload')
plt.plot(range_nm, bepl, label=f'BEPL {1000*rev_rate_kg:.2} @ €/ton')
plt.ylabel('Mass [kg]')
plt.xlabel('Range [nm]')
plt.ylim([0, 35000])
plt.xlim([0, 3500])
plt.legend()
plt.grid()
plt.savefig('Figures/break-even_payload.png', bbox_inches='tight')

# Break-even Pax

plt.figure(5, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(range_nm, np.divide(np.subtract(pl_data, m_cargo), 95), label='Max Capacity', linestyle='--', color='k' , alpha=0.5)
plt.plot(range_nm, np.divide(np.subtract(pl_data, m_cargo), 95/0.8), label='80% Capacity')
plt.plot(range_nm, be_pax, label=f'Break-even PAX @ {rev_rate_pax:.2} €/AS')
plt.ylabel('PAX [-]')
plt.xlabel('Range [nm]')
plt.ylim([0, 300])
plt.xlim([0, 3500])
plt.legend()
plt.grid()
plt.savefig('Figures/break-even_pax.png', bbox_inches='tight')

# Seat Cost vs Range

plt.figure(6, figsize=(10, 7), dpi=130)
plt.rcParams.update({'font.size': 14})
plt.plot(range_nm, seat_cost, label=f'Seat Cost')
plt.plot([opt_range, opt_range], [0, 200000], '--', color='grey')
plt.ylabel('Seat Cost [€]')
plt.xlabel('Range [nm]')
plt.ylim([0, 400])
plt.xlim([0, 3500])
plt.legend()
plt.grid()
plt.savefig('Figures/seat_cost.png', bbox_inches='tight')

plt.show()
