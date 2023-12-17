#imports
import numpy as np
from TEST_controller.Simuleer_warmte_model import simuleer_warmte_model
from TEST_controller.Optimalisatie import optimaliseer
import scipy.integrate as integrate


def controller(tempinput,priceinput,radiationinput,wm_boolean,auto_boolean, keuken_boolean, wp_boolean, bat_boolean, thuis):

    #functies
    def reset(thuis, wm_boolean, auto_boolean, keuken_boolean):
        if thuis:
            aankomst = 0
            vertrek = 0
        else:
            aankomst = 17 - 6  # Aankomsttijd (uur van 6h => 17h)
            vertrek = 24 + 6 - 6  # Vertrektijd (uur van 12h => 6h)

        keuken_begin = 17 - 6  # beginttijd (uur van 6h => 17h)
        keuken_einde = 19 - 6  # eindtijd (uur van 6h => 19h)
        wm_aan = 0  # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        auto_aan = 0  # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        keuken_aan = 0  # Aantal uren dat de keuken nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        if wm_boolean:
            wm_aan = 2  # Aantal uren dat de wasmachine nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        if auto_boolean:
            auto_aan = 3  # Aantal uren dat de auto nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        if keuken_boolean:
            keuken_aan = 2  # Aantal uren dat de keuken nog aan moet staan (wordt door optimalisatiefunctie eventueel geüpdatet)
        return aankomst, vertrek, keuken_begin, keuken_einde, wm_aan, auto_aan, keuken_aan

    #constanten
    delta_t = 1                     # tijdsinterval (h)
    delta_t_simulatie = 0.5         # tijdsinterval (h) voor simulatie
    horizon = 24                    # lengte van de horizon (h)
    zp_opp = 46.2                   # oppervlakte zonnepaneel (m^2)
    eff = 0.2                       # efficientie zonnepaneel
    M = 1000                        # grote M. Wat is dit?
    ewm = 2.5                       # verbruik wasmachine (kW = kWh/h)
    eau = 7.4                       # vermogen laadpaal (kW)
    ekeuken = 3.3905                   # vermogen keuken (kW)
    start_time = 0                  # Begin met tijd = 0
    total_time = 24                 # Totaal aantal uren die geoptimaliseerd moeten worden
    if thuis:
        aankomst = 0
        vertrek = 0
    else:
        aankomst = 17-6                 # Aankomsttijd (uur van 6h => 17h)
        vertrek = 24+6-6                    # Vertrektijd (uur van 12h => 6h)

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

    T_in_0 = 20  # begintemperatuur van de binnenlucht (Celsius) voor benadering en simulatie (arbitrair)
    T_m_0 = 20  # begintemperatuur van de bouwmassa (Celsius) voor benadering en simulatie (arbitrair)
    if wp_boolean:
        P_max = 4000                    # maximaal vermogen van de warmtepomp (W)
        P_max_airco = 4000              # maximaal vermogen van de airco (W)
        T_in_min = 20                   # minimale binnentemperatuur (Celsius)
        T_in_max = 22                   # maximale binnentemperatuur (Celsius)
        T_m_min = -10                    # minimale temperatuur van de bouwmassa (Celsius)
        T_m_max = 50                   # maximale temperatuur van de bouwmassa (Celsius)
        T_nothome_min = 16              # minimale binnentemperatuur als er niemand thuis is (Celsius)
        if max(tempinput) > 25:
            T_nothome_max = max(tempinput)              # maximale binnentemperatuur als er niemand thuis is (Celsius)
        else:
            T_nothome_max = 25              # maximale binnentemperatuur als er niemand thuis is (Celsius)
    else:
        P_max = 0                    # maximaal vermogen van de warmtepomp (W)
        P_max_airco = 0              # maximaal vermogen van de airco (W)
        T_in_min = -10                   # minimale binnentemperatuur (Celsius)
        T_in_max = 50                   # maximale binnentemperatuur (Celsius)
        T_m_min = -10                    # minimale temperatuur van de bouwmassa (Celsius)
        T_m_max = 50                   # maximale temperatuur van de bouwmassa (Celsius)
        T_nothome_min = -10              # minimale binnentemperatuur als er niemand thuis is (Celsius)
        T_nothome_max = 50              # maximale binnentemperatuur als er niemand thuis is (Celsius)

    if bat_boolean:
        batmax = 10000                     #maximale batterijcapaciteit (kWh)
        batmin = 0                      #minimale batterijcapaciteit (kWh)
        bat0 = 0                        #begintoestand batterij (kWh)
        batmaxcharge = batmax/2                #maximale laadsnelheid batterij (kW)
        batmaxdischarge = batmax/2             #maximale ontlaadsnelheid batterij (kW)
    else:
        batmax = 0                     #maximale batterijcapaciteit (kWh)
        batmin = 0                      #minimale batterijcapaciteit (kWh)
        bat0 = 0                        #begintoestand batterij (kWh)
        batmaxcharge = 0                #maximale laadsnelheid batterij (kW)
        batmaxdischarge = 0             #maximale ontlaadsnelheid batterij (kW)

    #haal data uit database
    temp_out = tempinput
    irradiantie = radiationinput
    netstroom = priceinput
    for i in netstroom:
        if i < 0:
            netstroom[netstroom.index(i)] = 0

    #Celsius naar Kelvin
    temp_out = [i + 273.15 for i in temp_out]
    T_in_0 = T_in_0 + 273.15
    T_m_0 = T_m_0 + 273.15
    T_in_min = T_in_min + 273.15
    T_in_max = T_in_max + 273.15
    T_m_min = T_m_min + 273.15
    T_m_max = T_m_max + 273.15
    T_nothome_min = T_nothome_min + 273.15
    T_nothome_max = T_nothome_max + 273.15

    #netstroom naar €/kWh
    netstroom = [i/1000 for i in netstroom]

    #bereken zonne energie
    zonne_energie = [i * zp_opp * eff for i in irradiantie]  # lijst met beschikbare zonne-energie (W) per uur
    for i in zonne_energie:
        if i > 7000:
            zonne_energie[zonne_energie.index(i)] = 7000  # maximum vermogen van zonnepanelen is 4750 W
    zonne_energie = [i *0.9 for i in zonne_energie]

    #horizon implementatie
    current_time = start_time                                                       #houdt de huidige tijd bij
    opslag_resultaat = {}                                                           #maak een dictionary om de resultaten van de optimalisatie in op te slaan
    actions = {}                                                                    #maak een dictionary om de definitieve acties van de controller in op te slaan
    attributes = ['auto', 'wm','keuken', 'ebuy', 'esell', 'wpsum', 'aircosum', 'batstate', 'batcharge', 'batdischarge']      #maak een lijst met de attributen van de dictionary
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
            opslag_resultaat['Iteratie', current_time] = optimaliseer(horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zonne_energie[current_time:horizon_end],ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, T_nothome_min, T_nothome_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        else:
            horizon_end = total_time                                                #einde van de huidige horizon, zorgt ervoor dat de controller niet verder dan de totale tijd optimaliseert
            new_horizon = horizon -((current_time + horizon) - total_time)          #nieuwe horizon die niet over totale tijd optimaliseert
            opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zonne_energie[current_time:horizon_end], ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, T_nothome_min, T_nothome_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

        #controleer de acties die de controller heeft gekozen voor dit interval, deze worden de beginvoorwaarden voor het volgende interval
        wm_aan = int(wm_aan - opslag_resultaat['Iteratie', current_time]['wm'][0]) #aantal uren dat de wasmachine nog aan moet staan
        auto_aan = int(auto_aan - opslag_resultaat['Iteratie', current_time]['auto'][0]) #aantal uren dat de auto nog aan moet staan
        keuken_aan = int(keuken_aan - opslag_resultaat['Iteratie', current_time]['keuken'][0]) #aantal uren dat de keuken nog aan moet staan

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

        # reset de acties voor de volgende dag
        if (current_time % 24 == 0) and current_time != 0:
            [aankomst, vertrek, keuken_begin, keuken_einde, wm_aan, auto_aan, keuken_aan] = reset(thuis, wm_boolean,auto_boolean,keuken_boolean)

    #update batterij en temp laatste keer
    actions['batstate'].append(bat0)

    # foutcontrole
    if wp_boolean:
        T_in_np = np.array(T_in_simulatie)
        T_time_np = np.array(T_time_simulatie)
        if thuis:
            int_arr_down = np.array([])
            int_arr_up = np.array([])
            mask = T_in_np < T_in_min
            int_arr_down = T_in_np[mask]
            if len(int_arr_down) == 0:
                err_down = 0
            else:
                err_down = integrate.simpson(np.full(len(int_arr_down),T_in_min)) - integrate.simpson(int_arr_down)
            mask = T_in_np > T_in_max
            int_arr_up = T_in_np[mask]
            if len(int_arr_up) == 0:
                err_up = 0
            else:
                err_up = integrate.simpson(int_arr_up) - integrate.simpson(np.full(len(int_arr_up),T_in_max))
            tot_opp = (T_in_max- T_in_min) * (24*60*60)
            tot_fout = ((err_down+ err_up)/tot_opp)*100

        else:
            int_arr_down_home = np.array([])
            int_arr_up_home = np.array([])
            int_arr_down_nothome = np.array([])
            int_arr_up_nothome = np.array([])

            mask = T_in_np[aankomst*3600:vertrek*3600] < T_in_min
            int_arr_down_home = T_in_np[aankomst*3600:vertrek*3600][mask]
            if len(int_arr_down_home) == 0:
                err_down_home = 0
            else:
                err_down_home = integrate.simpson(np.full(len(int_arr_down_home),T_in_min)) - integrate.simpson(int_arr_down_home)
            mask = T_in_np[aankomst*3600:vertrek*3600] > T_in_max
            int_arr_up_home = T_in_np[aankomst*3600:vertrek*3600][mask]
            if len(int_arr_up_home) == 0:
                err_up_home = 0
            else:
                err_up_home = integrate.simpson(int_arr_up_home) - integrate.simpson(np.full(len(int_arr_up_home),T_in_max))
            mask = T_in_np[:aankomst*3600] < T_nothome_min
            int_arr_down_nothome = T_in_np[:aankomst*3600][mask]
            if len(int_arr_down_nothome) == 0:
                err_down_nothome = 0
            else:
                err_down_nothome = integrate.simpson(np.full(len(int_arr_down_nothome),T_nothome_min)) - integrate.simpson(int_arr_down_nothome)
            mask = T_in_np[:aankomst*3600] > T_nothome_max
            int_arr_up_nothome = T_in_np[:aankomst*3600][mask]
            if len(int_arr_up_nothome) == 0:
                err_up_nothome = 0
            else:
                err_up_nothome = integrate.simpson(int_arr_up_nothome) - integrate.simpson(np.full(len(int_arr_up_nothome),T_nothome_max))
            tot_fout = ((err_down_home+err_up_home)/((T_in_max-T_in_min)*(vertrek-aankomst)*60*60) + (err_down_nothome+err_up_nothome)/((T_nothome_max-T_nothome_min)*((24-(vertrek-aankomst))*60*60)))*100
    else:
        tot_fout = 0
    #optimalisatie laatste keer
    T_in_simulatie = [i - 273.15 for i in T_in_simulatie]
    T_m_simulatie = [i - 273.15 for i in T_m_simulatie]
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
        elif key == 'wpsum':
            wpsum_final = value
        elif key == 'aircosum':
            aircosum_final = value
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

    #som ebuy en esell in kWh
    ebuy_final_sum = sum(ebuy_final)
    esell_final_sum = sum(esell_final)

    #batstate in %
    if bat_boolean:
        batstate_final = [(i/batmax)*100 for i in batstate_final]
    else:
        batstate_final = list(np.zeros(25))

    zonne_energie_sum = sum(zonne_energie)
    #bereken de kostrpijs_energie met de data opgeslagen in actions
    kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i] - (1/3)* actions['esell'][i] * netstroom[i] for i in range(0, total_time))


    return [auto_final, wm_final, keuken_final, ebuy_final, esell_final, ebuy_final_sum, esell_final_sum, wpsum_final, aircosum_final, wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, opslag_resultaat, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final, tot_fout]