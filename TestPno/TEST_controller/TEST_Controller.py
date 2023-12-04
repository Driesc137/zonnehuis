#file in progress voor controller demodag
#notes:
#constraint auto aanpassen: contraint niet per inteval maar voor 50-80%, bovendien eventueel input van gebruiker via database
#to-do:
#verliezen zonne energie nog 0,75% verlies op tot zonne energie binnen
#zonne installatie:
    #zonne energie binnen = irradiatie * oppervlakte * efficientie * 75% door helling enzo
    #dit kan max 4750 W zijn
    #hier gaat nog es 10% af dus max 4750 W * 90% = 4275 W
#batterij erin gooien

#imports

from Simuleer_warmte_model import simuleer_warmte_model
from GetfromDB import getFromDB
from GetfromDB import getTempFromDB
from Optimalisatie import optimaliseer
import numpy as np

def controller(tempinput,priceinput,radiationinput,wm_boolean,auto_boolean):
    #constanten
    delta_t = 1                     # tijdsinterval (h)
    horizon = 24                    # lengte van de horizon (h)
    zp_opp = 32                   # oppervlakte zonnepaneel (m^2)
    eff = 0.2                       # efficientie zonnepaneel
    M = 1000                        # grote M. Wat is dit?
    ewm = 2.5                       # verbruik wasmachine (kW = kWh/h)
    eau = 7.4                       # vermogen laadpaal (kW)
    start_time = 0                  # Begin met tijd = 0
    total_time = 24                 # Totaal aantal uren die geoptimaliseerd moeten worden
    wm_aan = 0                     # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    auto_aan = 0                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if wm_boolean:
        wm_aan = 2                      # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if auto_boolean:
        auto_aan = 3                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)

    T_in_0 = 20                     # begintemperatuur van de binnenlucht (Celsius) voor benadering en simulatie (arbitrair)
    T_m_0 = 20                      # begintemperatuur van de bouwmassa (Celsius) voor benadering en simulatie (arbitrair)
    P_max = 4000                    # maximaal vermogen van de warmtepomp (W)
    P_max_airco = 4000              # maximaal vermogen van de airco (W)
    T_in_min = 19                   # minimale binnentemperatuur (Celsius)
    T_in_max = 22                   # maximale binnentemperatuur (Celsius)
    T_m_min = -10                    # minimale temperatuur van de bouwmassa (Celsius)
    T_m_max = 50                   # maximale temperatuur van de bouwmassa (Celsius)

    #haal data uit database
    temp_out = tempinput
    irradiantie = radiationinput
    netstroom = priceinput

    #bereken zonne energie

    zonne_energie = [i * zp_opp * eff * 0.75 for i in irradiantie]  # lijst met beschikbare zonne-energie (W) per uur
    for i in zonne_energie:
        if i > 4750:
            zonne_energie[zonne_energie.index(i)] = 4750  # maximum vermogen van zonnepanelen is 4750 W
    zonne_energie = [i *0.9 for i in zonne_energie]

    #horizon implementatie
    current_time = start_time                                                       #houdt de huidige tijd bij
    opslag_resultaat = {}                                                           #maak een dictionary om de resultaten van de optimalisatie in op te slaan
    opslag_simulatie = {}                                                          #maak een dictionary om de resultaten van de simulatie in op te slaan
    actions = {}                                                                    #maak een dictionary om de definitieve acties van de controller in op te slaan
    attributes = ['auto', 'wm', 'ebuy', 'esell', 'wpsum', 'aircosum']                               #maak een lijst met de attributen van de dictionary
    for i in attributes:
        actions[i] = []                                                             #initialiseer een lijst voor elk attribuut in de dictionary
    actions['Binnentemperatuur'] = []                                               #initialiseer een lijst voor de binnentemperatuur

    while current_time < total_time:                                                #zolang de huidige tijd kleiner is dan de totale tijd is de optimalisatie niet voltooid
        actions['Binnentemperatuur'].append(T_in_0)                                 #sla de binnentemperatuur op
        # bepaal de horizon lengte, optimaliseer en sla de resultaten op
        if current_time + horizon <= total_time:
            horizon_end = current_time + horizon                                    #einde van de huidige horizon
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zp_opp, eff, ewm, eau, delta_t, M, wm_aan, auto_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max)     #optimalisatie a.d.h.v. benadering

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end],  zp_opp, eff, ewm, eau, delta_t, M, wm_aan, auto_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max)     #optimalisatie a.d.h.v. benadering

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0] #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0] #aantal uren dat de auto nog aan moet staan

        # sla de resultaten van de optimalisatie voor de current time op. Deze worden de definitieve acties
        for i in attributes:
            actions[i].append(opslag_resultaat['Iteratie', current_time][i][0])

        #simuleer het warmte model van de huidige iteratie naar de volgende iteratie (tijdsvenster schuift op)
        [T_in, T_m, T_in_time, T_m_time, oplossing] = simuleer_warmte_model(delta_t, actions['wpsum'][current_time],actions['aircosum'][current_time],temp_out[current_time], irradiantie[current_time],T_in_0,T_m_0) #simulatie van het warmtemodel
        T_in_0 = T_in[-1]                                                      #begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]                                                        #begintemperatuur van de bouwmassa voor volgende iteratie
        opslag_simulatie['Iteratie', current_time] = [T_in, T_m, T_in_time, T_m_time, oplossing]               #sla de resultaten van de simulatie op

        #verschuif horizon
        current_time += 1                                                           #verschuif de horizon met 1 uur


    #print(opslag_resultaat)
    print("----------------------------------")

    for key, value in actions.items():
        locals()[key] = value
        if key == 'auto':
            auto_final = value
        elif key == 'wm':
            wm_final = value
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
    print(f"zonne_energie_sum: {sum(zonne_energie)}")
    print("----------------------------------")

    #bereken de kostrpijs_energie met de data opgeslagen in actions
    kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i]/1000 - (1/3)* actions['esell'][i] * netstroom[i]/1000 for i in range(0, total_time))
    #print("De oplossing is €", kostprijs_energie)
    print(f"{"kostprijs_energie"}: {kostprijs_energie}")
    print("----------------------------------")
    print(opslag_resultaat['Iteratie', 0]['result'])
    print("----------------------------------")


    return [auto_final, wm_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final, opslag_simulatie]  #    return [auto_final, wm_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final]
    #print(f"Geheugengrootte van de dictionary: {geheugengrootte_dict} bytes")

testdag = '2022-01-03'
dataset1 = getTempFromDB(testdag)                                       #haal temperatuur en irradiantie van dag 1 uit database
temp_out = dataset1[0]
#temp_out = [30,25,28,29,30,26,25,29,29,30,30,30,30,30,30,30,30,30,31,31,31,31,28,29,31,31,31,31]#haal temperatuur uit dataset1 (°C)
irradiantie = dataset1[1]
#irradiantie = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
netstroom = getFromDB(testdag)                                          #haal netstroom van dag 1 uit database
boolean1 = True
boolean2 = True
[A,B,C,D,E,F,G, H] = controller(temp_out, netstroom, irradiantie, boolean1, boolean2)

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
min_T_in = min(G)
max_T_in = max(G)
gem_T_in = sum(G)/len(G)
print(f"min_T_in: {min_T_in}")
print(f"max_T_in: {max_T_in}")
print(f"gem_T_in: {gem_T_in}")

#maak een plot van de oplossing van de simulatie opslag (oplossing) over de hele dag: plak de lijsten uit oplossing.y en oplossing.t achter elkaar
import matplotlib.pyplot as plt
import numpy as np
T_in = []
T_m = []
T_in_time = []
T_m_time = []
for i in range(0,24):
    T_in = T_in + H['Iteratie', i][4].y[0, :].tolist()
    T_m = T_m + H['Iteratie', i][4].y[1, :].tolist()
    T_in_time = T_in_time + [elem + i*3600 for elem in H['Iteratie', i][4].t.tolist()]
    T_m_time = T_m_time + [elem + i*3600 for elem in H['Iteratie', i][4].t.tolist()]
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