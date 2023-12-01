#file in progress voor controller demodag
#notes:
#constraint auto aanpassen: contraint niet per inteval maar voor 50-80%, bovendien eventueel input van gebruiker via database
#optimalisatie per kwartier ipv per uur --> nauwkeuriger
#airco
#to-do:
#auto niet per tijdslot maar per percentage
#batterij erin gooien
#uitzoeken hoe controller data opslaat in database, krijgt van interface en welke, en hoe terug naar interface sturen

'''overzicht:
- imports
- constanten
- haal data uit database
- pyomo model
- contraints
- objective
- horizon (loop)
    - benadering horizon
    - optimalisatie
    - simulatie 1 uur (of 1 kwartier)
- resultaten
- naar database'''

#imports

from TEST_controller.Simuleer_warmte_model import simuleer_warmte_model
from TEST_controller.Benader_warmte_model import benader_warmte_model
from TEST_controller.Benader_warmte_model_start import benader_warmte_model_start
from TEST_controller.GetfromDB import getFromDB
from TEST_controller.GetfromDB import getTempFromDB
from TEST_controller.Optimalisatie import optimaliseer
import numpy as np 
'''
from Simuleer_warmte_model import simuleer_warmte_model
from Benader_warmte_model import benader_warmte_model
from Benader_warmte_model_start import benader_warmte_model_start
from GetfromDB import getFromDB
from GetfromDB import getTempFromDB
from Optimalisatie import optimaliseer
import numpy as np '''

def controller(templist1,pricelist1,radiationlist1,wm_boolean,auto_boolean):
    #constanten
    delta_t = 1                     # tijdsinterval (h)
    horizon = 24                    # lengte van de horizon (h)
    zp_opp = 22.4                   # oppervlakte zonnepaneel (m^2)
    eff = 0.2                       # efficientie zonnepaneel
    M = 1000                        # grote M. Wat is dit?
    ewm = 2.5                       # verbruik wasmachine (kW = kWh/h)
    eau = 7.4                       # vermogen laadpaal (kW)
    start_time = 0                  # Begin met tijd = 0
    total_time = 24                 # Totaal aantal uren die geoptimaliseerd moeten worden
    dag_simulatie_1 = '2022-06-01'  # Dag 1 waarop de simulatie plaatsvindt
    dag_simulatie_2 = '2022-06-02'  # Dag 2 waarop de simulatie plaatsvindt
    wm_aan = 0                     # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    auto_aan = 0                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if wm_boolean:
        wm_aan = 2                      # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    if auto_boolean:
        auto_aan = 3                    # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
    T_in_0 = 20                     # begintemperatuur van de binnenlucht (Celsius) voor benadering en simulatie (arbitrair)
    T_m_0 = 18                      # begintemperatuur van de bouwmassa (Celsius) voor benadering en simulatie (arbitrair)
    P_max = 4000                    # maximaal vermogen van de warmtepomp (W)
    T_in_min = 19                   # minimale binnentemperatuur (Celsius)
    T_in_max = 30000                   # maximale binnentemperatuur (Celsius)
    T_m_min = 0                    # minimale temperatuur van de bouwmassa (Celsius)
    T_m_max = 30000                   # maximale temperatuur van de bouwmassa (Celsius)

    #haal data uit database
    dataset1 = getTempFromDB(dag_simulatie_1)                                       #haal temperatuur en irradiantie van dag 1 uit database
    temp_out = dataset1[0]                                                          #haal temperatuur uit dataset1 (°C)
    irradiantie = dataset1[1]                                                       #haal irradiantie uit dataset1 (kWh/m^2)
    dataset2 = getTempFromDB(dag_simulatie_2)                                       #haal temperatuur en irradiantie van dag 2 uit database
    temp_out.extend(dataset2[0])                                                    #voeg temperatuur van dag 2 toe aan temperatuur van dag 1
    irradiantie.extend(dataset2[1])                                                 #voeg irradiantie van dag 2 toe aan irradiantie van dag 1
    netstroom = getFromDB(dag_simulatie_1)                                          #haal netstroom van dag 1 uit database
    netstroom.extend(getFromDB(dag_simulatie_2))                                    #voeg netstroom van dag 2 toe aan netstroom van dag 1
    temp_out = templist1
    irradiantie = radiationlist1
    netstroom = pricelist1
    #horizon implementatie
    current_time = start_time                                                       #houdt de huidige tijd bij
    wp = np.zeros(total_time)                                                       #initialiseer een lijst voor de warmtepomp
    wp = list(wp)                                                                   #zet de lijst om naar een lijst met floats
    opslag_resultaat = {}                                                           #maak een dictionary om de resultaten van de optimalisatie in op te slaan
    opslag_benadering = {}                                                          #maak een dictionary om de resultaten van de benadering in op te slaan
    opslag_simulatie = {}                                                          #maak een dictionary om de resultaten van de simulatie in op te slaan
    actions = {}                                                                    #maak een dictionary om de definitieve acties van de controller in op te slaan
    attributes = ['auto', 'wm', 'ebuy', 'esell', 'wpsum']                               #maak een lijst met de attributen van de dictionary
    for i in attributes:
        actions[i] = []                                                             #initialiseer een lijst voor elk attribuut in de dictionary
    actions['kostprijs_energie'] = []                                               #initialiseer een lijst voor de kostprijs van de energie
    actions['Binnentemperatuur'] = []                                               #initialiseer een lijst voor de binnentemperatuur

    while current_time < total_time:                                                #zolang de huidige tijd kleiner is dan de totale tijd is de optimalisatie niet voltooid
        actions['Binnentemperatuur'].append(T_in_0)                                 #sla de binnentemperatuur op
        # bepaal de horizon lengte, optimaliseer en sla de resultaten op
        if current_time + horizon <= total_time:
            horizon_end = current_time + horizon                                    #einde van de huidige horizon
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zp_opp, eff, ewm, eau, delta_t, M, wm_aan, auto_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, T_in_min, T_in_max, T_m_min, T_m_max)     #optimalisatie a.d.h.v. benadering
            for i in range(0,horizon):
                wp[current_time+i] = opslag_resultaat['Iteratie', current_time]['wpsum'][i]      #de volgende benadering/voorspelling gebeurt a.d.h.v. deze resultaten
            #[T_in, T_m] = benader_warmte_model(horizon, opslag_resultaat['Iteratie', current_time]['wp'], temp_out[current_time:horizon_end],irradiantie[current_time:horizon_end], T_in_0,T_m_0)  # benadering/voorspelling van het warmtemodel
            #opslag_benadering['Iteratie', current_time] = [T_in, T_m]  # sla de resultaten van de benadering op

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end],  zp_opp, eff, ewm, eau, delta_t, M, wm_aan, auto_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, T_in_min, T_in_max, T_m_min, T_m_max)     #optimalisatie a.d.h.v. benadering
            for i in range(0,new_horizon):
                wp[current_time+i] = opslag_resultaat['Iteratie', current_time]['wpsum'][i]     #de volgende benadering/voorspelling gebeurt a.d.h.v. deze resultaten
            #[T_in, T_m] = benader_warmte_model(new_horizon, wp[current_time:horizon_end],temp_out[current_time:horizon_end], irradiantie[current_time:horizon_end] * 1000,T_in_0, T_m_0)  # benadering/voorspelling van het warmtemodel
            #opslag_benadering['Iteratie', current_time] = [T_in, T_m]  # sla de resultaten van de benadering op

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0] #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0] #aantal uren dat de auto nog aan moet staan

        # sla de resultaten van de optimalisatie voor de current time op. Deze worden de definitieve acties
        for i in attributes:
            actions[i].append(opslag_resultaat['Iteratie', current_time][i][0])
        actions['kostprijs_energie'].append(opslag_resultaat['Iteratie', current_time]['kostprijs_energie'])

        #simuleer het warmte model van de huidige iteratie naar de volgende iteratie (tijdsvenster schuift op)
        [T_in, T_m, T_in_time, T_m_time] = simuleer_warmte_model(delta_t, actions['wpsum'][current_time],temp_out[current_time], irradiantie[current_time],T_in_0,T_m_0) #simulatie van het warmtemodel
        T_in_0 = T_in[-1]                                                      #begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]                                                        #begintemperatuur van de bouwmassa voor volgende iteratie
        opslag_simulatie['Iteratie', current_time] = [T_in, T_m, T_in_time, T_m_time]               #sla de resultaten van de simulatie op


        current_time += 1                                                           #verschuif de horizon met 1 uur

    '''  for i in range(0,total_time):
        print(opslag_resultaat['Iteratie', i]['auto'])
    for i in range(0,total_time):
        print(opslag_resultaat['Iteratie', i]['wm'])
    for i in range(0,total_time):
        print(opslag_resultaat['Iteratie', i]['ebuy'])
    for i in range(0,total_time):
        print(opslag_resultaat['Iteratie', i]['esell'])
    for i in range(0,total_time):
        print(opslag_resultaat['Iteratie', i]['wp'])'''
    #print(opslag_resultaat)
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
        elif key == 'kostprijs_energie':
            kostprijs_energie_final = value
        elif key == 'Binnentemperatuur':
            T_in_final = value
        #print(f"{key}: {value}")

    #bereken de kostrpijs_energie met de data opgeslagen in actions
    kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i]/1000 - (1/3)* actions['esell'][i] * netstroom[i]/1000 for i in range(0, total_time))
    #print("De oplossing is €", kostprijs_energie)
    print(kostprijs_energie)

    import sys

    geheugengrootte_dict = sys.getsizeof(opslag_resultaat)
    geheugengrootte_dict += sys.getsizeof(opslag_benadering)
    geheugengrootte_dict += sys.getsizeof(opslag_simulatie)
    return [auto_final,wm_final,ebuy_final,esell_final,wpsum_final,T_in_final]
    #print(f"Geheugengrootte van de dictionary: {geheugengrootte_dict} bytes")

dataset1 = getTempFromDB('2022-01-01')                                       #haal temperatuur en irradiantie van dag 1 uit database
temp_out = dataset1[0]                                                          #haal temperatuur uit dataset1 (°C)
irradiantie = dataset1[1] 
netstroom = getFromDB('2022-01-01')                                          #haal netstroom van dag 1 uit database
boolean1 = True
boolean2 = True
[A,B,C,D,E,F] = controller(temp_out,netstroom,irradiantie,boolean1,boolean2)
print(E)
print(len(E))
print(len((F)))
