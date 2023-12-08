import random
from TestPno.TEST_controller.GetfromDB import getFromDB
from TestPno.TEST_controller.GetfromDB import getTempFromDB
from TestPno.TEST_controller.GetfromDB import getFullCost
from TestPno.TEST_controller.GetfromDB import getFullTempAndIr
from TestPno.TEST_controller.GetfromDB import removeSpaces
from TestPno.TEST_controller.GetfromDB import vervang_komma_door_punt
from TestPno.TEST_controller.Simuleer_warmte_model import simuleer_warmte_model

delta_T = 1
def scuffed_warmte(T_in0, T_m0, S_rad, T_out):
    if T_in0 <= 19:
        for i in range(0,14):
            temp_lijst = simuleer_warmte_model(delta_T, i*300, 0, T_out,S_rad,T_in0,T_m0)
            if temp_lijst[0][-1] >=19 and temp_lijst[0][-1] <= 22:
                return i*0.3 , temp_lijst[0][-1], temp_lijst[1][-1]
        return 4 , temp_lijst[0][-1], temp_lijst[1][-1]
    elif T_in0 > 19 and T_in0 <= 23:
        temp_lijst = simuleer_warmte_model(delta_T, 0, 0, T_out,S_rad,T_in0,T_m0)
        return 0 , temp_lijst[0][-1], temp_lijst[1][-1]
    else:
        for i in range(0,14):
            temp_lijst = simuleer_warmte_model(delta_T, 0, i*300, T_out,S_rad,T_in0,T_m0)
            if temp_lijst[0][-1] >=19 and temp_lijst[0][-1] <= 22:
                return i*0.3 , temp_lijst[0][-1], temp_lijst[1][-1]
        return 4 , temp_lijst[0][-1], temp_lijst[1][-1]





e_kost = list(reversed(getFullCost()))
temp_en_ir = list(reversed(getFullTempAndIr()))
e_prijzen = []




auto_verbruik = 7.4
warmtepomp_verbruik_hoog = 1.5
warmtepomp_verbruik_laag = 0
verbruik_keuken = 3.3905

def standaarddag(ekost, radiantie, temp_out, thuis, bolwp, bolwas, bolauto, bolkeuken):
    def zonnepaneelE(radiantie):
        if (radiantie * 0.2 * 46.2) / 1000 > 6.3:
            return 6.3
        else:
            return (radiantie * 0.2 * 46.2) / 1000

    #prijs in kwh ipv Mwh
    e_kost = [i/1000 for i in ekost]
    #hoeveel hebben we al gespendeerd
    kost = 0
    groene_energie = 0
    net_energie = 0
    T_0 = 20
    T_m0 = 20

    if bolwp == True: boolwp = 1
    else: boolwp = 0
    if bolwas == True: boolwas = 1
    else: boolwas = 0
    if bolauto == True: boolauto = 1
    else: boolauto = 0
    if bolkeuken == True: boolkeuken = 1
    else: boolkeuken = 0
    #warmtepomp van 0 uur tot 9 uur
    for i in range(0,9):
        result = scuffed_warmte(T_0,T_m0,radiantie[i],temp_out[i])
        T_0 = result[1]
        T_m0 = result[2]
        delta_e = result[0]*boolwp-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
            groene_energie += result[0]*boolwp
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #warmtepomp van 9 uur tot 17 uur
    for i in range(9,17):
        if thuis == True:
            variabele = 1
        else: variabele = 0
        result = scuffed_warmte(T_0, T_m0, radiantie[i], temp_out[i])
        T_0 = result[1]
        T_m0 = result[2]
        delta_e = result[0]*variabele*boolwp-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
            groene_energie += result[0]*variabele*boolwp
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #warmtepomp om 17 uur
    result = scuffed_warmte(T_0, T_m0, radiantie[17], temp_out[17])
    T_0 = result[1]
    T_m0 = result[2]
    Delta_e = result[0]*boolwp-zonnepaneelE(radiantie[17])
    if Delta_e < 0:
        groene_energie += result[0]*boolwp
        kost += 1/3*Delta_e*e_kost[17]
    elif Delta_e > 0:
        groene_energie += zonnepaneelE(radiantie[17])
        net_energie += Delta_e
        kost += Delta_e*e_kost[17]
    #tijdsinterval van 18 tot 20 uur
    #tijdsinterval waar veel apparaten samen aanstaan, in volgorde : warmtepomp, keuken, auto
    for i in range(18,20):
        result = scuffed_warmte(T_0, T_m0, radiantie[i], temp_out[i])
        T_0 = result[1]
        T_m0 = result[2]
        delta_e = result[0]*boolwp + verbruik_keuken*boolkeuken+auto_verbruik*boolauto-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            groene_energie += result[0]*boolwp + verbruik_keuken+auto_verbruik
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #20 uur, apparaten: warmtepomp, auto, wasmachine
    result = scuffed_warmte(T_0, T_m0, radiantie[20], temp_out[20])
    T_0 = result[1]
    T_m0 = result[2]
    delta_e_20 = result[0]*boolwp+auto_verbruik*boolauto+2.5*boolwas-zonnepaneelE(radiantie[20])
    if delta_e_20 < 0:
        groene_energie += result[0]*boolwp + auto_verbruik + 2.5
        kost += 1/3*delta_e_20*e_kost[20]
    elif delta_e_20 > 0:
        groene_energie += zonnepaneelE(radiantie[20])
        net_energie += delta_e_20
        kost += delta_e_20*e_kost[20]
    #21 uur, apparaten: warmtepomp, wasmachine
    result = scuffed_warmte(T_0, T_m0, radiantie[21], temp_out[21])
    T_0 = result[1]
    T_m0 = result[2]
    delta_e_21 = result[0]*boolwp+2.5*boolwas-zonnepaneelE(radiantie[21])
    if delta_e_21 < 0:
        groene_energie += result[0]*boolwp + 2.5
        kost += 1/3*delta_e_21*e_kost[21]
    elif delta_e_21 > 0:
        groene_energie += zonnepaneelE(radiantie[21])
        net_energie += delta_e_21
        kost += delta_e_21*e_kost[21]
    #22 -23 uur, apparaten: warmtepomp
    for i in range(22,24):
        result = scuffed_warmte(T_0, T_m0, radiantie[i], temp_out[i])
        T_0 = result[1]
        T_m0 = result[2]
        delta_e = result[0]*boolwp-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            groene_energie += result[0]*boolwp
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    return kost, groene_energie, net_energie


def dag_berekenen(dag, thuis):
    #neem een deel van de temperatuurlijst en de irradiantielijst
    boolwp = True
    boolwas = True
    boolauto = True
    boolkeuken = True
    e_prijzen = []
    for i in range(dag*24,(dag+1)*24):
        e_prijzen.append(float(vervang_komma_door_punt(removeSpaces(e_kost[i][1]))))

    radiantie = []
    for i in range(dag*24,(dag+1)*24):
        radiantie.append(float(vervang_komma_door_punt(removeSpaces(temp_en_ir[i][2]))))

    T_out = []
    for i in range(dag*24, (dag+1)*24):
        T_out.append(float(removeSpaces(temp_en_ir[i][1])))

    [kost, groene_energie, net_energie] = standaarddag(e_prijzen, radiantie, T_out ,thuis, boolwp, boolwas, boolauto, boolkeuken)
    return kost, groene_energie, net_energie

def custom_dag(e_kost, irradiante, thuis, boolwp, boolwas, boolauto, boolkeuken, temperatuur):
    kost = standaarddag(e_kost, irradiante, temperatuur, thuis, boolwp, boolwas, boolauto, boolkeuken)[0]
    return kost

def periode_berekenen(startdag, einddag):
    kost_tot = 0
    groene_energie_tot = 0
    net_energie_tot = 0
    kost_lijst = []
    for i in range(startdag, einddag+1):
        if startdag//7 <= 1:
            thuis = True
        else: thuis = False

        [kost, groene_energie, net_energie] = dag_berekenen(i, thuis)
        kost_lijst.append(kost)
        kost_tot += kost
        groene_energie_tot += groene_energie
        net_energie_tot += net_energie
    return kost_tot, kost_lijst, groene_energie_tot, net_energie_tot

a = periode_berekenen(0, 363)





