#imports
import numpy as np
from Test_Simuleer_Warmte_model import simuleer_warmte_model
from GetfromDB import getFromDB
from GetfromDB import getTempFromDB
from Test_Optimalisatie import optimaliseer
import datetime

def controller_uitbreiding(dag, totaal_dagen, thuis, wm_boolean, auto_boolean, keuken_boolean):

    #functies
    def get_n_days(n, first_day):
        first_day = datetime.datetime.strptime(first_day, '%Y-%m-%d')
        future_dates = []

        for i in range(n):
            future_date = first_day + datetime.timedelta(days=i)
            future_dates.append(future_date.strftime('%Y-%m-%d'))

        return future_dates
    def controller(tempinput,priceinput,radiationinput,wm_boolean,auto_boolean, keuken_boolean, thuis, uren):
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
        ekeuken = 2.11                   # vermogen keuken (kW)
        start_time = 0                  # Begin met tijd = 0
        total_time = uren                 # Totaal aantal uren die geoptimaliseerd moeten worden
        [aankomst, vertrek, keuken_begin, keuken_einde, wm_aan, auto_aan, keuken_aan] = reset(thuis, wm_boolean, auto_boolean, keuken_boolean)

        T_in_0 = 20                     # begintemperatuur van de binnenlucht (Celsius) voor benadering en simulatie (arbitrair)
        T_m_0 = 20                      # begintemperatuur van de bouwmassa (Celsius) voor benadering en simulatie (arbitrair)
        P_max = 4000                    # maximaal vermogen van de warmtepomp (W)
        P_max_airco = 4000              # maximaal vermogen van de airco (W)
        T_in_min = 20                   # minimale binnentemperatuur (Celsius)
        T_in_max = 22                   # maximale binnentemperatuur (Celsius)
        T_m_min = -10                    # minimale temperatuur van de bouwmassa (Celsius)
        T_m_max = 50                   # maximale temperatuur van de bouwmassa (Celsius)
        T_nothome_min = 16  # minimale binnentemperatuur als er niemand thuis is (Celsius)
        if max(tempinput) > 25:
            T_nothome_max = max(tempinput)  # maximale binnentemperatuur als er niemand thuis is (Celsius)
        else:
            T_nothome_max = 25  # maximale binnentemperatuur als er niemand thuis is (Celsius)
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
        temp_out = [i + 273.15 for i in temp_out]
        T_in_0 = T_in_0 + 273.15
        T_m_0 = T_m_0 + 273.15
        T_in_min = T_in_min + 273.15
        T_in_max = T_in_max + 273.15
        T_m_min = T_m_min + 273.15
        T_m_max = T_m_max + 273.15

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
        opslag_simulatie = {}                                                          #maak een dictionary om de resultaten van de simulatie in op te slaan
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
                opslag_resultaat['Iteratie', current_time] = optimaliseer(new_horizon, irradiantie[current_time:horizon_end], netstroom[current_time:horizon_end], zonne_energie[current_time:horizon_end], ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, temp_out[current_time: horizon_end], P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, T_nothome_min, T_nothome_max,thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, bat0)     #optimalisatie a.d.h.v. benadering

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

            #reset de acties voor de volgende dag
            if (current_time % 24 == 0) and current_time != 0:
                print("Dag")
                [aankomst, vertrek, keuken_begin, keuken_einde, wm_aan, auto_aan, keuken_aan] = reset(thuis, wm_boolean,auto_boolean,keuken_boolean)

        #update batterij en temp laatste keer
        actions['batstate'].append(bat0)

        #optimalisatie laatste keer
        T_in_simulatie = [i - 273.15 for i in T_in_simulatie]
        T_m_simulatie = [i - 273.15 for i in T_m_simulatie]
        T_time_simulatie = [i / (60 * 60) for i in T_time_simulatie]

        #bereid return voor
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
            elif key == 'Bouwmassa':
                T_m_final = value
            elif key == 'batstate':
                batstate_final = value
            elif key == 'batcharge':
                batcharge_final = value
            elif key == 'batdischarge':
                batdischarge_final = value
            print(f"{key}: {value}")

        print("----------------------------------")
        print(f"zonne_energie: {zonne_energie}")
        zonne_energie_sum = sum(zonne_energie)
        print(f"zonne_energie_sum: {zonne_energie_sum}")
        print("----------------------------------")

        #bereken de kostrpijs_energie met de data opgeslagen in actions
        kostprijs_energie = sum(actions['ebuy'][i] * netstroom[i] - (1/3)* actions['esell'][i] * netstroom[i] for i in range(0, total_time))
        #print("De oplossing is €", kostprijs_energie)
        print(f"kostprijs_energie: {kostprijs_energie}")
        print("----------------------------------")
        print(opslag_resultaat['Iteratie', 0]['result'])
        print("----------------------------------")


        return [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wpsum_final, aircosum_final, wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, opslag_resultaat, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final]  #    return [auto_final, wm_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final]

    testdagen = get_n_days(totaal_dagen, dag)
    temp_out = []
    irradiantie = []
    netstroom = []
    for i in testdagen:
        temp_out += getTempFromDB(i)[0]
        irradiantie += getTempFromDB(i)[1]
        netstroom += getFromDB(i)

    uren_tot = 24 * totaal_dagen

    booleanwm = wm_boolean
    booleanauto = auto_boolean
    booleankeuken = keuken_boolean
    thuis = thuis
    #print inputs
    print("-----------------------------------")
    print(f"wm input: {booleanwm}")
    print(f"auto input: {booleanauto}")
    print(f"keuken input: {booleankeuken}")
    print(f"thuis input: {thuis}")
    for i in testdagen:
        print(f"dagen input: {i}")
    print("-----------------------------------")

    [auto_final, wm_final, keuken_final, ebuy_final, esell_final, wpsum_final, aircosum_final,wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, opslag_resultaat, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final] = controller(temp_out, netstroom, irradiantie, booleanwm, booleanauto, booleankeuken, thuis, uren_tot)

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
    min_T_in = min(T_in_final)
    max_T_in = max(T_in_final)
    gem_T_in = sum(T_in_final)/len(T_in_final)
    print(f"min_T_in: {min_T_in}")
    print(f"max_T_in: {max_T_in}")
    print(f"gem_T_in: {gem_T_in}")

    '''#print alle T_in uit opslag_simulatie
    print("----------------------------------")
    for i in range(0,24):
        print(f"T_in_{i}: {opslag_resultaat['Iteratie', i]['T_in']}")
    for i in range(0,24):
        print(f"vermogen_{i}: {opslag_resultaat['Iteratie', i]['wpsum']}")
    print("----------------------------------")
    #print alle wp en airco acties uit opslag_resultaat
    print("----------------------------------")
    for i in range(0,24):
        print(f"wp_{i}: {opslag_resultaat['Iteratie', i]['wp']}")
    for i in range(0,24):
        print(f"airco_{i}: {opslag_resultaat['Iteratie', i]['airco']}")
    print("----------------------------------")
    print(f"wp_actions: {wp_actions}")
    print(f"airco_actions: {airco_actions}")'''
    #print batterij
    print("----------------------------------")
    '''import pandas as pd

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

    df = create_dataframe(batstate_final, batcharge_final, batdischarge_final)
    print(df)
    df3 = create_dataframe(wp_actions, airco_actions, T_in_final)
    print(df3)
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
        df = pd.DataFrame({'Auto': list1, 'Wasmachine': list2, 'Keuken': list3, 'Ebuy': list4, 'Esell': list5, 'Wpsum': list6, 'Aircosum': list7, 'Zonne_energie': list9, 'Batstate': list10, 'Batcharge': list11, 'Batdischarge': list12})
        return df

    df2 = create_dataframe2(auto_final, wm_final, keuken_final, ebuy_final, esell_final, wpsum_final, aircosum_final, T_in_final, zonne_energie, batstate_final, batcharge_final, batdischarge_final)
    import matplotlib.pyplot as plt
    df2.plot(kind='bar', subplots = True)
    plt.subplots_adjust(hspace=0.9, top=0.95,bottom=0.05)
    plt.show(block=False)

    #plot de binnentemperatuur en de temperatuur van de bouwmassa
    plt.figure()
    plt.plot(T_time_simulatie, T_in_simulatie, label='T_in')
    plt.plot(T_time_simulatie, T_m_simulatie, label='T_m')
    uren = np.linspace(0, uren_tot, uren_tot*60*60)
    mintemp = min(min(T_in_simulatie), min(T_m_simulatie))

    if thuis:
        plt.fill_between(T_time_simulatie, mintemp, T_in_simulatie, alpha=0.5, label='Thuis')
    if not thuis:
        for i in range(0, int(uren_tot/24)):
            plt.fill_between(T_time_simulatie, mintemp, T_in_simulatie, where=((uren >= (i*24)+11) & (uren <= (i*24)+24)), alpha=0.5, label='Thuis')
    plt.plot(T_time_simulatie, [20 for i in T_time_simulatie], label='T_min')
    plt.plot(T_time_simulatie, [22 for i in T_time_simulatie], label='T_max')
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Temperatuur (°C)')                          #label y-as
    plt.title('Binnen- en muurtemperatuur zonnehuis')     #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.legend(loc='upper left')                           #legende linksboven
    plt.show(block=False)                                              #toon de grafiek
    plt.figure()
    plt.plot(range(len(temp_out)), temp_out, label='T_out')
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Temperatuur (°C)')                          #label y-as
    plt.title('Buitentemperatuur zonnehuis')     #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.legend(loc='upper left')                           #legende linksboven
    plt.show()                                              #toon de grafieken'''

    return auto_final, wm_final, keuken_final, ebuy_final, esell_final,wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final

[auto_final, wm_final, keuken_final, ebuy_final, esell_final,wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum, T_in_simulatie, T_m_simulatie, T_time_simulatie, kostprijs_energie, batstate_final, batcharge_final, batdischarge_final] = controller_uitbreiding('2022-03-25', 5, False, True, True, True)