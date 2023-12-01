import pyomo.environ as pe
import pyomo.opt as po

def optimaliseer(horizon, irradiantie, netstroom, zp_opp, eff, ewm, eau, delta_t, M, wm_aan, auto_aan, T_in_0, T_m_0, T_out, P_max, T_in_min, T_in_max, T_m_min, T_m_max):

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
    CoP = 3  # COP van de warmtepomp (constante) (arbitrair)
    K = 273.15  # omrekeningsfactor van Celsius naar Kelvin

    # Celsius to Kelvin
    T_out = [i + K for i in T_out]  # omzetten van lijst met temperaturen van Celsius naar Kelvin
    T_in_0 = T_in_0 + K  # omzetten van begintemperatuur van de binnentemperatuur van Celsius naar Kelvin
    T_m_0 = T_m_0 + K  # omzetten van begintemperatuur van de bouwmassa van Celsius naar Kelvin

    # aanpassen lengte van lijsten om te matchen met n: 1 waarde per half uur/kwartier
    T_out = extend_list(T_out, N)  # lengte van lijst met buitentemperaturen (K) aanpassen:
    S_rad = extend_list(irradiantie, N)  # lengte van lijst met solar radiation (kW) aanpassen

    # variabelen
    m.bkoop = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of we energie kopen in tijdsinterval i
    m.bverkoop = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of we energie verkopen in tijdsinterval i
    m.wm = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de wasmachine aanstaat in tijdsinterval i
    m.auto = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de auto aanstaat in tijdsinterval i
    m.ebuy = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie we kopen in tijdsinterval i
    m.esell = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie we verkopen in tijdsinterval i
    m.wm_start = pe.Var(pe.RangeSet(1, horizon),domain=pe.Binary)  # binaire variabele die aangeeft of de wasmachine start in tijdsinterval i
    m.wp = pe.Var(pe.RangeSet(1, N*horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de warmtepomp verbruikt per tijdsinterval i/2
    m.T_in = pe.Var(pe.RangeSet(1, N*horizon),within=pe.NonNegativeReals)  # reële variabele die de binnentemperatuur aangeeft per tijdsinterval i/2
    m.T_m = pe.Var(pe.RangeSet(1, N*horizon),within=pe.NonNegativeReals)  # reële variabele die de temperatuur van de bouwmassa aangeeft per tijdsinterval i/2
    m.wpsum = pe.Var(pe.RangeSet(1, horizon),within=pe.NonNegativeReals)  # reële variabele die aangeeft hoeveel energie de warmtepomp verbruikt per tijdsinterval i (=som van m.wp over N tijdsintervallen)

    # constraints
    m.conb = pe.ConstraintList()  # lijst met constraints: men kan niet tegelijk kopen en verkopen
    for i in range(1, horizon + 1):
        m.conb.add(m.bkoop[i] + m.bverkoop[i] <= 1)

    auto_con_expr = sum(m.auto[i] for i in range(1, horizon + 1)) == auto_aan  # auto staat <auto_aan> tijdsintervallen aan
    m.auto_con = pe.Constraint(expr=auto_con_expr)


    if wm_aan == 2:
        wm_con_expr = sum(m.wm[i] for i in range(1, horizon + 1)) == wm_aan  # wasmachine staat <wm_aan> tijdsintervallen aan
        m.wm_con = pe.Constraint(expr=wm_con_expr)
        wm_startcon_expr = sum(m.wm_start[i] for i in range(1, horizon + 1)) == 1  # wasmachine staat 1 tijdsinterval aan het begin aan
        m.wm_startcon = pe.ConstraintList()  # lijst met constraints: wasmachine staat 1 tijdsinterval aan het begin aan
        m.wm_startcon.add(m.wm[1] == m.wm_start[1])  # waarvoor dient deze code?
        for k in range(2, horizon + 1):  # waarvoor dient deze code?
            m.wm_startcon.add(m.wm[k] == m.wm_start[k - 1] + m.wm_start[k])  # waarvoor dient deze code?
    if wm_aan == 1:
        wm_con_expr = m.wm[1] == wm_aan                    # wasmachine staat onmiddellijk aan
        m.wm_con = pe.Constraint(expr=wm_con_expr)

    m.con_energiebalans = pe.ConstraintList()  # lijst met constraints: energiebalans
    for i in range(1, horizon + 1):
        m.con_energiebalans.add(m.ebuy[i] - m.esell[i] == -irradiantie[i - 1] * zp_opp * eff + ewm * m.wm[i] * delta_t + eau * m.auto[i] + m.wpsum[i]/1000)


    m.con_wp_grenzen = pe.ConstraintList()  # lijst met constraints: warmtepomp tussen 0 en 4000 W
    for i in range(1, horizon + 1):
        m.con_wp_grenzen.add(0 <= m.wpsum[i])
        m.con_wp_grenzen.add(m.wpsum[i] <= P_max)

    m.con_wp_start = pe.ConstraintList()  # lijst met constraints: warmtepomp beginvoorwaarden moeten gerespecteerd worden
    m.con_wp_start.add(m.T_in[1] == T_in_0)
    m.con_wp_start.add(m.T_m[1] == T_m_0)

    m.con_wp = pe.ConstraintList()  # lijst met constraints: T_in, T-m en wp voldoen aan warmtebenadering in elk tijdsinterval
    for i in range(2, N*horizon+1):
        m.con_wp.add(m.T_in[i] == m.T_in[i - 1] + h * (1 / C_i) * ((1 - frad) * CoP * m.wp[i-1] - (m.T_in[i - 1] - T_out[i - 2]) / R_vent - (m.T_in[i - 1] - m.T_m[i - 1]) / R_i))
        m.con_wp.add(m.T_m[i] == m.T_m[i - 1] + h * (1 / C_m) * (frad * CoP * m.wp[i-1] + gA * S_rad[i - 2]*1000 - (m.T_m[i - 1] - T_out[i - 2]) / R_e - (m.T_m[i - 1] - m.T_in[i - 1]) / R_i))

    m.con_temp_grenzen = pe.ConstraintList()  # lijst met constraints: T_in en T_m tussen 18 en 22 graden
    for i in range(2, N*horizon + 1):
        m.con_temp_grenzen.add(T_in_min+K <= m.T_in[i])
        m.con_temp_grenzen.add(m.T_in[i] <= T_in_max+K)
        m.con_temp_grenzen.add(T_m_min+K <= m.T_m[i])
        m.con_temp_grenzen.add(m.T_m[i] <= T_m_max+K)

    m.con_wpsum = pe.ConstraintList()  # lijst met constraints: wpsum is de som van wp over N tijdsintervallen --> len(wpsum) = horizon ipv N*horizon
    x = 1
    for i in range(1, N*horizon):
        if i % 2 == 0:
            pass
        else:
            m.con_wp.add(m.wpsum[x] == m.wp[i] + m.wp[i + 1])
            x += 1

    '''waarom?'''
    '''m.con_buymax = pe.ConstraintList()                                              #lijst met constraints: maximum opleggen om energie van het net te kopen
    for i in range(1,horizon+1):
        m.con_buymax.add(m.ebuy[i] <= M*m.bkoop[i])'''
    '''waarom?'''
    '''m.con_sellmax = pe.ConstraintList()                                             #lijst met constraints: maximum opleggen om energie aan het net te verkopen
    for i in range(1,horizon+1):
        m.con_sellmax.add(m.esell[i] <= M*m.bverkoop[i])'''

    # objectieffunctie
    kostprijs_energie = sum(netstroom[i - 1] / 1000 * (m.ebuy[i] - 1 / 3 * m.esell[i]) for i in range(1,horizon + 1))  # hoe weten we dat verkoopprijs altijd exact 1/3 is van aankoopprijs?
    m.obj = pe.Objective(expr=kostprijs_energie, sense=pe.minimize)

    #los het probleem op
    solver = po.SolverFactory('glpk')
    result = solver.solve(m)

    #haal data uit resultaat en stuur terug
    resultaat = {}
    x= 0
    '''for i in range(1, N * horizon + 1):
        #print(pe.value(m.wp[i]))
        x+=1
    #print("wpsum values per uur:")
    for i in range(1, horizon + 1):
        #print(pe.value(m.wpsum[i]))
    #print("T_in per half uur")
        l = 0
    for i in range(1, N * horizon + 1):
        #print(pe.value(m.T_in[i])-K)
        l+=1
    for i in range(1, N * horizon + 1):
        #print(pe.value(m.T_m[i])-K) '''
    resultaat['result'] = result
    resultaat['wp'] = [pe.value(m.wp[i]) for i in range(1, N*horizon + 1)] #lijst met vermogen van de warmtepomp (W) per half uur
    resultaat['wpsum'] = [pe.value(m.wpsum[i]) for i in range(1, horizon + 1)] #lijst met vermogen van de warmtepomp (W) per uur
    resultaat['T_in'] = [pe.value(m.T_in[i])-K for i in range(1, N*horizon + 1)] #lijst met binnentemperaturen (Celsius) per half uur
    resultaat['T_m'] = [pe.value(m.T_m[i])-K for i in range(1, N*horizon + 1)] #lijst met temperaturen van de bouwmassa (Celsius) per half uur
    resultaat['auto'] = [pe.value(m.auto[i]) for i in range(1, horizon + 1)] #lijst met auto aan/uit (0/1) per uur
    resultaat['wm'] = [pe.value(m.wm[i]) for i in range(1, horizon + 1)] #lijst met wasmachine aan/uit (0/1) per uur
    resultaat['ebuy'] = [pe.value(m.ebuy[i]) for i in range(1, horizon + 1)] #lijst met energie die we kopen (kWh) per uur
    resultaat['esell'] = [pe.value(m.esell[i]) for i in range(1, horizon + 1)] #lijst met energie die we verkopen (kWh) per uur
    resultaat['kostprijs_energie'] = pe.value(kostprijs_energie) #kostprijs van de energie (euro)
    if wm_aan == 2:
        resultaat['wm_start'] = [pe.value(m.wm_start[i]) for i in range(1, horizon + 1)] 
    resultaat['bkoop'] = [pe.value(m.bkoop[i]) for i in range(1, horizon + 1)] 
    resultaat['bverkoop'] = [pe.value(m.bverkoop[i]) for i in range(1, horizon + 1)]
    resultaat['status'] = result.solver.status
    resultaat['termination_condition'] = result.solver.termination_condition

    return resultaat