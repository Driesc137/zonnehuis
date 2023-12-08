import pyomo.environ as pe
import pyomo.opt as po

def optimaliseer(horizon, irradiantie, netstroom, zonne_energie, ewm, eau, ekeuken, delta_t, M, wm_aan, auto_aan, keuken_aan, T_in_0, T_m_0, T_out, P_max, P_max_airco, T_in_min, T_in_max, T_m_min, T_m_max, T_nothome_min, T_nothome_max, thuis, aankomst, vertrek, keuken_begin, keuken_einde, batmax, batmin, batmaxcharge, batmaxdischarge, batstart):

    #defenitie functies
    def extend_list(L, N):              #functie om lijsten te verlengen
        temp_list = []                  #maak een tijdelijke lijst
        for i in L:                     #voor elk element in de lijst L
            temp_list.extend([i] * N)   #voeg het element N keer toe aan de tijdelijke lijst
        return temp_list                #geef de tijdelijke lijst terug

    m = pe.ConcreteModel(name='Optimalisatie')  # maak een concreet model
    #warmtepomp parameters
    t0 = 0  # begintijdstip
    t_end = horizon * 60 * 60  # aantal seconden in de horizon
    N = 2  # nauwkeurigheid benadering: N=2 => berekening om het half uur, N=4 => berekening om het kwartier !voorwaartse methode van Euler divergeert voor N=1
    n = N * horizon  # aantal stappen = ieder uur opgedeeld in 2 stappen => elk half uur een stap
    h = (t_end - t0) / (n)  # stapgrootte, horizon wordt opgedeeld in gelijke stukken van een half uur

    # Parameters van de vergelijkingen van het model
    C_i = 2.44 * 10 ** 6  # warmtecapaciteit van de binnenlucht (J/K)
    C_m = 9.40 * 10 ** 7  # warmtecapaciteit van de bouwmassa (J/K)
    R_i = 8.64 * 10 ** (-4)  # warmteweerstand van de binnenlucht naar de muur (K/W)
    R_e = 1.05 * 10 ** (-2)  # warmteweerstand van de muur naar de buitenlucht (K/W)
    R_vent = 7.98 * 10 ** (-3)  # warmteweerstand van temperatuurverlies door ventilatie (K/W)
    gA = 12  # solar gain factor (m^2)
    frad = 0.3  # distributiefactor van warmtepomp (constante)
    CoP = 4.5  # COP van de warmtepomp (constante) (arbitrair)
    EER = 7.5  # EER van de airco (constante) (arbitrair)

    # aanpassen lengte van lijsten om te matchen met n: 1 waarde per half uur/kwartier
    T_out = extend_list(T_out, N)  # lengte van lijst met buitentemperaturen (K) aanpassen:
    S_rad = extend_list(irradiantie, N)  # lengte van lijst met solar radiation (W) aanpassen

    # vaste variabelen
    m.bkoop = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of we energie kopen in tijdsinterval i
    m.bverkoop = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of we energie verkopen in tijdsinterval i
    m.ebuy = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie we kopen in tijdsinterval i
    m.esell = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie we verkopen in tijdsinterval i
    m.wp = pe.Var(pe.RangeSet(1, N*horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de warmtepomp verbruikt per tijdsinterval i/2
    m.T_in = pe.Var(pe.RangeSet(1, N*(horizon+1)),within=pe.Reals)  # reële variabele die de binnentemperatuur aangeeft per tijdsinterval i/2
    m.T_m = pe.Var(pe.RangeSet(1, N*(horizon+1)),within=pe.Reals)  # reële variabele die de temperatuur van de bouwmassa aangeeft per tijdsinterval i/2
    m.wpsum = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de warmtepomp verbruikt per tijdsinterval i (=som van m.wp over N tijdsintervallen)
    m.airco = pe.Var(pe.RangeSet(1, N*horizon),domain=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de airco verbruikt per tijdsinterval i/2
    m.aircosum = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de airco verbruikt per tijdsinterval i (=som van m.airco over N tijdsintervallen)
    m.wp_aan = pe.Var(pe.RangeSet(1, N*horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de warmtepomp aanstaat in tijdsinterval i/2
    m.airco_aan = pe.Var(pe.RangeSet(1, N*horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de airco aanstaat in tijdsinterval i/2
    m.wm = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de wasmachine aanstaat in tijdsinterval i
    m.auto = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de auto aanstaat in tijdsinterval i
    m.keuken = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de keuken aanstaat in tijdsinterval i
    m.batcharge_aan = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de batterij aan het opladen is in tijdsinterval i
    m.batdischarge_aan = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de batterij aan het ontladen is in tijdsinterval i
    m.batcharge = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de batterij oplaadt in tijdsinterval i
    m.batdischarge = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de batterij ontlaadt in tijdsinterval i
    m.batstate = pe.Var(pe.RangeSet(1, horizon+1),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie er in de batterij zit in tijdsinterval i

    #afhankelijke variabelen
    if wm_aan > 1:
        m.wm_start = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de wasmachine start in tijdsinterval i
    if keuken_aan > 1:
        m.keuken_start = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de keuken start in tijdsinterval i

    # constraints
    '''bkoop bverkoop'''
    m.conb = pe.ConstraintList()  # lijst met constraints: men kan niet tegelijk kopen en verkopen
    for i in range(1, horizon + 1):
        m.conb.add(m.bkoop[i] + m.bverkoop[i] <= 1)

    '''auto'''
    if thuis:
        if auto_aan > 0:
            auto_con_expr = sum(m.auto[i] for i in range(1, horizon + 1)) == auto_aan  # auto staat <auto_aan> tijdsintervallen aan
            m.auto_con = pe.Constraint(expr=auto_con_expr)
        else:
            m.auto_con = pe.ConstraintList()
            for i in range(1, horizon + 1):
                m.auto_con.add(m.auto[i] == 0)
    elif not thuis:
        if auto_aan > 0:
            auto_con_expr = sum(m.auto[i] for i in range(1, horizon + 1)) == auto_aan  # auto staat <auto_aan> tijdsintervallen aan
            m.auto_con = pe.Constraint(expr=auto_con_expr)
            m.auto_thuis_con = pe.ConstraintList()
            if aankomst > 0:
                for i in range(1, aankomst+1):
                    m.auto_thuis_con.add(m.auto[i] == 0)
                for i in range(vertrek+1, horizon + 1):
                    m.auto_thuis_con.add(m.auto[i] == 0)
            elif vertrek > 0:
                for i in range(vertrek+1, horizon + 1):
                    m.auto_thuis_con.add(m.auto[i] == 0)
        else:
            m.auto_con = pe.ConstraintList()
            for i in range(1, horizon + 1):
                m.auto_con.add(m.auto[i] == 0)

    '''wm'''
    if wm_aan == 2:
        wm_con_expr = sum(m.wm[i] for i in range(1, horizon + 1)) == wm_aan  # wasmachine staat <wm_aan> tijdsintervallen aan
        m.wm_con = pe.Constraint(expr=wm_con_expr)
        wm_startcon_expr = sum(m.wm_start[i] for i in range(1, horizon + 1)) == 1  # wasmachine staat 1 tijdsinterval aan het begin aan
        m.wm_startcon2 = pe.Constraint(expr=wm_startcon_expr)
        m.wm_startcon = pe.ConstraintList()  # lijst met constraints: wasmachine staat 1 tijdsinterval aan het begin aan
        m.wm_startcon.add(m.wm[1] == m.wm_start[1])
        for i in range(2, horizon + 1):
            m.wm_startcon.add(m.wm[i] == m.wm_start[i - 1] + m.wm_start[i])
    elif wm_aan == 1:
        wm_con_expr = sum(m.wm[i] for i in range(1, horizon + 1)) == wm_aan  # wasmachine staat <wm_aan> tijdsintervallen aan
        m.wm_con = pe.Constraint(expr=wm_con_expr)
        wm_con_expr2 = m.wm[1] == wm_aan                    # wasmachine staat onmiddellijk aan
        m.wm_con2 = pe.Constraint(expr=wm_con_expr2)
    elif wm_aan == 0:
        m.wm_con = pe.ConstraintList()
        for i in range(1, horizon + 1):
            m.wm_con.add(m.wm[i] == 0)

    '''keuken'''
    if keuken_aan > 0:
        keuken_con_expr = sum(m.keuken[i] for i in range(1, horizon + 1)) == keuken_aan  # wasmachine staat <wm_aan> tijdsintervallen aan
        m.keuken_con = pe.Constraint(expr=keuken_con_expr)
        m.keuken_tijd_con = pe.ConstraintList()
        if keuken_begin > 0:
            for i in range(1, keuken_begin + 1):
                m.keuken_tijd_con.add(m.keuken[i] == 0)
            for i in range(keuken_einde + 1, horizon + 1):
                m.keuken_tijd_con.add(m.keuken[i] == 0)
        elif keuken_einde > 0:
            for i in range(keuken_einde + 1, horizon + 1):
                m.keuken_tijd_con.add(m.keuken[i] == 0)
    elif keuken_aan == 1:
        keuken_con_expr = sum(m.keuken[i] for i in range(1, horizon + 1)) == keuken_aan  # wasmachine staat <wm_aan> tijdsintervallen aan
        m.keuken_con = pe.Constraint(expr=keuken_con_expr)
        keuken_con_expr2 = m.keuken[1] == keuken_aan                    # wasmachine staat onmiddellijk aan
        m.keuken_con2 = pe.Constraint(expr=keuken_con_expr2)
    elif keuken_aan == 0:
        m.keuken_con = pe.ConstraintList()
        for i in range(1, horizon + 1):
            m.keuken_con.add(m.keuken[i] == 0)

    '''energiebalans'''
    m.con_energiebalans = pe.ConstraintList()  # lijst met constraints: energiebalans
    for i in range(1, horizon + 1):
        m.con_energiebalans.add(m.ebuy[i] - m.esell[i] == -zonne_energie[i - 1]/1000 + ewm * m.wm[i] * delta_t + eau * m.auto[i] * delta_t + ekeuken * m.keuken[i] * delta_t + m.wpsum[i]/1000 + m.aircosum[i]/1000 + m.batcharge[i]/1000 - m.batdischarge[i]/1000)

    '''maximum vermogen wp en airco + relatie wp en wp_aan'''
    m.con_wp_grenzen = pe.ConstraintList()  # lijst met constraints: warmtepomp tussen 0 en 4000 W
    for i in range(1, N*horizon + 1):
        m.con_wp_grenzen.add(0 <= m.wp[i])
        m.con_wp_grenzen.add(m.wp[i] <= m.wp_aan[i] * P_max)

    m.con_airco_grenzen = pe.ConstraintList()  # lijst met constraints: airco tussen 0 en 4000 W
    for i in range(1, N*horizon + 1):
        m.con_airco_grenzen.add(0 <= m.airco[i])
        m.con_airco_grenzen.add(m.airco[i] <= m.airco_aan[i] * P_max_airco)

    '''beginvoorwaarden temperatuur'''
    m.con_wp_start = pe.ConstraintList()  # lijst met constraints: warmtepomp beginvoorwaarden moeten gerespecteerd worden
    m.con_wp_start.add(m.T_in[1] == T_in_0)
    m.con_wp_start.add(m.T_m[1] == T_m_0)

    '''warmtebalans'''
    m.con_wp = pe.ConstraintList()  # lijst met constraints: T_in, T-m en wp en airco voldoen aan warmtebenadering in elk tijdsinterval
    for i in range(2, N*(horizon+1)):
        m.con_wp.add(m.T_in[i] == m.T_in[i - 1] + h * (1 / C_i) * ((1 - frad) * (CoP * m.wp[i-1] - EER * m.airco[i-1]) - (m.T_in[i - 1] - T_out[i - 2]) / R_vent - (m.T_in[i - 1] - m.T_m[i - 1]) / R_i))
        m.con_wp.add(m.T_m[i] == m.T_m[i - 1] + h * (1 / C_m) * (frad * (CoP * m.wp[i-1] - EER * m.airco[i-1])+ gA * S_rad[i - 2] - (m.T_m[i - 1] - T_out[i - 2]) / R_e - (m.T_m[i - 1] - m.T_in[i - 1]) / R_i))

    '''temperatuur grenzen'''
    print(T_nothome_max, 'max')
    print(T_nothome_min, 'min')
    print(T_in_0)
    print(T_out)
    m.con_temp_grenzen = pe.ConstraintList()  # lijst met constraints: T_in en T_m tussen 18 en 22 graden
    if thuis:
        for i in range(2, N*(horizon + 1)):
            m.con_temp_grenzen.add(T_in_min <= m.T_in[i])
            m.con_temp_grenzen.add(m.T_in[i] <= T_in_max)
            m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
            m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)
    if not thuis:
        if aankomst > 0:
            '''for i in range(2, aankomst*N):
                m.con_temp_grenzen.add(T_nothome_min <= m.T_in[i])
                m.con_temp_grenzen.add(m.T_in[i] <= T_nothome_max)
                m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
                m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)'''
            for i in range(aankomst*N, N*(vertrek + 1)):
                m.con_temp_grenzen.add(T_in_min <= m.T_in[i])
                m.con_temp_grenzen.add(m.T_in[i] <= T_in_max)
                m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
                m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)
            '''for i in range(N*(vertrek + 1), N*(horizon) + 1):
                m.con_temp_grenzen.add(T_nothome_min <= m.T_in[i])
                m.con_temp_grenzen.add(m.T_in[i] <= T_nothome_max)
                m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
                m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)'''
        elif vertrek > 0:
            for i in range(2, N*(vertrek + 1)):
                m.con_temp_grenzen.add(T_in_min <= m.T_in[i])
                m.con_temp_grenzen.add(m.T_in[i] <= T_in_max)
                m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
                m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)
            '''for i in range(N*(vertrek + 1), N*(horizon) + 1):
                m.con_temp_grenzen.add(T_nothome_min <= m.T_in[i])
                m.con_temp_grenzen.add(m.T_in[i] <= T_nothome_max)
                m.con_temp_grenzen.add(T_m_min <= m.T_m[i])
                m.con_temp_grenzen.add(m.T_m[i] <= T_m_max)'''

    '''wpsum en aircosum'''
    m.con_wpsum = pe.ConstraintList()  # lijst met constraints: wpsum is de som van wp over N tijdsintervallen --> len(wpsum) = horizon ipv N*horizon
    x = 1
    for i in range(1, N*horizon):
        if i % 2 == 0:
            pass
        else:
            m.con_wp.add(m.wpsum[x] == (delta_t/2)*(m.wp[i] + m.wp[i + 1]))
            x += 1
    m.con_aircosum = pe.ConstraintList()  # lijst met constraints: aircosum is de som van airco over N tijdsintervallen --> len(aircosum) = horizon ipv N*horizon
    x = 1
    for i in range(1, N*horizon):
        if i % 2 == 0:
            pass
        else:
            m.con_aircosum.add(m.aircosum[x] == (delta_t/2)*(m.airco[i] + m.airco[i + 1]))
            x += 1

    '''wp en airco niet tegelijk aan in half uur'''
    m.con_wp_airco = pe.ConstraintList()
    for i in range(1, horizon + 1):
        m.con_wp_airco.add(m.wp_aan[i] + m.airco_aan[i] <= 1)

    '''maximum ebuy + relatie ebuy met bkoop'''
    m.con_buymax = pe.ConstraintList()                                              #lijst met constraints: maximum opleggen om energie van het net te kopen
    for i in range(1,horizon+1):
        m.con_buymax.add(m.ebuy[i] <= M*m.bkoop[i])
    m.con_sellmax = pe.ConstraintList()                                             #lijst met constraints: maximum opleggen om energie aan het net te verkopen
    for i in range(1,horizon+1):
        m.con_sellmax.add(m.esell[i] <= M*m.bverkoop[i])

    '''batterij niet tegelijk op en ontladen'''
    m.con_batcharge_simul = pe.ConstraintList()
    for i in range(1, horizon + 1):
        m.con_batcharge_simul.add(m.batcharge_aan[i] + m.batdischarge_aan[i] <= 1)

    '''batterijbalans'''
    m.con_batcharge = pe.ConstraintList()  # lijst met constraints: batterijbalans
    m.con_batcharge.add(m.batstate[1] == batstart)
    for i in range(2, horizon + 2):
        m.con_batcharge.add(m.batstate[i] == m.batstate[i-1] + m.batcharge[i-1] - m.batdischarge[i-1])

    '''min max batterijcapaciteit'''
    m.con_batmax = pe.ConstraintList()  # lijst met constraints: batterijcapaciteit mag niet overschreden worden
    m.con_batmin = pe.ConstraintList()  # lijst met constraints: batterijcapaciteit mag niet negatief worden
    for i in range(1, horizon + 2):
        m.con_batmax.add(sum(m.batstate[i] for i in range(1,horizon+2)) <= batmax)
        m.con_batmin.add(sum(m.batstate[i] for i in range(1,horizon+2)) >= batmin)

    '''batterij opladen en ontladen'''
    m.con_batcharge_grenzen = pe.ConstraintList()  # lijst met constraints: batterij opladen en ontladen
    for i in range(1, horizon + 1):
        m.con_batcharge_grenzen.add(0 <= m.batcharge[i])
        m.con_batcharge_grenzen.add(m.batcharge[i] <= m.batcharge_aan[i] * batmaxcharge)
        m.con_batcharge_grenzen.add(0 <= m.batdischarge[i])
        m.con_batcharge_grenzen.add(m.batdischarge[i] <= m.batdischarge_aan[i] * batmaxdischarge)

    # objectieffunctie
    kostprijs_energie = sum(netstroom[i - 1] * (m.ebuy[i] - 1 / 3 * m.esell[i]) for i in range(1,horizon + 1))  # hoe weten we dat verkoopprijs altijd exact 1/3 is van aankoopprijs?
    m.obj = pe.Objective(expr=kostprijs_energie, sense=pe.minimize)

    #los het probleem op
    '''solver = po.SolverFactory('glpk')
    result = solver.solve(m)'''

    solver = po.SolverFactory('gurobi_direct')
    result = solver.solve(m)

    #haal data uit resultaat en stuur terug
    resultaat = {}
    resultaat['result'] = result
    resultaat['wp'] = [pe.value(m.wp[i]) for i in range(1, N*horizon + 1)] #lijst met vermogen van de warmtepomp (W) per half uur
    resultaat['wpsum'] = [pe.value(m.wpsum[i]) for i in range(1, horizon + 1)] #lijst met vermogen van de warmtepomp (W) per uur
    resultaat['T_in'] = [round(pe.value(m.T_in[i])-273.15,2) for i in range(1, N*horizon + 1)] #lijst met binnentemperaturen (Celsius) per half uur
    resultaat['T_m'] = [round(pe.value(m.T_m[i])-273.15,2) for i in range(1, N*horizon + 1)] #lijst met temperaturen van de bouwmassa (Celsius) per half uur
    resultaat['auto'] = [pe.value(m.auto[i]) for i in range(1, horizon + 1)] #lijst met auto aan/uit (0/1) per uur
    resultaat['wm'] = [pe.value(m.wm[i]) for i in range(1, horizon + 1)] #lijst met wasmachine aan/uit (0/1) per uur
    resultaat['ebuy'] = [pe.value(m.ebuy[i]) for i in range(1, horizon + 1)] #lijst met energie die we kopen (kWh) per uur
    resultaat['esell'] = [pe.value(m.esell[i]) for i in range(1, horizon + 1)] #lijst met energie die we verkopen (kWh) per uur
    resultaat['kostprijs_energie'] = pe.value(kostprijs_energie) #kostprijs van de energie (euro)
    resultaat['airco'] = [pe.value(m.airco[i]) for i in range(1, N*horizon + 1)]
    resultaat['aircosum'] = [pe.value(m.aircosum[i]) for i in range(1, horizon + 1)]
    resultaat['keuken'] = [pe.value(m.keuken[i]) for i in range(1, horizon + 1)]
    resultaat['batcharge'] = [pe.value(m.batcharge[i]) for i in range(1, horizon + 1)]
    resultaat['batdischarge'] = [pe.value(m.batdischarge[i]) for i in range(1, horizon + 1)]
    resultaat['batstate'] = [pe.value(m.batstate[i]) for i in range(1, horizon + 2)]

    return resultaat