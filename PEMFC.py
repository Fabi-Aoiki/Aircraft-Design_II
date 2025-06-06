import numpy as np
import isa as isa
import constants as con
import math
import lhCalc as old
############################################################# Value
#Basic Thermodynamic things

cp = (con.PEMFC_Kappa*con.PEMFC_R_s)/(con.PEMFC_Kappa-1)

#Changig values
h = []
TS0 = []
TT0 = []
PS0 = []
M0 = []
q0 = []
PT0 = []
n=1
while n < con.H_CRUISE:
    h.append(n)
    n = n +100 

n=0
while n < con.ma_max:
    M0.append(n)
    n = n +0.05

for z in M0:
    TS0it = []
    TT0it = []
    PS0it = []
    PT0it = []
    qit = []
    for i in h:
        TS0it.append(isa.isa_model(i,con.dt)[1])
        TT0it.append((isa.isa_model(i,con.dt)[1])*(1+((con.PEMFC_Kappa-1)/(2))*(z**2)))
        PS0it.append(isa.isa_model(i,con.dt)[0])
        #qit.append(((((isa.isa_model(i,con.dt)[3])*z)**2)*(isa.isa_model(i,con.dt)[2]))/2) Erster Versuch mittels Bernouli
        PT0it.append((1+0.5*(-1+con.PEMFC_Kappa)*((z**(2)))**(con.PEMFC_Kappa/(-1+con.PEMFC_Kappa)))) #Zweiter VErsuch Mach Formel auf seite 12 umgestelllt
        qit.append(((1+0.5*(-1+con.PEMFC_Kappa)*((z**(2)))**(con.PEMFC_Kappa/(-1+con.PEMFC_Kappa))))-(isa.isa_model(i,con.dt)[0]))

    TS0.append(TS0it)
    PS0.append(PS0it)
    q0.append(qit)
    TT0.append(TT0it)
    PT0.append(PT0it)




    




#Non Changing Values
PT3 = con.PEMFC_PT_d * (1+ con.PEMFC_dPT_PT)
PT4 = con.PEMFC_PT_d * (1- con.PEMFC_dPT_PT)


#Values From Changing values
##PRc Clac Iteration over M and then hight
PRc = []
for i in PT0:
    PRcint = []
    for x in i:
        PRcint.append(PT3/x)#PT2 = PT0 
    
    PRc.append(PRcint)

##PRt Clac Iteration over M and then hight    
PRt = []
for i in PT0:
    PRtint = []
    for x in i:
        PRtint.append(PT4/x)#PT5 = PT0 
    
    PRt.append(PRtint)


##ETA_fc_stack
ETA_fc_stack = con.PEMFC_a*con.oversizingFc + con.PEMFC_b


##Pel_stack
Pel_Stack = old.calcElPower(old.FlightPhase.cruise, con.PEMFC_powertoweight)[1]
P_stackDesign = old.calcDesignStackPower(Pel_Stack)
P_stackMax = old.calcStackPowerMax(P_stackDesign)



##Mass Flow
mdot = con.PEMFC_Lamda*((Pel_Stack/ (ETA_fc_stack * con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2)))


##TT3 and PC Itération over length of lists the same length


def listlength(liste):
    lg=0#Länge gesamt
    ls=0#Länge Stage
    ns=0#Number of stages
    i = 0
    x = 0
    for i in liste:
        ns = ns +1
        for x in i:
            lg = lg + 1

    ls = lg / ns
    

    return(lg,ls,ns)


lg = listlength(TT0)[0] 
ls = listlength(TT0)[1] 
ns = (listlength(TT0)[2])
ns = int(ns)-1
TT3=[]
TTerm=[]
PC =[]
i=0

while i <= ns:
    TT3i = []
    TTermi=[]
    Prcrun_pre=[]
    TT0run_pre=[]
    PCi = []
    Prcrun_pre.append(PRc[i])
    TT0run_pre.append(TT0[i])

   

    for x,y in zip(TT0run_pre,Prcrun_pre):
        n = 0
        TT3it=[]
        TTermit=[]
        PCit=[]

        while n <= ls-1:

            Prcrun = y[n]
            TT0run = x[n]
            #print(TT0run,Prcrun)
            TT3run = ((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa)))*TT0run))
            TTermrun = ((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa)))))
            PCrun = cp * mdot * TT0run *(TTermrun - 1)
            TT3it.append(TT3run)
            TTermit.append(TTermrun)
            PCit.append(PCrun)
            n = n +1


        TT3.append(TT3it)
        TTerm.append(TTermit)
        PC.append(PCit)
    #TT3.append(TT3i)old idea
    #TTerm.append(TTermi)
    #PC.append(PCi)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(i)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#Pt


lg = listlength(TT3)[0] 
ls = listlength(TT3)[1] 
ns = (listlength(TT3)[2])
ns = int(ns)-1

Pt =[]
i=0
print("---------------------------------------------------------------------")
#print("TT3")
#print(TT3)
print("_--------------------------------------------------------------")
while i <= ns:


    Prtrun_pre=[]
    TT3run_pre=[]
    Pti = []
    Prtrun_pre.append(PRt[i])
    TT3run_pre.append(TT3[i])

   

    for x,y in zip(TT3run_pre,Prtrun_pre):
        n = 0
        Ptit=[]

        while n <= ls-1:

            Prtrun = y[n]
            TT3run = x[n]
            
            Ptrun = cp * mdot * TT3run *(1-pow(Prtrun,(((con.PEMFC_ETA_t_pol)*-1)*(con.PEMFC_Kappa-1))/con.PEMFC_Kappa))
            #print(Ptrun)

            Ptit.append(Ptrun)
            n = n +1



        Pt.append(Ptit)

    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(i)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1

#print(Pt)

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#ETA_fc_anc


lg = listlength(TT0)[0] 
ls = listlength(TT0)[1] 
ns = (listlength(TT0)[2])
ns = int(ns)-1

ETA_fc_anc =[]
i=0

while i <= ns:


    Prtrun_pre=[]
    Prcrun_pre=[]
    TT0run_pre=[]
    Prcrun_pre.append(PRc[i])
    TT0run_pre.append(TT0[i])
    Prtrun_pre.append(PRt[i])


   

    for x,y,z in zip(TT0run_pre,Prtrun_pre,Prcrun_pre):
        n = 0
        ETA_fc_ancit=[]

        while n <= ls-1:

            
            TT0run = x[n]
            Prtrun = y[n]
            Prcrun = z[n]
            
            ETA_fc_ancrun = 1-((1/con.PEMFC_ETA_c_m)*cp*con.PEMFC_Lamda*(1/(ETA_fc_stack*con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2))*TT0run*(((((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))))))/(pow(Prtrun,(((con.PEMFC_ETA_t_pol))*(con.PEMFC_Kappa-1))/con.PEMFC_Kappa)))-1)) 
            
            print(ETA_fc_ancrun)

            ETA_fc_ancit.append(ETA_fc_ancrun)
            n = n +1



        ETA_fc_anc.append(ETA_fc_ancit)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(i)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1

print(ETA_fc_anc)
"""print(f"Das ist TSO{TS0}")
print(f"Das ist PSO{PS0}")"""
"""print(f"Das ist PT4 {PT4}")
print(f"Das ist PT3 {PT3}")
print(f"Das ist PRc {PRc}")"""
