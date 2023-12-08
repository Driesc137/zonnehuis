import random
from TestPno.TEST_controller.GetfromDB import getFromDB
from TestPno.TEST_controller.GetfromDB import getTempFromDB
from TestPno.TEST_controller.GetfromDB import getFullCost
from TestPno.TEST_controller.GetfromDB import getFullTempAndIr
from TestPno.TEST_controller.GetfromDB import removeSpaces
from TestPno.TEST_controller.GetfromDB import vervang_komma_door_punt


e_kost = list(reversed(getFullCost()))
temp_en_ir = list(reversed(getFullTempAndIr()))
e_prijzen = []




auto_verbruik = 7.4
warmtepomp_verbruik_hoog = 2.5
warmtepomp_verbruik_laag = 1.5
verbruik_keuken = 3.3905

def standaarddag(ekost, radiantie, thuis):
    def zonnepaneelE(radiantie):
        if (radiantie * 0.2 * 46.2)/1000>6.3:
            return 6.3
        else:
            return (radiantie * 0.2 * 46.2)/1000
    #prijs in kwh ipv Mwh
    e_kost = [i/1000 for i in ekost]
    #hoeveel hebben we al gespendeerd
    kost = 0
    groene_energie = 0
    net_energie = 0
    #warmtepomp van 0 uur tot 9 uur
    for i in range(0,9):
        delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
            groene_energie += warmtepomp_verbruik_hoog
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #warmtepomp van 9 uur tot 17 uur
    for i in range(9,17):
        if thuis == True:
            variabele = 1
        else: variabele = 0
        delta_e = warmtepomp_verbruik_laag*variabele-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
            groene_energie += warmtepomp_verbruik_laag*variabele
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #warmtepomp om 17 uur
    Delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[17])
    if Delta_e < 0:
        groene_energie += warmtepomp_verbruik_hoog
        kost += 1/3*Delta_e*e_kost[17]
    elif Delta_e > 0:
        groene_energie += zonnepaneelE(radiantie[17])
        net_energie += Delta_e
        kost += Delta_e*e_kost[17]
    #tijdsinterval van 18 tot 20 uur
    #tijdsinterval waar veel apparaten samen aanstaan, in volgorde : warmtepomp, keuken, auto
    for i in range(18,20):
        delta_e = warmtepomp_verbruik_hoog+ verbruik_keuken+auto_verbruik-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            groene_energie += warmtepomp_verbruik_hoog+ verbruik_keuken+auto_verbruik
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    #20 uur, apparaten: warmtepomp, auto, wasmachine
    delta_e_20 = warmtepomp_verbruik_hoog+auto_verbruik+2.5-zonnepaneelE(radiantie[20])
    if delta_e_20 < 0:
        groene_energie += warmtepomp_verbruik_hoog+auto_verbruik+2.5
        kost += 1/3*delta_e_20*e_kost[20]
    elif delta_e_20 > 0:
        groene_energie += zonnepaneelE(radiantie[20])
        net_energie += delta_e_20
        kost += delta_e_20*e_kost[20]
    #21 uur, apparaten: warmtepomp, wasmachine
    delta_e_21 = warmtepomp_verbruik_hoog+2.5-zonnepaneelE(radiantie[21])
    if delta_e_21 < 0:
        groene_energie += warmtepomp_verbruik_hoog+2.5
        kost += 1/3*delta_e_21*e_kost[21]
    elif delta_e_21 > 0:
        groene_energie += zonnepaneelE(radiantie[21])
        net_energie += delta_e_21
        kost += delta_e_21*e_kost[21]
    #22 -23 uur, apparaten: warmtepomp
    for i in range(22,24):
        delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            groene_energie += warmtepomp_verbruik_hoog
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            groene_energie += zonnepaneelE(radiantie[i])
            net_energie += delta_e
            kost += delta_e*e_kost[i]
    return kost, groene_energie, net_energie


def dag_berekenen(dag, thuis):
    #neem een deel van de temperatuurlijst en de irradiantielijst
    e_prijzen = []
    for i in range(dag*24,(dag+1)*24):
        e_prijzen.append(float(vervang_komma_door_punt(removeSpaces(e_kost[i][1]))))
    radiantie = []
    for i in range(dag*24,(dag+1)*24):
        radiantie.append(float(vervang_komma_door_punt(removeSpaces(temp_en_ir[i][2]))))
    kost = standaarddag(e_prijzen, radiantie, thuis)[0]
    groene_energie = standaarddag(e_prijzen, radiantie, thuis)[1]
    net_energie = standaarddag(e_prijzen, radiantie, thuis)[2]
    return kost, groene_energie, net_energie

def custom_dag(e_kost, irradiante, thuis, temperatuur):
    kost  = standaarddag(e_kost, irradiante, thuis)[0]
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

        kost = dag_berekenen(i, thuis)[0]
        groene_energie = dag_berekenen(i, thuis)[1]
        net_energie = dag_berekenen(i, thuis)[2]
        kost_lijst.append(kost)
        kost_tot += kost
        groene_energie_tot += groene_energie
        net_energie_tot += net_energie
    return kost_tot, kost_lijst, groene_energie_tot, net_energie_tot

a = periode_berekenen(0, 7)
print(a[0])
print(a[1])




