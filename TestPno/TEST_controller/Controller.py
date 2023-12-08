from Simuleer_warmte_model import simuleer_warmte_model
from Optimalisatie import optimaliseer

def controller(tempinput,priceinput,radiationinput,wm_boolean,auto_boolean, keuken_boolean, thuis):
    #constanten
    delta_t = 1                     # tijdsinterval (h)
    delta_t_simulatie = 0.5         # tijdsinterval (h) voor simulatie
    horizon = 24                    # lengte van de horizon (h)
    zp_opp = 46.2                   # oppervlakte zonnepaneel (m^2)
    eff = 0.2                       # efficientie zonnepaneel
    M = 1000                        # grote M. Wat is dit?
    ewm = 2.5                       # verbruik wasmachine (kW = kWh/h)
    eau = 7.4                       # vermogen laadpaal (kW)
    ekeuken = 2.11                   # vermogen keuken (kW)
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
    K = 273.15                      # constante om van Celsius naar Kelvin te gaan

    batmax = 10000                     #maximale batterijcapaciteit (kWh)
    batmin = 0                      #minimale batterijcapaciteit (kWh)
    bat0 = 0                        #begintoestand batterij (kWh)
    batmaxcharge = batmax                #maximale laadsnelheid batterij (kW)
    batmaxdischarge = batmax             #maximale ontlaadsnelheid batterij (kW)

    #haal data uit database
    temp_out = tempinput
    irradiantie = radiationinput
    netstroom = priceinput

    #Celsius naar Kelvin
    temp_out = [i + K for i in temp_out]
    T_in_0 = T_in_0 + K
    T_m_0 = T_m_0 + K
    T_in_min = T_in_min + K
    T_in_max = T_in_max + K
    T_m_min = T_m_min + K
    T_m_max = T_m_max + K

    #netstroom naar €/kWh
    netstroom = [i/1000 for i in netstroom]

    #bereken zonne energie

    zonne_energie = [i * zp_opp * eff * 0.75 for i in irradiantie]  # lijst met beschikbare zonne-energie (W) per uur
    for i in zonne_energie:
        if i > 7000:
            zonne_energie[zonne_energie.index(i)] = 7000  # maximum vermogen van zonnepanelen is 4750 W
    zonne_energie = [i *0.9 for i in zonne_energie]

    #horizon implementatie
    current_time = start_time                                                       #houdt de huidige tijd bij
    opslag_resultaat = {}                                                           #maak een dictionary om de resultaten van de optimalisatie in op te slaan
    actions = {}                                                                    #maak een dictionary om de definitieve acties van de controller in op te slaan
    attributes = ['auto', 'wm','keuken', 'ebuy', 'esell', 'batstate', 'batcharge', 'batdischarge']      #maak een lijst met de attributen van de dictionary
    for i in attributes:
        actions[i] = []                                                             #initialiseer een lijst voor elk attribuut in de dictionary
    actions['Binnentemperatuur'] = []                                               #initialiseer een lijst voor de binnentemperatuur
    actions['Bouwmassa'] = []                                                       #initialiseer een lijst voor de temperatuur van de bouwmassa
    wp_actions = []                                                                 #maak een lijst voor de acties van de warmtepomp
    airco_actions = []                                                              #maak een lijst voor de acties van de airco
    T_in_simulatie = []                                                             #maak een lijst voor de binnentemperatuur van de simulatie
    T_m_simulatie = []                                                              #maak een lijst voor de temperatuur van de bouwmassa van de simulatie
    T_time_simulatie = []                                                           #maak een lijst voor de tijd van de simulatie
    while current_time < total_time:                                                #zolang de huidige tijd kleiner is dan de totale tijd is de optimalisatie niet voltooid
        # bepaal de horizon lengte, optimaliseer en sla de resultaten op
        if current_time + horizon <= total_time:
            horizon_end = current_time + horizon                                    #einde van de huidige horizon
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zonne_energie[current_time:horizon_end],ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zonne_energie[current_time:horizon_end], ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0] #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0] #aantal uren dat de auto nog aan moet staan
        keuken_aan = keuken_aan - opslag_resultaat['Iteratie', current_time]['keuken'][0] #aantal uren dat de keuken nog aan moet staan

        # sla de resultaten van de optimalisatie voor de current time op. Deze worden de definitieve acties
        for i in attributes:
            actions[i].append(opslag_resultaat['Iteratie', current_time][i][0])
        wp_actions += opslag_resultaat['Iteratie', current_time]['wp'][0:2]
        airco_actions += opslag_resultaat['Iteratie', current_time]['airco'][0:2]

        #batterij update
        bat0 = actions['batstate'][current_time] + actions['batcharge'][current_time] - actions['batdischarge'][current_time] #update de batterijtoestand voor de volgende iteratie

        #simuleer het warmte model van de huidige iteratie naar de volgende iteratie (tijdsvenster schuift op) voor eerste half uur
        [T_in, T_m, T_time] = simuleer_warmte_model(delta_t_simulatie, wp_actions[-2],airco_actions[-2],temp_out[current_time], irradiantie[current_time],T_in_0,T_m_0) #simulatie van het warmtemodel
        T_in_0 = T_in[-1]                                                      #begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]                                                        #begintemperatuur van de bouwmassa voor volgende iteratie
        T_in_simulatie = T_in_simulatie + T_in                                #voeg de binnentemperatuur van de huidige iteratie toe aan de lijst met binnentemperaturen
        T_m_simulatie = T_m_simulatie + T_m                               #voeg de temperatuur van de bouwmassa van de huidige iteratie toe aan de lijst met temperaturen van de bouwmassa
        T_time_simulatie = T_time_simulatie + [elem + 2*current_time*(30*60) for elem in T_time] #voeg de tijd van de huidige iteratie toe aan de lijst met tijden

        #simulatie tweede half uur
        [T_in, T_m, T_time] = simuleer_warmte_model(delta_t_simulatie, wp_actions[-1],airco_actions[-1],temp_out[current_time],irradiantie[current_time], T_in_0,T_m_0)  # simulatie van het warmtemodel
        T_in_0 = T_in[-1]  # begintemperatuur van de binnentemperatuur voor volgende iteratie
        T_m_0 = T_m[-1]  # begintemperatuur van de bouwmassa voor volgende iteratie
        T_in_simulatie = T_in_simulatie + T_in  # voeg de binnentemperatuur van de huidige iteratie toe aan de lijst met binnentemperaturen
        T_m_simulatie = T_m_simulatie + T_m  # voeg de temperatuur van de bouwmassa van de huidige iteratie toe aan de lijst met temperaturen van de bouwmassa
        T_time_simulatie = T_time_simulatie + [elem + (2*current_time+1)*(30*60) for elem in T_time] #voeg de tijd van de huidige iteratie toe aan de lijst met tijden

        #voeg binnentemperatuur uit optimalisatie toe aan actions
        actions['Binnentemperatuur'] += opslag_resultaat['Iteratie', current_time]['T_in'][0:2]
        actions['Bouwmassa'] += opslag_resultaat['Iteratie', current_time]['T_m'][0:2]

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

    #update batterij en temp laatste keer bereid voor op return
    actions['batstate'].append(bat0)
    actions['batstate'] = [(i/batmax)*100 for i in actions['batstate']]

    #optimalisatie return voorbereiden
    T_in_simulatie = [i - K for i in T_in_simulatie]
    T_m_simulatie = [i - K for i in T_m_simulatie]
    T_time_simulatie = [i / (60 * 60) for i in T_time_simulatie]


    #bereid return voor
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
        elif key == 'Binnentemperatuur':
            T_in_final = value
        elif key == 'Bouwmassa':
            T_m_final = value
        elif key == 'batstate':
            batstate_final = value
        elif key == 'batcharge':
            batcharge_final = value
        elif key == 'batdischarge':
            batdischarge_final = value

    zonne_energie_sum = sum(zonne_energie)

    #bereken de kostrpijs_energie met de data opgeslagen in actions
    kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i]/1000 - (1/3)* actions['esell'][i] * netstroom[i]/1000 for i in range(0, total_time))

    #bereid wp_actions en airco_actions voor op return
    wp_actions = [(delta_t_simulatie*i)/1000 for i in wp_actions]
    airco_actions = [(delta_t_simulatie*i)/1000 for i in airco_actions]


    return [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final]

#test: [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final] = controller([14.2, 14.3, 13.7, 13.3, 12.9, 12.7, 12.2, 11.9, 11.5, 11.5, 12.7, 12.9, 13.0, 12.7, 11.4, 13.2, 11.8, 11.3, 11.1, 10.9, 11.1, 11.1, 10.8, 10.4], [92.2, 36.08, 19.63, 22.49, 44.88, 79.0, 117.91, 149.09, 161.51, 148.37, 130.41, 112.8, 107.2, 111.69, 134.67, 149.07, 145.74, 193.3, 200.91, 170.96, 145.54, 140.92, 128.25, 120.92],[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 12.0, 34.0, 66.0, 167.0, 164.0, 148.0, 190.0, 271.0, 45.0, 31.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], True, True, True, False)