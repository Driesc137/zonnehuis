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

from TEST_controller.Simuleer_warmte_model import simuleer_warmte_model
from TEST_controller.GetfromDB import getFromDB
from TEST_controller.GetfromDB import getTempFromDB
from TEST_controller.Optimalisatie import optimaliseer
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
    if thuis:
        keuken_begin = 0
        keuken_einde = 0
    else:
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

    while current_time < total_time:                                                #zolang de huidige tijd kleiner is dan de totale tijd is de optimalisatie niet voltooid
        actions['Binnentemperatuur'].append(T_in_0)                                 #sla de binnentemperatuur op
        # bepaal de horizon lengte, optimaliseer en sla de resultaten op
        if current_time + horizon <= total_time:
            horizon_end = current_time + horizon                                    #einde van de huidige horizon
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zp_opp, eff, ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end],  zp_opp, eff, ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0] #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0] #aantal uren dat de auto nog aan moet staan
        keuken_aan = keuken_aan - opslag_resultaat['Iteratie', current_time]['keuken'][0] #aantal uren dat de keuken nog aan moet staan

        # sla de resultaten van de optimalisatie voor de current time op. Deze worden de definitieve acties
        for i in attributes:
            actions[i].append(opslag_resultaat['Iteratie', current_time][i][0])

        #batterij update
        bat0 = actions['batstate'][current_time] + actions['batcharge'][current_time] - actions['batdischarge'][current_time] #update de batterijtoestand voor de volgende iteratie


        #simuleer het warmte model van de huidige iteratie naar de volgende iteratie (tijdsvenster schuift op)
        [T_in, T_m, T_in_time, T_m_time, oplossing] = simuleer_warmte_model(delta_t, actions['wpsum'][current_time],actions['aircosum'][current_time],temp_out[current_time], irradiantie[current_time],T_in_0,T_m_0) #simulatie van het warmtemodel
        T_in_0 = T_in[-1]                                                      #begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]                                                        #begintemperatuur van de bouwmassa voor volgende iteratie
        opslag_simulatie['Iteratie', current_time] = [T_in, T_m, T_in_time, T_m_time, oplossing]               #sla de resultaten van de simulatie op

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
        print(current_time)
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

    T_in = []
    
    for i in range(0,24):
        T_in = T_in + opslag_simulatie['Iteratie', i][4].y[0, :].tolist()
       
    T_in = [i-273.15 for i in T_in]
    return [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final, zonne_energie, zonne_energie_sum, opslag_simulatie, opslag_resultaat, kostprijs_energie,T_in, batstate_final, batcharge_final, batdischarge_final]  #    return [auto_final, wm_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final]
    #print(f"Geheugengrootte van de dictionary: {geheugengrootte_dict} bytes")