#Basic 

l_fus_s=62.7 # meter
h_fus_s=5.5 # meter
b_fus_s=4.5 # meter






#General
Wto = 90350 * 9.806 #maxium takeoff weight base version in N
Wf = 5782 * 9.806 #fuel weight in Newton Base Version
#Wto = 100094 * 9.806 #STRETCH: maximum takeoff weight stretch version in N
Wto_stretch = 100094 * 9.806 #STRETCH: maximum takeoff weight stretch version in N
#Wf = 6913 * 9.806 #fuel weight in N, Stretch Version
# V_CRUISE = 140 #crusing speed in m/s - disused calc through general calc from mach
ntrans = 0.99 #transmission efficency (gearbox)
nprop = 0.9 #propeller efficeny, variable pitch.
AR = 10 #Aspect Ratio
e0 = 0.8 #Oswald factor, see cruise, take off and landing
H_CRUISE = 12200 #crusing altitude in m
#H_CRUISE = 11000
H_CRUISE_OEI = 3050 #crusing altidude OEI in m
N_E = 4 #number of engines
N_prop = 4 #number of Blades on the Prop
ToOEI = 80000 #XXX NOT RIGHT VALUE XXX
SeCe = 40000/3.28084 #Service Ceiling [m]CHECK VALUE!!!!
vvre =  100*0.00508 # Minimum Vertikal Speed in [m/s] CHECK VALUE!!!!
dt = 0  # no temperature difference Temperature(ISA) CHECK VALUE!!!!
cd0 = 0.017 #parasitic drag
#cd0 = 0.019 #str
ma = 0.75  # chosen Mach number for flight CHECK VALUE!!!!
ma_stretch = 0.785
ma_max = 0.8 #max Mach number; used for wing dimensioning
#ma_max = 0.785 #max speed stretch version
#ma_max = 0.785
n_zw = 1 #Load Multiplier Vertical Trajectory
g0 = 9.806 #Gravitationsbeschleunigung
WS = 4500 #Wing Loading as determined from power estimation
#WS = 4987 #WS Stretch
WS_stretch = 4987
rhoLH = 70.85 #density of liquid hydrogen in kg/m^3
m_fStr = 6606 #fuel mass of the stretch variant in kg
m_fBas = 5782 #fuel mass of the base variant in kg
P_b = 20447989*(10**-3) #kW - (System?)Power base variant
P_s = 22653528*(10**-3) #kW - (System?)Power stretch variant
P_elNonProp = 250 * 10^3 #W Elektrische Leistung ohne Motor(en)
P_elNonPropToMotors = 0.0625 #percent electric power relation systems to electric motors
l_cab = 52 #length of cabin stretched
pax_s = 276 # Pax stretch


#Cruise chosen values
epsilion = 1/18 #glide ratio 1/(L/D) - middle of range for commercial aircraft turbofans due to worse aerodynamics of LHE aircaft compared to conventional
#epsilion = (1/18)*0.85 #STRETCH VERSION
C_L = 0.5 #lift coefficient cruise
e0_cruise = 0.83
TRthr_CR = 0.8
n_prop_CR = 0.9

#Choosen Values Take Off
u_roll = 0.03 #Rollreibungskoeffizient
u_aero  = 0.13 #Luftreibungskoeffizient
TRthr_TO = 1 #Power Throttle Ratio
n_prop_TO = 0.7 #Propulsion Efficiency
n_prop_TOCl = 0.8 #Propulsion Efficiency during initial climb phase
c_Lmax_Start = 2.1 #1.8 #Coefficient of lift during Take Off, with Flaps and Slats
f_LOF = 1.08 #Speed Coefficient to calculate v_LOF from v_s1g
h_scr = 10.668 #35 ft obstacle height in meters. CONSTANT! DO NOT CHANGE!
dT_TO = 0 #Temperature difference at take off in K
h_TO = 0 #height above mean sea level in m
e_TO=0.7 #ossi
cd0_to = 0.04
epsilon_TO = 1/10 #1/10 #Take-Off Epsilon Annahme
pwsafetyfactor = 1.05


#Choosen Values Climb OEI
Probef_OEI = 0.80
Transef_OEI= 0.99
TRthr_OEI = 1

# #Choosen Values Climb service
Probef_Se = 0.90
Transef_Se = 0.99
TRthr_Se = 0.9



#Choosen Values Landing
h_50=50*0.3048 #height in Meters 50ft.
v_50 = 140*0.514444 #Angabe: Maximum approach speed at maximum landing mass 140 kts (CAS)
v_s = v_50/1.23
Epsilon_Landing = 8
if N_E > 3: v_L = v_s*1.08
else: v_L = v_s*1.13 # for 2 Enginies, 1.08 for more Engines
S = 250 #Wing Surface Area, to Dicuss
b_M = -9.81/3 #Braking deacceleration [m/s^2], g/2 is appropriate
c_Lmax_Landing = 2.5#Angabe: Maximum lift coefficient in landing Configuration: 2.2 … 2.8 because we have an average plane
safety = 0.6 #According to EASA CAT.POL.A.230 the aircraft must come to a standstill after 60% (or 70% for Turboprops) of the available landing distance.
s_L_max = 1900#Maximum Landing Distance lt. Angabe 1900m
landing_altitude = 0
landing_dT = 0


#wing area calculation
k_r = 0.98 #fuel factor at cruise height
k_n = 1.3 #maneuvering factor
k_av = 1.1 #local lift coefficient increase
k_trim = 1.1 #cl increase due to trimming
taper = 0.275 #taper ratio lambda of wing

#empennange dimensioning
l_f = 54 #overall length fuselage in m
k_lf = 0.5 #correction factor for determining distance between ACs of wing and stabilizer
coef_h = 0.904 #volume coefficient horizontal stabilizer
coef_v = 0.074 #volume coefficient vertical stabilizer
AR_h = 4
AR_v = 1.2
taper_h = 0.4 #taper ratio horizontal stabilizer
taper_v = 0.6 #taper ratio vertical stabilizer
sweep_h = 28 #sweep angle of horizontal stabilizer in degrees
sweep_v = 28 #sweep angle for vertical stabilizer in degrees

#chosen values lh calc
safteyFacMinTankVol = 1.072
n_FcAnc = 0.93
oversizingFc = 0.4 #percent
Dens_powerBostBat = 7.5 #kWh/l boooooooooooooster battery
DensW_powerBostBat = 10 #kWh/kg boooooooooooooster battery
n_FCcool = 0.8

#Wing Thorenbeck Weight

const = 4.58 * 10**(-3) # Empirische Konst aus Buch dim los
bref = 1.905 # Meter Empi
klamb = (1+taper)**(0.4) #Dumm
ke = 0.9 #Def by engines num#
kuc = 0.95 #Under mounted on fuse

Lamda_LE = 24.25 #Sweep an der vorderkante (slats)
Lamda_12 = 18.55 #Sweep mittellinie

const_kst = 9.06*10**(-4)#Kosnt in kst

vD = 200.6 # m/s, Georg hat das gerechnet
kb = 1.0 #Krakträger Wing

cons_Wtef = 2.706 #Jaaaa

kf1 = 1.3 #Flap config (Double slot)
kf2 = 1 #Flap Vanes (Easy)

delta_f = 40 #Flap angle def

Lamda_f = 12.57 #Flap sweep

t_c_f = 0.13 #NEEDS CHECK

cons_Wlef = 30 #kg/m^2 bei ca 90 ton take off weight slats weight 
S_slat = 30 #m^2


#Emp Thorenbeck

k_wt = 0.64 #Nein

Cor_factor_Ttail = 1.05 #NOT in Thorenbeck assumption by me. 

Lambda_h = 25 # ° sweep angle (quarter line) horizontal tail wing
Lambda_v = 25 # ° sweep angle (quarter line) vertical tail wing

#Fus Tohrenbeck

kwf = 0.23
lt = 29.83 # m Length fus to tail 
hf = 5.48 # m height fus
bf = 4.5 #m with fus
SG = 755 #m^2 wetted fuselage area


#Under Thorenbeck

kuc = 1.08 #Hiegh wing
A_u_m = 18.1
B_u_m = 0.131
C_u_m = 0.019
D_u_m = 2.23*10**(-5)

A_u_n = 9.1
B_u_n = 0.082
C_u_n = 0
D_u_n = 2.97*10**(-6)

#Control Thorenbeck

ksc = 0.44 # Wert für control anname da neu

#Engine Thorenbeck

Wn_constant = 0.0635 #kg per PS



kpg = 1.35 

M_engine = 750 #Engine Elektro in kg

#Service Thorenbeck

kieg = 0.347 

RC = 6800 #km

mOE_s = 62300 #kg

S_human = 1.8 #m^2 (Paper)

k_human = 58 #w/m^2 (Paper)

Q_ppax = S_human * k_human # W

Q_lhi = 16817.7 # W Wärme aufnahme des LH


################################################################

#Seating 

W_eco_pp = 8 #kg Recaro R1
W_bus_pp = 10 #kg Recaro R2


# Plane Geometry for CoG

MAC = 4.916



####################################
#PEMFC
##########
PEMFC_Lamda = 1.8
PEMFC_dPT_PT=0.08108
PEMFC_PT_d=18500 #N/m^2
PEMFC_ETA_c_pol = 0.72
PEMFC_ETA_t_pol = 0.85
PEMFC_ETA_c_m = 0.95
PEMFC_R_s=287.05 
PEMFC_Kappa=1.4
PEMFC_LHV = 1.2*(10**8) #J/kg
PEMFC_M_H2= 2.0159*(10**(-3)) #kg/mol
PEMFC_M_air=28.965*(10**(-3))
PEMFC_y_air_o2=0.21
PEMFC_a = -0.213
PEMFC_b = 0.67
PEMFC_powertoweight = 20










