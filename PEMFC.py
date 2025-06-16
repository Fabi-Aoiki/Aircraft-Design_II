import numpy as np
import isa as isa
import constants as con
import math
import lhCalc as old
import matplotlib.pyplot as plt
import itertools
############################################################# Value
#Basic Thermodynamic things

cp = (con.PEMFC_Kappa*con.PEMFC_R_s)/(con.PEMFC_Kappa-1)

#Changig values
h = []
"""TS0 = []
TT0 = []
PS0 = []
M0 = []
q0 = []
PT0 = []
"""

TS0n = []
TT0n = []
PS0n = []
M0n = []
q0n = []
PT0n = []

M1 =[]
v0 = []
vmax=0.8*295
n=0
while n < con.H_CRUISE:
    h.append(n)
    n = n +50 

"""n=0
while n <= con.ma_max:
    M0.append(n)
    n = n +(con.ma_max/10)"""


n=0 #Vmin additition 
while n <= vmax:
    v0.append(n)
    n = n +(vmax/10)
v0.append(vmax)


"""for z in M0:
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
    PT0.append(PT0it)"""


for z in v0:
    TS0it = []
    TT0it = []
    PS0it = []
    PT0it = []
    qit = []
    M1it = []
    for i in h:
        TS0run=(isa.isa_model(i,con.dt)[1])
        PS0run=(isa.isa_model(i,con.dt)[0])
        #qrun=8900
        #qrun=(((z**2)*(1))/2)
        qrun=(((z**2)*(isa.isa_model(i,con.dt)[2]))/2) #Erster Versuch mittels Bernouli
        PT0run=(PS0run + qrun)
        M1run=(((2/((con.PEMFC_Kappa)-1))*(((PT0run/PS0run)**(((con.PEMFC_Kappa)-1)/(con.PEMFC_Kappa)))-1))**0.5)
        TT0runr=((TS0run)*(1+(((con.PEMFC_Kappa-1)/(2))*(M1run**2))))



        TS0it.append(TS0run)
        PS0it.append(PS0run)
        qit.append(qrun)
        PT0it.append(PT0run)
        M1it.append(M1run)
        TT0it.append(TT0runr)
        #PT0it.append((1+0.5*(-1+con.PEMFC_Kappa)*((z**(2)))**(con.PEMFC_Kappa/(-1+con.PEMFC_Kappa)))) #Zweiter VErsuch Mach Formel auf seite 12 umgestelllt
        #qit.append(((1+0.5*(-1+con.PEMFC_Kappa)*((z**(2)))**(con.PEMFC_Kappa/(-1+con.PEMFC_Kappa))))-(isa.isa_model(i,con.dt)[0]))

    TS0n.append(TS0it)
    PS0n.append(PS0it)
    q0n.append(qit)
    TT0n.append(TT0it)
    PT0n.append(PT0it)
    M1.append(M1it)

    




#Non Changing Values
PT3 = con.PEMFC_PT_d * (1+con.PEMFC_dPT_PT)
PT4 = con.PEMFC_PT_d * (1-con.PEMFC_dPT_PT)


#Values From Changing values
##PRc Clac Iteration over M and then hight
"""PRc = []
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
    
    PRt.append(PRtint)"""

############################################################################################################################
#New

PRcn = []
for i in PT0n:
    PRcint = []
    for x in i:
        PRcint.append(PT3/x)#PT2 = PT0 
        #print(x)
    
    PRcn.append(PRcint)

##PRt Clac Iteration over M and then hight    
PRtn = []
for o in PT0n:
    PRtint = []
    for f in o:
        PRtint.append(PT4/f)#PT5 = PT0 
    
    PRtn.append(PRtint)
############################################################################################################################
#New



##Pel_stack
Pel_Stack = 29.21e6 #old.calcElPower(old.FlightPhase.cruise, con.PEMFC_powertoweight)[1]
#P_stackDesign = old.calcDesignStackPower(Pel_Stack)
P_stackMax = 63.29e6 #old.calcStackPowerMax(P_stackDesign)
##ETA_fc_stack
#ETA_fc_stack = con.PEMFC_a*(0.33) + con.PEMFC_b
ETA_fc_stack = con.PEMFC_a*(Pel_Stack/P_stackMax) + con.PEMFC_b



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

"""
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
"""
###################################################################################################################################################
lg = listlength(TT0n)[0] 
ls = listlength(TT0n)[1] 
ns = (listlength(TT0n)[2])
ns = int(ns)-1
TT3n=[]
TTermn=[]
PCn =[]
i=0

while i <= ns:
    TT3i = []
    TTermi=[]
    Prcrun_pre=[]
    TT0run_pre=[]
    PCi = []
    Prcrun_pre.append(PRcn[i])
    TT0run_pre.append(TT0n[i])

   

    for x,y in itertools.zip_longest(TT0run_pre,Prcrun_pre):
        n = 0
        TT3it=[]
        TTermit=[]
        PCit=[]

        while n <= ls-1:

            Prcrun = y[n]
            TT0run = x[n]
            #print(TT0run,Prcrun)
            TT3run = ((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))))*TT0run)
            TTermrun = ((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa)))))
            PCrun = cp * mdot * TT0run *(TTermrun - 1)
            TT3it.append(TT3run)
            TTermit.append(TTermrun)
            PCit.append(PCrun)
            n = n +1


        #PCit.reverse()
        TT3n.append(TT3it)
        TTermn.append(TTermit)
        PCn.append(PCit)
    #TT3.append(TT3i)old idea
    #TTerm.append(TTermi)
    #PC.append(PCi)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(i)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
"""########################
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

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")"""


########################
#Pt


lg = listlength(TT3n)[0] 
ls = listlength(TT3n)[1] 
ns = (listlength(TT3n)[2])
ns = int(ns)-1

Ptn =[]
i=0
print("---------------------------------------------------------------------")
#print("TT3")
#print(TT3)
print("_--------------------------------------------------------------")
while i <= ns:


    Prtrun_pre=[]
    TT3run_pre=[]
    Pti = []
    Prtrun_pre.append(PRtn[i])
    TT3run_pre.append(TT3n[i])

   

    for x,y in itertools.zip_longest(TT3run_pre,Prtrun_pre):
        n = 0
        Ptit=[]

        while n <= ls-1:

            Prtrun = y[n]
            TT3run = x[n]
            
            Ptrun = cp * mdot * TT3run *(1-(Prtrun**((((con.PEMFC_ETA_t_pol)*-1)*(con.PEMFC_Kappa-1))/con.PEMFC_Kappa)))
            #print(Ptrun)

            Ptit.append(Ptrun)
            n = n +1


        #Ptit.reverse()
        Ptn.append(Ptit)

    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(i)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1

#print(Pt)

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#ETA_fc_anc


"""lg = listlength(TT0)[0] 
ls = listlength(TT0)[1] 
ns = (listlength(TT0)[2])
ns = int(ns)-1

ETA_fc_anc =[]
RETA_fc_anc=[]# 1- ETA (Revese Eta)
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
        RETA_fc_ancit=[]

        while n <= ls-1:

            
            TT0run = x[n]
            Prtrun = y[n]
            Prcrun = z[n]
            
            ETA_fc_ancrun = 1-((1/con.PEMFC_ETA_c_m)*cp*con.PEMFC_Lamda*(1/(ETA_fc_stack*con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2))*TT0run*(((((Prcrun**(((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))))))/(pow(Prtrun,(((con.PEMFC_ETA_t_pol))*(con.PEMFC_Kappa-1))/con.PEMFC_Kappa)))-1)) 
            RETA_fc_ancrun = 1-ETA_fc_ancrun

            ETA_fc_ancit.append(ETA_fc_ancrun)
            RETA_fc_ancit.append(RETA_fc_ancrun)
            n = n +1



        ETA_fc_anc.append(ETA_fc_ancit)
        RETA_fc_anc.append(RETA_fc_ancit)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(i)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1

print(ETA_fc_anc)
"""

#h.reverse()

lg = listlength(TT0n)[0] 
ls = listlength(TT0n)[1] 
ns = (listlength(TT0n)[2])
ns = int(ns)-1

ETA_fc_ancn =[]
RETA_fc_ancn=[]# 1- ETA (Revese Eta)
minl=[]
i=0


#PRcn.reverse()
#PRtn.reverse()
#TT0n.reverse()
while i <= ns:


    Prtrun_pre1=[]
    Prcrun_pre1=[]
    TT0run_pre1=[]
    Prcrun_pre1.append(PRcn[i])
    TT0run_pre1.append(TT0n[i])
    Prtrun_pre1.append(PRtn[i])
    
    
    #Prcrun_pre1.reverse()
    #TT0run_pre1.reverse()
    #Prtrun_pre1.reverse()



    for x1,y1,z1 in itertools.zip_longest(TT0run_pre1,Prtrun_pre1,Prcrun_pre1):
        n = 0
        ETA_fc_ancit=[]
        RETA_fc_ancit=[]
        
        
        #x1.reverse()
        #y1.reverse()
        #z1.reverse()

        while n <= ls-1:

        
            TT0run1 = x1[n]
            Prtrun1 = y1[n]
            Prcrun1 = z1[n]

            

            #print(x[n],y1[n],z1[n])



            PRc_hoch = ((0.4)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))
            PRT_hoch = ((con.PEMFC_ETA_t_pol)*((0.4))/con.PEMFC_Kappa)


            Ltr = TT0run1*((((Prcrun1**(PRc_hoch)))/(Prtrun1**(PRT_hoch)))-1)


            #Ltrr = TT0run1*(1-(((Prcrun1**(PRc_hoch)))/(Prtrun1**(PRT_hoch))))
            ETA_fc_ancrun = (1- (((1/con.PEMFC_ETA_c_m))*cp*con.PEMFC_Lamda*(1/(ETA_fc_stack*con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2)) * Ltr))

            RETA_fc_ancrun = ((1-ETA_fc_ancrun))
            #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            #print(f"Das ist der Wirkungsgrad  {ETA_fc_ancrun} , Das ist der Gegen Wirkungsgrad {RETA_fc_ancrun} , Das ist der letzte Term {Ltr}")
            
            #print(f"Das ist PRC  {Prcrun1} , Das ist PRT {Prtrun1} , Das ist der letzte Term reverse  {Ltr}")
            #print(f"Controll Term {(Prcrun1/Prtrun1)}")
            #print(f"Hoch vergleich {(((PRc_hoch))/(PRT_hoch))}") Hoch zahlen können ausggeschlossen werden
            #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            ETA_fc_ancit.append(ETA_fc_ancrun)
            RETA_fc_ancit.append(RETA_fc_ancrun)
            n = n +1

        #RETA_fc_ancit.reverse()

        minl.append(min(RETA_fc_ancit))
        ETA_fc_ancn.append(ETA_fc_ancit)
        RETA_fc_ancn.append(RETA_fc_ancit)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(i)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1

    #print(ETA_fc_ancn)

    #**********************************************************************************************************************************************************************************
    #Graphen
    #**********************************************************************************************************************************************************************************
    #for m,f in zip(M0,RETA_fc_anc):


#print(minl)
ming = min(minl)
RETA_fc_mani = []

for k in RETA_fc_ancn:
    RETA_fc_maniit = []
    for s in k:
        s = s + ((ming*-1)*1.5)
        RETA_fc_maniit.append(s)
    RETA_fc_mani.append(RETA_fc_maniit)


for m,f in itertools.zip_longest(v0,RETA_fc_ancn):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height and different VCAS')
plt.show()


"""for m,f in itertools.zip_longest(v0,RETA_fc_mani):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height and different VCAS')
plt.show()

"""

"""plt.plot(RETA_fc_ancn[-1], h, label = str(v0[-1]))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height')
plt.show()
"""


data = {}
r=[]
rm=[]
ri=[]
maxr = []
for f,v in itertools.zip_longest(Ptn,PCn):
    
    run = []
    runm = []
    rin=[]
    for b,p in zip(f,v):
        if b/p >= 1:
            run.append(None)
            rin.append(None)
            continue
        elif b/p <= 0:
            run.append(None)
            rin.append(None)
            continue
        else:
            #run.append((((b/p))))
            run.append((((b/p))))
            rin.append((1+((b/p)*-1)))
            runm.append((1+((b/p)*-1)))
        #print(f"Turbine{b}   Compressor{p}")
    maxr.append(max(runm))
    r.append(run)
    ri.append(rin)
    rm.append(runm)
#print(r)
"""for m,t in zip(v0,r):
 plt.plot(t, h, label = str(m))"""

maxg = max(maxr)
rap = []
for i in ri:
    ir = []
    for x in i:
        if x != None:
            x=x+maxg
        ir.append(x)
    rap.append(ir)

for m,f in itertools.zip_longest(v0,r):
    
    plt.plot((f), h, label = str(m))


plt.xlabel("Power ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Power ratio over height and different VCAS Old')
plt.show()

#r.reverse()
"""h.reverse()
#r[-1].reverse()
for m,f in itertools.zip_longest(v0,rap):
    
    plt.plot((f), h, label = str(m))


plt.xlabel("Power ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Power ratio over height and different VCAS')
plt.show()
"""
#print(f"PT3 {PT3}   PT4 {PT4}")


"""print(f"Das ist TSO{TS0}")
print(f"Das ist PSO{PS0}")"""
"""print(f"Das ist PT4 {PT4}")
print(f"Das ist PT3 {PT3}")
print(f"Das ist PRc {PRc}")"""





"""#**********************************************************************************************************************************************************************************
#Graphen
#**********************************************************************************************************************************************************************************
#for m,f in zip(M0,RETA_fc_anc):

data = {}

for m,f in zip(M0,ETA_fc_anc):
    data[m]=f
    plt.plot(f, h, label = str(m))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height and different Mach numbers')
plt.show()



plt.plot(ETA_fc_anc[-1], h, label = str(M0[-1]))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height')
plt.show()



data = {}
r=[]
for f,v in zip(Pt,PC):
    run = []
    for b,p in zip(f,v):
        run.append(b/p)
    r.append(run)

for m,t in zip(M0,r):
 plt.plot(t, h, label = str(m))

plt.xlabel("Power ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Power ratio over height and different Mach numbers')
plt.show()"""
