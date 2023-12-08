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

def standaarddag(ekost, radiantie):
    def zonnepaneelE(radiantie):
        return radiantie * 0.2 * 22.4
    #prijs in kwh ipv Mwh
    e_kost = [i/1000 for i in ekost]
    #hoeveel hebben we al gespendeerd
    kost = 0
    #warmtepomp van 0 uur tot 9 uur
    for i in range(0,9):
        delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            kost += delta_e*e_kost[i]
    #warmtepomp van 9 uur tot 17 uur
    for i in range(9,17):
        delta_e = warmtepomp_verbruik_laag-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            kost += delta_e*e_kost[i]
    #warmtepomp om 17 uur
    Delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[17])
    if Delta_e < 0:
        kost += 1/3*Delta_e*e_kost[17]
    elif Delta_e > 0:
        kost += Delta_e*e_kost[17]
    #tijdsinterval van 18 tot 20 uur
    #tijdsinterval waar veel apparaten samen aanstaan, in volgorde : warmtepomp, keuken, auto
    for i in range(18,20):
        delta_e = warmtepomp_verbruik_hoog+ verbruik_keuken+auto_verbruik-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            kost += delta_e*e_kost[i]
    #20 uur, apparaten: warmtepomp, auto, wasmachine
    delta_e_20 = warmtepomp_verbruik_hoog+auto_verbruik+2.5-zonnepaneelE(radiantie[20])
    if delta_e_20 < 0:
        kost += 1/3*delta_e_20*e_kost[20]
    elif delta_e_20 > 0:
        kost += delta_e_20*e_kost[20]
    #21 uur, apparaten: warmtepomp, wasmachine
    delta_e_21 = warmtepomp_verbruik_hoog+2.5-zonnepaneelE(radiantie[21])
    if delta_e_21 < 0:
        kost += 1/3*delta_e_21*e_kost[21]
    elif delta_e_21 > 0:
        kost += delta_e_21*e_kost[21]
    #22 -23 uur, apparaten: warmtepomp
    for i in range(22,24):
        delta_e = warmtepomp_verbruik_hoog-zonnepaneelE(radiantie[i])
        if delta_e < 0:
            kost += 1/3*delta_e*e_kost[i]
        elif delta_e > 0:
            kost += delta_e*e_kost[i]
    return kost


def dag_berekenen(dag):
    #neem een deel van de temperatuurlijst en de irradiantielijst
    e_prijzen = []
    for i in range(dag*24,(dag+1)*24):
        e_prijzen.append(float(vervang_komma_door_punt(removeSpaces(e_kost[i][1]))))
    print(e_prijzen)
    radiantie = []
    for i in range(dag*24,(dag+1)*24):
        radiantie.append(float(vervang_komma_door_punt(removeSpaces(temp_en_ir[i][2]))))
    kost = standaarddag(e_prijzen, radiantie)
    return kost

def custom_dag(e_kost, irradiante, temperatuur):
    kost  = standaarddag(e_kost, irradiante)
    return kost

def periode_berekenen(startdag, einddag):
    kost_tot = 0
    kost_lijst = []
    for i in range(startdag, einddag+1):
        kost = dag_berekenen(i)
        kost_lijst.append(kost)
        kost_tot += kost
    return kost_tot, kost_lijst

a = periode_berekenen(0, 1)
print(a[0])




