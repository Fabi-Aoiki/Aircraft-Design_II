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
vmax=0.8*300
n=0
while n < 18000:#con.H_CRUISE:
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

PTDiff = PT3 -PT4 

#Values From Changing values
##PRc Clac Iteration over M and then hight

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
mdot = con.PEMFC_Lamda*((Pel_Stack/ (ETA_fc_stack * con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2))) #[kg/s]  under regular circum 26.218857206691773 


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
#print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


########################
#Pt


lg = listlength(TT3n)[0] 
ls = listlength(TT3n)[1] 
ns = (listlength(TT3n)[2])
ns = int(ns)-1

Ptn =[]
i=0

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

#corrections 
##############################################
#Mdot coreections

#Op points find

opind = h.index(12000) #op height
Mop = 0.785
n=0
ETAR = []
Mpoint = []
TT0pointit =[]
PT0pointit =[]

ETARl = []
Mpointl = []
v0l=[]
Mdis =[]
PRcl = []
TT0pointl =[]
PT0pointl =[]


for i in v0:
    Mpoint = M1[n]
    ETAR = ETA_fc_ancn[n]
    PRcrl = PRcn[n]
    TT0pointit = TT0n[n]
    PT0pointit = PT0n[n]
    print(f"Geschwindigkeit {i}, Wirkungsgrad {ETAR[opind]}, Mach {Mpoint[opind]} ")
    PRcl.append(PRcrl[opind])
    ETARl.append(ETAR[opind])
    Mpointl.append(Mpoint[opind])
    v0l.append(opind)
    Mdis.append(abs((Mpoint[opind])-Mop))
    TT0pointl.append(TT0pointit[opind])
    PT0pointl.append(PT0pointit[opind])
    n=n+1



Mnear = min(Mdis)

vspoint = Mdis.index(Mnear)

PRc_Choosen= PRcl[vspoint]
TT_Choosen = TT0pointl[vspoint]
PT_Choosen = PT0pointl[vspoint]
print(f"Compression choosen = {PRc_Choosen}, Temp choosen = {TT_Choosen}, Pressure choosen = {PT_Choosen}")



PRcrestricted = []
n=0
for i in PRcn:

    PRc_it =[]

    for x in i:
        if PRc_Choosen <= x:
            PRc_it.append(PRc_Choosen)
        else:
            PRc_it.append(x)
    PRcrestricted.append(PRc_it)
    n=n+1


mdotcor = mdot* (((TT_Choosen/con.PEMFC_TT_ref)**0.5)/(PT_Choosen/con.PEMFC_PT_ref))

mdot_aden = mdotcor* ((PT_Choosen/con.PEMFC_PT_ref)/((TT_Choosen/con.PEMFC_TT_ref)**0.5))

mdot_cn = []

for x,y in zip(PRcrestricted,PRcn):
    mdot_cn_it =[]
    for a,b in zip(x,y):
        m = mdot_aden*((a/b)**(1-(((0.4)/(2*con.PEMFC_ETA_c_pol*con.PEMFC_Kappa)))))
        mdot_cn_it.append(m)
    mdot_cn.append(mdot_cn_it)




PT3C = []
PTFCC = []
for a,b in zip(PRcrestricted, PT0n):
    PT3C_r = []
    PTFCC_r = []
    for x,y in zip(a,b):
        PT3c_n = x*y
        PTFCC_n = PT3c_n/(1+con.PEMFC_dPT_PT)
        #print(f"PT3 = {PT3c_n}, PRCr = {x}, PT0 = {y}, PTFCC = {PTFCC_n}")
        PT3C_r.append(PT3c_n)
        PTFCC_r.append(PTFCC_n)
    PT3C.append(PT3C_r)
    PTFCC.append(PTFCC_r)


PT4C = []
a = None
x = None
for a in PTFCC :
    PT4C_r = []
    for x in a:
        PT4c_n = x*(1-con.PEMFC_dPT_PT)
        PT4C_r.append(PT4c_n)
    PT4C.append(PT4C_r)



PRTCn = []
for o,u in zip(PT0n,PT4C):
    PRtintc = []
    for f,g in zip(o,u):
        PRtintc.append(g/f)#PT5 = PT0
        print(g/f)
    
    PRTCn.append(PRtintc)

#Pel Stack cn
Pel_cn = []
H_cn = []
FC_cn = [] 
ETA_stack_cn = []


for i in mdot_cn:
    Pel_cn_it = []
    Pel_ver_it = []
    FC_cn_it = []
    ETA_stack_cn_it = []
    for m in i:
        sub1 = (1/((1/ETA_fc_stack)*(m/mdot_aden)))
        sub2 = con.PEMFC_a*(Pel_Stack/P_stackMax)
        complete = ((con.PEMFC_b)/(sub1-sub2)) * Pel_Stack
        ncomplete = ((con.PEMFC_b)/(sub1-sub2))
        FC_com = (Pel_Stack/P_stackMax)*ncomplete
        ETA_com = con.PEMFC_a * FC_com + con.PEMFC_b
        Pel_cn_it.append(complete)
        Pel_ver_it.append(ncomplete)
        FC_cn_it.append(FC_com)
        ETA_stack_cn_it.append(ETA_com)
    Pel_cn.append(Pel_cn_it)
    H_cn.append(Pel_ver_it)
    FC_cn.append(FC_cn_it)
    ETA_stack_cn.append(ETA_stack_cn_it)

#############################################################################################################################
lg = listlength(TT0n)[0] 
ls = listlength(TT0n)[1] 
ns = (listlength(TT0n)[2])
ns = int(ns)-1

ETA_cn =[]
RETA_cn=[]# 1- ETA (Revese Eta)

i=0



while i <= ns:


    Prtrun_pre1=[]
    Prcrun_pre1=[]
    TT0run_pre1=[]
    ETA_stack_run_pre1=[]
    Prcrun_pre1.append(PRcrestricted[i])
    TT0run_pre1.append(TT0n[i])
    Prtrun_pre1.append(PRTCn[i])
    ETA_stack_run_pre1.append(ETA_stack_cn[i])
    
    




    for x1,y1,z1,u1 in itertools.zip_longest(TT0run_pre1,Prtrun_pre1,Prcrun_pre1,ETA_stack_run_pre1):
        n = 0
        ETA_cnit=[]
        RETA_cnit=[]
        
        


        while n <= ls-1:

        
            TT0run1 = x1[n]
            Prtrun1 = y1[n]
            Prcrun1 = z1[n]
            ETA_stack_run1 = u1[n]

            





            PRc_hoch = ((0.4)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))
            PRT_hoch = ((con.PEMFC_ETA_t_pol)*((0.4))/con.PEMFC_Kappa)


            Ltr = TT0run1*((((Prcrun1**(PRc_hoch)))/(Prtrun1**(PRT_hoch)))-1)



            ETA_cnrun = (1- (((1/con.PEMFC_ETA_c_m))*cp*con.PEMFC_Lamda*(1/(ETA_stack_run1*con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2)) * Ltr))

            RETA_cnrun = ((1-ETA_cnrun))


            ETA_cnit.append(ETA_cnrun)
            RETA_cnit.append(RETA_cnrun)
            n = n +1

        #RETA_fc_ancit.reverse()


        ETA_cn.append(ETA_cnit)
        RETA_cn.append(RETA_cnit)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(i)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i +1
################################################################################################################################
Pshaft = []

for a , b, c, d in zip(H_cn, ETA_cn, ETA_fc_ancn, FC_cn):
    Pshaft_it =[]

    for w, x, y, z in zip(a,b,c,d):
        Pel_mot_crs = ((Pel_Stack*0.93)- con.P_elNonProp)  #Sketchy shit weil Timon mist Programiert
        Konst = con.Transef_Se * con.PEMFC_ETA_emot * con.PEMFC_ETA_invert * Pel_mot_crs
        Nonkonst = w*(x/y)*(z/(Pel_Stack/P_stackMax))
        P = Konst *Nonkonst
        Pshaft_it.append(P)
    Pshaft.append(Pshaft_it)






















############################################################################################################################










    #**********************************************************************************************************************************************************************************
    #Graphen
    #**********************************************************************************************************************************************************************************
    #for m,f in zip(M0,RETA_fc_anc):





for m,f in itertools.zip_longest(v0,RETA_fc_ancn):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("1-ETA_fc_anc")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Efficiency over height and different VCAS')
plt.show()






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


rm=[]

for f,v in itertools.zip_longest(PRTCn,PRcrestricted):
    

    runm = []

    for b,p in zip(f,v):
        if b/p >= 1:

            runm.append(None)
            continue
        elif b/p <= 0:

            runm.append(None)
            continue
        else:
            #run.append((((b/p))))
            runm.append((((b/p))))





    rm.append(runm)




for m,f,g in itertools.zip_longest(v0,r,rm):
    
    plt.plot((f), h, label = str(m))
    plt.plot((g), h, label = (str(m)+"Restricted"))


plt.xlabel("Pressure ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Pressure ratio over height and different VCAS')
plt.grid(True)
plt.show()


    
plt.plot((r[-1]), h, label = str(v0[-1]))
plt.plot((rm[-1]), h, label = (str(v0[-1])+"Restricted"))


plt.xlabel("Pressure ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Pressure ratio over height')
plt.grid(True)
plt.show()

plt.plot((r[4]), h, label = str(v0[4]))
plt.plot((rm[4]), h, label = (str(v0[4])+"Restricted"))


plt.xlabel("Pressure ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Pressure ratio over height')
plt.grid(True)
plt.show()

#Pressure Ratio constricted and none constricted
for m,f,g in itertools.zip_longest(v0,PRcn,PRcrestricted):
    
    plt.plot((f), h, label = str(m))
    plt.plot((g), h, label = (str(m) + " Restricted"))


plt.xlabel("Compressor Pressure Ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Compressor Ratio over height and different VCAS')
plt.grid(True)
plt.show()



#Pressure Ratio constricted and none constricted 

    
plt.plot((PRcn[-1]), h, label = str(v0[-1]))
plt.plot((PRcrestricted[-1]), h, label = (str(v0[-1]) + " Restricted"))


plt.xlabel("Compressor Pressure Ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Compressor Ratio diffrence of restriction')
plt.grid(True)
plt.show()



#Pressure Ratio constricted and none constricted TURBINE
for m,f,g in itertools.zip_longest(v0,PRtn,PRTCn):
    
    plt.plot((f), h, label = str(m))
    plt.plot((g), h, label = (str(m) + " Restricted"))


plt.xlabel("Turbine Pressure Ratio")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Turbine Ratio over height and different VCAS')
plt.grid(True)
plt.show()


rverg=[]

for f in mdot_cn:
    
    run = []

    for b in f:

        run.append((((b/mdot_aden))))



    rverg.append(run)





for m,f in itertools.zip_longest(v0,rverg):
    
    plt.plot((f), h, label = str(m))


plt.xlabel("mdot")
plt.ylabel("Height [m]")
plt.legend()
plt.title('mdot_cn / mdot over height and different VCAS')
plt.grid(True)
plt.show()




for m,f in itertools.zip_longest(v0,H_cn):
    
    plt.plot((f), h, label = str(m))


plt.xlabel("mdot")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Pel diff over height and different VCAS')
plt.grid(True)
plt.show()



for m,f in itertools.zip_longest(v0,RETA_cn):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("1-ETA_fc_anc_constricted")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Constricted efficiency over height and different VCAS')
plt.grid(True)
plt.show()





    
plt.plot(RETA_cn[-1], h, label = str(v0[-1]))

plt.xlabel("1-ETA_fc_anc_constricted")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Constricted efficiency')
plt.grid(True)
plt.show()



for m,f in itertools.zip_longest(v0,Pshaft):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("Shaft Power  [W]")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Shaft power to height')
plt.grid(True)
plt.show()

for m,f in itertools.zip_longest(v0,FC_cn):
    
    plt.plot(f, h, label = str(m))

plt.xlabel("FC Load")
plt.ylabel("Height [m]")
plt.legend()
plt.title('Fuel Cell Load')
plt.grid(True)
plt.show()

#print(PTDiff)
#print(PRcrestricted)
#print(f"PT3C {PT3C}  _______   PT4C{PT4C}")
print(PRTCn)