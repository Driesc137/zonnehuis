#file in progress voor controller demodag
#to-do:
#verliezen zonne energie nog 0,75% verlies op tot zonne energie binnen
#zonne installatie:
    #zonne energie binnen = irradiatie * oppervlakte * efficientie * 75% door helling enzo
    #dit kan max 4750 W zijn
    #hier gaat nog es 10% af dus max 4750 W * 90% = 4275 W
#batterij erin gooien
#constraint : temp max 1 graad veranderen per uur (enkel als thuis) maak vergelijking voor verslag: tijdens oz
#simulatie laten beginnen om 6h
#imports

from Simuleer_warmte_model import simuleer_warmte_model
from GetfromDB import getFromDB
from GetfromDB import getTempFromDB
from Optimalisatie import optimaliseer
import numpy as np

def controller(tempinput,priceinput,radiationinput,wm_boolean,auto_boolean, keuken_boolean, thuis):
    #constanten
    delta_t = 1                     # tijdsinterval (h)
    horizon = 24                    # lengte van de horizon (h)
    zp_opp = 46.2                   # oppervlakte zonnepaneel (m^2)
    eff = 0.2                       # efficientie zonnepaneel
    M = 1000                        # grote M. Wat is dit?
    ewm = 2.5                       # verbruik wasmachine (kW = kWh/h)
    eau = 7.4                       # vermogen laadpaal (kW)
    ekeuken = 2.5                   # vermogen keuken (kW)
    start_time = 0                  # Begin met tijd = 0
    total_time = 24                 # Totaal aantal uren die geoptimaliseerd moeten worden
    if thuis:
        aankomst = 0
        vertrek = 0
    else:
        aankomst = 17-6                 # Aankomsttijd (uur van 6h => 17h)
        vertrek = horizon                    # Vertrektijd (uur van 12h => 6h)

    keuken_begin = 17-6                    # beginttijd (uur van 6h => 17h)
    keuken_einde = 19-6                    # eindtijd (uur van 6h => 19h)
    wm_aan = 0                     # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    auto_aan = 0                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    keuken_aan = 0                  # Aantal uren dat de keuken nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if wm_boolean:
        wm_aan = 2                      # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if auto_boolean:
        auto_aan = 3                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if keuken_boolean:
        keuken_aan = 2                  # Aantal uren dat de keuken nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)

    T_in_0 = 20                     # begintemperatuur van de binnenlucht (Celsius) voor benadering en simulatie (arbitrair)
    T_m_0 = 20                      # begintemperatuur van de bouwmassa (Celsius) voor benadering en simulatie (arbitrair)
    P_max = 4000                    # maximaal vermogen van de warmtepomp (W)
    P_max_airco = 4000              # maximaal vermogen van de airco (W)
    T_in_min = 20                   # minimale binnentemperatuur (Celsius)
    T_in_max = 22                   # maximale binnentemperatuur (Celsius)
    T_m_min = -10                    # minimale temperatuur van de bouwmassa (Celsius)
    T_m_max = 50                   # maximale temperatuur van de bouwmassa (Celsius)

    batmax = 10000                     #maximale batterijcapaciteit (kWh)
    batmin = 0                      #minimale batterijcapaciteit (kWh)
    bat0 = 0                        #begintoestand batterij (kWh)
    batmaxcharge = batmax                #maximale laadsnelheid batterij (kW)
    batmaxdischarge = batmax             #maximale ontlaadsnelheid batterij (kW)


    #haal data uit database
    temp_out = tempinput
    irradiantie = radiationinput
    netstroom = priceinput

    #bereken zonne energie

    zonne_energie = [i * zp_opp * eff * 0.75 for i in irradiantie]  # lijst met beschikbare zonne-energie (W) per uur
    for i in zonne_energie:
        if i > 7000:
            zonne_energie[zonne_energie.index(i)] = 7000  # maximum vermogen van zonnepanelen is 4750 W
    zonne_energie = [i *0.9 for i in zonne_energie]

    #horizon implementatie
    current_time = start_time                                                       #houdt de huidige tijd bij
    opslag_resultaat = {}                                                           #maak een dictionary om de resultaten van de optimalisatie in op te slaan
    opslag_simulatie = {}                                                          #maak een dictionary om de resultaten van de simulatie in op te slaan
    actions = {}                                                                    #maak een dictionary om de definitieve acties van de controller in op te slaan
    attributes = ['auto', 'wm','keuken', 'ebuy', 'esell', 'wpsum', 'aircosum', 'batstate', 'batcharge', 'batdischarge']      #maak een lijst met de attributen van de dictionary
    for i in attributes:
        actions[i] = []                                                             #initialiseer een lijst voor elk attribuut in de dictionary
    actions['Binnentemperatuur'] = []                                               #initialiseer een lijst voor de binnentemperatuur
    wp_actions = []                                                                 #maak een lijst voor de acties van de warmtepomp
    airco_actions = []                                                              #maak een lijst voor de acties van de airco
    T_in_simulatie = []                                                             #maak een lijst voor de binnentemperatuur van de simulatie
    T_m_simulatie = []                                                              #maak een lijst voor de temperatuur van de bouwmassa van de simulatie
    T_time_simulatie = []                                                           #maak een lijst voor de tijd van de simulatie
    while current_time < total_time:                                                #zolang de huidige tijd kleiner is dan de totale tijd is de optimalisatie niet voltooid
        actions['Binnentemperatuur'].append(T_in_0)                                 #sla de binnentemperatuur op
        # bepaal de horizon lengte, optimaliseer en sla de resultaten op
        if current_time + horizon <= total_time:
            horizon_end = current_time + horizon                                    #einde van de huidige horizon
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zp_opp, eff, zonne_energie[current_time:horizon_end], eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end],  zp_opp, eff, zonne_energie[current_time:horizon_end], ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0] #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0] #aantal uren dat de auto nog aan moet staan
        keuken_aan = keuken_aan - opslag_resultaat['Iteratie', current_time]['keuken'][0] #aantal uren dat de keuken nog aan moet staan

        # sla de resultaten van de optimalisatie voor de current time op. Deze worden de definitieve acties
        for i in attributes:
            actions[i].append(opslag_resultaat['Iteratie', current_time][i][0])
        wp_actions.append(opslag_resultaat['Iteratie', current_time]['wp'][0:2])
        airco_actions.append(opslag_resultaat['Iteratie', current_time]['airco'][0:2])

        #batterij update
        bat0 = actions['batstate'][current_time] + actions['batcharge'][current_time] - actions['batdischarge'][current_time] #update de batterijtoestand voor de volgende iteratie


        #simuleer het warmte model van de huidige iteratie naar de volgende iteratie (tijdsvenster schuift op)
        [T_in, T_m, T_in_time, T_m_time, oplossing] = simuleer_warmte_model(delta_t, wp_actions[-2],airco_actions[-2],temp_out[current_time], irradiantie[current_time],T_in_0,T_m_0) #simulatie van het warmtemodel
        T_in_0 = T_in[-1]                                                      #begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]                                                        #begintemperatuur van de bouwmassa voor volgende iteratie
        opslag_simulatie['Iteratie', current_time] = [T_in, T_m, T_in_time, T_m_time, oplossing]
        [T_in, T_m, T_in_time, T_m_time, oplossing] = simuleer_warmte_model(delta_t, wp_actions[-2],airco_actions[-2],temp_out[current_time],irradiantie[current_time], T_in_0,T_m_0)  # simulatie van het warmtemodel
        T_in_0 = T_in[-1]  # begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]
        opslag_simulatie['Iteratie', current_time] = [T_in, T_m, T_in_time, T_m_time, oplossing]
        T_in_time = []
        T_m_time = []
        for i in range(0, 24):
            T_in = T_in + K['Iteratie', i][4].y[0, :].tolist()
            T_m = T_m + K['Iteratie', i][4].y[1, :].tolist()
            T_in_time = T_in_time + [elem + i * 3600 for elem in K['Iteratie', i][4].t.tolist()]
            T_m_time = T_m_time + [elem + i * 3600 for elem in K['Iteratie', i][4].t.tolist()]
        T_in = [i - 273.15 for i in T_in]
        T_m = [i - 273.15 for i in T_m]
        T_in_time = [i / (60 * 60) for i in T_in_time]
        T_m_time = [i / (60 * 60) for i in T_m_time]


        #verschuif horizon
        if aankomst == 0:
            aankomst = 0
        else:
            aankomst -= 1                                                           #verschuif de aankomst met 1 uur
        if vertrek == 0:
            vertrek = 0
        else:
            vertrek -= 1                                                            #verschuif het vertrek met 1 uur
        if keuken_begin == 0:
            keuken_begin = 0
        else:
            keuken_begin -= 1                                                       #verschuif het begin van de keuken met 1 uur
        if keuken_einde == 0:
            keuken_einde = 0
        else:
            keuken_einde -= 1                                                       #verschuif het einde van de keuken met 1 uur
        current_time += 1                                                           #verschuif de horizon met 1 uur

    #update batterij en temp laatste keer
    actions['batstate'].append(bat0)

    #print(opslag_resultaat)
    print("----------------------------------")

    for key, value in actions.items():
        locals()[key] = value
        if key == 'auto':
            auto_final = value
        elif key == 'wm':
            wm_final = value
        elif key == 'keuken':
            keuken_final = value
        elif key == 'ebuy':
            ebuy_final = value
        elif key == 'esell':
            esell_final = value
        elif key == 'wpsum':
            wpsum_final = value
        elif key == 'aircosum':
            aircosum_final = value
        elif key == 'Binnentemperatuur':
            T_in_final = value
        elif key == 'batstate':
            batstate_final = value
        elif key == 'batcharge':
            batcharge_final = value
        elif key == 'batdischarge':
            batdischarge_final = value
        print(f"{key}: {value}")

    print("----------------------------------")
    #haal van (bkoop, bverkoop) de eerste waarde uit de opslag_resultaat dictionary voor elke iteratie
    bkoop = [opslag_resultaat['Iteratie', i]['bkoop'][0] for i in range(0, total_time)]
    bverkoop = [opslag_resultaat['Iteratie', i]['bverkoop'][0] for i in range(0, total_time)]
    #haal van (wp_aan, airco_aan) de eerste twee waarden uit de opslag_resultaat dictionary voor elke iteratie
    wp_aan = [opslag_resultaat['Iteratie', i]['wp_aan'][0] for i in range(0, total_time)]
    airco_aan = [opslag_resultaat['Iteratie', i]['airco_aan'][0] for i in range(0, total_time)]
    #plak hier de tweede waarde van elke iteratie achteraan (voor wp_aan en airco_aan)
    wp_aan = wp_aan + [opslag_resultaat['Iteratie', i]['wp_aan'][1] for i in range(0, total_time)]
    airco_aan = airco_aan + [opslag_resultaat['Iteratie', i]['airco_aan'][1] for i in range(0, total_time)]

    print(f"bkoop123: {bkoop}")
    print(f"bverkoop: {bverkoop}")
    print(f"wp_aan123: {wp_aan}")
    print(f"airco_aan: {airco_aan}")
    print("----------------------------------")
    print(f"zonne_energie: {zonne_energie}")
    zonne_energie_sum = sum(zonne_energie)
    print(f"zonne_energie_sum: {zonne_energie_sum}")
    print("----------------------------------")

    #bereken de kostrpijs_energie met de data opgeslagen in actions
    kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i]/1000 - (1/3)* actions['esell'][i] * netstroom[i]/1000 for i in range(0, total_time))
    #print("De oplossing is €", kostprijs_energie)
    print(f"kostprijs_energie: {kostprijs_energie}")
    print("----------------------------------")
    print(opslag_resultaat['Iteratie', 0]['result'])
    print("----------------------------------")


    return [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final, zonne_energie, zonne_energie_sum, opslag_simulatie, opslag_resultaat, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final]  #    return [auto_final, wm_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final]
    #print(f"Geheugengrootte van de dictionary: {geheugengrootte_dict} bytes")

testdag = '2022-05-05'
dataset1 = getTempFromDB(testdag)                                       #haal temperatuur en irradiantie van dag 1 uit database
temp_out = dataset1[0]
#temp_out = [30,25,28,29,30,26,25,29,29,30,30,30,30,30,30,30,30,30,31,31,31,31,28,29,31,31,31,31]#haal temperatuur uit dataset1 (°C)
#temp_out = [30, 30, 30,30,30,30, 30, 30,30,30,30, 30, 30,30,30,30, 30, 30,30,30,30, 30, 30,30,30,30, 30, 30,30,30,30, 30, 30,30,30]

irradiantie = dataset1[1]
#irradiantie = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]

netstroom = getFromDB(testdag)
#netstroom = [-0.5, 189.91, 210.98, 188.41, -2, -1, 294.68, 316.63, 376.31, 370.89, 275.13, 267.75, 237.66, 189.53, 213.51, 185.24, 225.1, 333.5, -2, 469.17, -5, -5, 318.42, 284.3]
#netstroom = [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]
#haal netstroom van dag 1 uit database
booleanwm = True
booleanauto = True
booleankeuken = True
thuis = True
#print inputs
print("-----------------------------------")
print(f"wm input: {booleanwm}")
print(f"auto input: {booleanauto}")
print(f"keuken input: {booleankeuken}")
print(f"thuis input: {thuis}")
print(f"dag input: {testdag}")
print("-----------------------------------")

[A,B,C,D,E,F,G,H, I, J, K, L, M, N, O, P] = controller(temp_out, netstroom, irradiantie, booleanwm, booleanauto, booleankeuken, thuis)

print(f"netstroom: {netstroom}")
print(f"min netstroom: {min(netstroom)}")
print(f"max netstroom: {max(netstroom)}")
print(f"gem netstroom: {sum(netstroom)/len(netstroom)}")
print("----------------------------------")
#print de temp_out en irradiantie
print(f"temp_out: {temp_out}")
print(f"max temp_out: {max(temp_out)}")
print(f"min temp_out: {min(temp_out)}")
print(f"gem temp_out: {sum(temp_out)/len(temp_out)}")
print(f"irradiantie: {irradiantie}")
print("----------------------------------")

#bereken min, max en gemiddelde binnentemperatuur van de dag
min_T_in = min(H)
max_T_in = max(H)
gem_T_in = sum(H)/len(H)
print(f"min_T_in: {min_T_in}")
print(f"max_T_in: {max_T_in}")
print(f"gem_T_in: {gem_T_in}")

'''#print alle T_in uit opslag_simulatie
print("----------------------------------")
for i in range(0,24):
    print(f"T_in_{i}: {L['Iteratie', i]['T_in']}")
for i in range(0,24):
    print(f"vermogen_{i}: {L['Iteratie', i]['wpsum']}")'''

#print batterij
print("----------------------------------")
import pandas as pd

def create_dataframe(list1, list2,list3):
    # make all lists the same size
    list1 = [round(i,4) for i in list1]
    list2 = [round(i,4) for i in list2]
    list3 = [round(i,4) for i in list3]
    max_len = max(len(list1), len(list2), len(list3))
    list1 += [None] * (max_len - len(list1))
    list2 += [None] * (max_len - len(list2))
    list3 += [None] * (max_len - len(list3))
    df = pd.DataFrame({'Batstate': list1, 'Batcharge': list2, 'Batdischarge': list3})
    return df

df = create_dataframe(N, O, P)
print(df)
#maak dezelfde functie als create_dataframe maar dan voor alle outputs (A tot P) van de controller
def create_dataframe2(list1, list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12):
    # make all lists the same size
    list1 = [round(i,4) for i in list1]
    list2 = [round(i,4) for i in list2]
    list3 = [round(i,4) for i in list3]
    list4 = [round(i,4) for i in list4]
    list5 = [round(i,4) for i in list5]
    list6 = [round(i,4) for i in list6]
    list7 = [round(i,4) for i in list7]
    list8 = [round(i,4) for i in list8]
    list9 = [round(i,4) for i in list9]
    list10 = [round(i,4) for i in list10]
    list11 = [round(i,4) for i in list11]
    list12 = [round(i,4) for i in list12]
    max_len = max(len(list1), len(list2), len(list3), len(list4), len(list5), len(list6), len(list7), len(list8), len(list9), len(list10), len(list11), len(list12))
    list1 += [None] * (max_len - len(list1))
    list2 += [None] * (max_len - len(list2))
    list3 += [None] * (max_len - len(list3))
    list4 += [None] * (max_len - len(list4))
    list5 += [None] * (max_len - len(list5))
    list6 += [None] * (max_len - len(list6))
    list7 += [None] * (max_len - len(list7))
    list8 += [None] * (max_len - len(list8))
    list9 += [None] * (max_len - len(list9))
    list10 += [None] * (max_len - len(list10))
    list11 += [None] * (max_len - len(list11))
    list12 += [None] * (max_len - len(list12))
    df = pd.DataFrame({'Auto': list1, 'Wasmachine': list2, 'Keuken': list3, 'Ebuy': list4, 'Esell': list5, 'Wpsum': list6, 'Aircosum': list7, 'T_in': list8, 'Zonne_energie': list9, 'Batstate': list10, 'Batcharge': list11, 'Batdischarge': list12})
    return df

df2 = create_dataframe2(A, B, C, D, E, F, G, H, I, N, O, P)
import matplotlib.pyplot as plt
df2.plot(kind='bar', subplots = True)
plt.show()
print(df2)

import numpy as np
T_in = []
T_m = []
T_in_time = []
T_m_time = []
for i in range(0,24):
    T_in = T_in + K['Iteratie', i][4].y[0, :].tolist()
    T_m = T_m + K['Iteratie', i][4].y[1, :].tolist()
    T_in_time = T_in_time + [elem + i*3600 for elem in K['Iteratie', i][4].t.tolist()]
    T_m_time = T_m_time + [elem + i*3600 for elem in K['Iteratie', i][4].t.tolist()]
T_in = [i-273.15 for i in T_in]
T_m = [i-273.15 for i in T_m]
T_in_time = [i/(60*60) for i in T_in_time]
T_m_time = [i/(60*60) for i in T_m_time]
plt.plot(T_in_time, T_in, label='T_in')
plt.plot(T_m_time, T_m, label='T_m')
plt.xlabel('Tijd (uur)')                                #label x-as
plt.ylabel('Temperatuur (°C)')                          #label y-as
plt.title('Binnen- en muurtemperatuur zonnehuis')     #titel van de grafiek
plt.grid()                                              #raster op de grafiek
plt.legend(loc='upper left')                           #legende linksboven
plt.show()                                              #toon de grafieken


#testdag negatieve prijzen: 29 december, 3 jan!
#daarnet: 2022-06-03