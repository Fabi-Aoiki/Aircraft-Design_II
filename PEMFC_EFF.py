from PEMFC import listlength, TT0n, PRcn, PRtn, cp, h, ETA_fc_stack,v0
import constants as con
import matplotlib.pyplot as plt

print(ETA_fc_stack)

def Efiicienc(TT0n, PRcn, PRtn, cp,ETA_fc_stack, h, v0):
    lg = listlength(TT0n)[0] 
    ls = listlength(TT0n)[1] 
    ns = (listlength(TT0n)[2])
    ns = int(ns)-1

    ETA_fc_ancn =[]
    RETA_fc_ancn=[]# 1- ETA (Revese Eta)
    i=0

    while i <= ns:


        Prtrun_pre1=[]
        Prcrun_pre1=[]
        TT0run_pre1=[]
        Prcrun_pre1.append(PRcn[i])
        TT0run_pre1.append(TT0n[i])
        Prtrun_pre1.append(PRtn[i])


    

        for x1,y1,z1 in zip(TT0run_pre1,Prtrun_pre1,Prcrun_pre1):
            n = 0
            ETA_fc_ancit=[]
            RETA_fc_ancit=[]

            while n <= ls-1:

                
                TT0run1 = x1[n]
                Prtrun1 = y1[n]
                Prcrun1 = z1[n]
                PRc_hoch = ((con.PEMFC_Kappa-1)/(con.PEMFC_ETA_c_pol*con.PEMFC_Kappa))
                PRT_hoch = ((con.PEMFC_ETA_t_pol)*((con.PEMFC_Kappa-1))/con.PEMFC_Kappa)
                Ltr = TT0run1*((((Prcrun1**(PRc_hoch)))/(Prtrun1**(PRT_hoch)))-1)
                Ltrr = TT0run1*(1-(((Prcrun1**(PRc_hoch)))/(Prtrun1**(PRT_hoch))))
                ETA_fc_ancrun = 1 - (1/con.PEMFC_ETA_c_m)*cp*con.PEMFC_Lamda*(1/(ETA_fc_stack*con.PEMFC_LHV))*(con.PEMFC_M_air/(2*con.PEMFC_M_H2*con.PEMFC_y_air_o2)) * Ltr
                RETA_fc_ancrun = 1-ETA_fc_ancrun
                print(f"Das ist der Wirkungsgrad  {ETA_fc_ancrun} , Das ist der Gegen Wirkungsgrad {RETA_fc_ancrun} , Das ist der letzte Term {Ltr}")
                print(f"Das ist PRC  {Prcrun1} , Das ist PRT {Prtrun1} , Das ist der letzte Term reverse  {Ltrr}")

                ETA_fc_ancit.append(ETA_fc_ancrun)
                RETA_fc_ancit.append(RETA_fc_ancrun)
                n = n +1



            ETA_fc_ancn.append(ETA_fc_ancit)
            RETA_fc_ancn.append(RETA_fc_ancit)

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(i)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        i = i +1



    #**********************************************************************************************************************************************************************************
    #Graphen
    #**********************************************************************************************************************************************************************************
    #for m,f in zip(M0,RETA_fc_anc):

    data = {}

    for m,f in zip(v0,RETA_fc_ancn):
        data[m]=f
        plt.plot(f, h, label = str(m))

    plt.xlabel("1-ETA_fc_anc")
    plt.ylabel("Height [m]")
    plt.legend()
    plt.title('Efficiency over height and different VCAS')
    plt.show()



    plt.plot(RETA_fc_ancn[-1], h, label = str(v0[-1]))

    plt.xlabel("1-ETA_fc_anc")
    plt.ylabel("Height [m]")
    plt.legend()
    plt.title('Efficiency over height')
    plt.show()




Efiicienc(TT0n,PRcn,PRtn,cp,ETA_fc_stack, h,v0)