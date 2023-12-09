#Simulatie warmte model
def simuleer_warmte_model(delta_T, P_in,P_airco, T_out, S_rad, T_in_0, T_m_0):       # functie om het warmtemodel te simuleren
                                                                    # input:
                                                                    # vermogen (W) van de warmtepomp
                                                                    # buitentemperatuur (K)
                                                                    # solar radiation (W)
                                                                    # vorige begintemperatuur van de binnentemperatuur (Celsius) uit simulatie model
                                                                    # vorige begintemperatuur van de bouwmassa (Celsius) uit simulatie model
                                                                    # output:
                                                                    # lijst met binnentemperaturen (Celsius)
                                                                    # lijst met temperaturen van de bouwmassa (Celsius)

    #importeren van modules
    import numpy as np
    from scipy.integrate import solve_ivp

    # Define parameters
    t0 = float(0)                      # begintijdstip
    t_end = float(delta_T * 60 * 60)         # aantal seconden in een uur

    # Parameters
    C_i = 2.44*10**6                    #warmtecapaciteit van de binnenlucht (J/K)
    C_m = 9.40*10**7                    #warmtecapaciteit van de bouwmassa (J/K)
    R_i = 8.64*10**(-4)                 #warmteweerstand van de binnenlucht naar de muur (K/W)
    R_e = 1.05*10**(-2)                 #warmteweerstand van de muur naar de buitenlucht (K/W)
    R_vent = 7.98*10**(-3)              #warmteweerstand van temperatuurverlies door ventilatie (K/W)
    gA = 12                             #solar gain factor (m^2)
    frad = 0.3                          #distributiefactor van warmtepomp (constante)
    CoP = 4.5                             #COP van de warmtepomp (constante) (arbitrair)
    EER = 7.5                             #EER van de airco (constante) (arbitrair)

    #Expleciete Runge-Kutta methode van orde 5(4)
    def equations(t, state, P_in_eq, P_airco_eq, T_out_eq, S_rad_eq):
        T_in_eq, T_m_eq = state
        dT_in = (1/C_i)*((1-frad)*(CoP*P_in_eq - EER*P_airco_eq) - (T_in_eq-T_out_eq)/R_vent - (T_in_eq-T_m_eq)/R_i)
        dT_m = (1/C_m)*(frad*(P_in_eq*CoP-EER*P_airco_eq)+gA*S_rad_eq - (T_m_eq-T_out_eq)/R_e - (T_m_eq-T_in_eq)/R_i)
        return [dT_in, dT_m]

    y0 = [T_in_0, T_m_0]        # Initial state of the system
    p = (P_in, P_airco, T_out, S_rad)    # Parameters to be passed to the function
    t_span = (t0, t_end)
    teval = np.arange(delta_T*60*60)
    oplossing = solve_ivp(equations, t_span, y0,t_eval=teval , args=p)

    #data terugsturen naar controller.py
    T_in = oplossing.y[0, :].tolist()
    T_m = oplossing.y[1, :].tolist()
    T_time = oplossing.t.tolist()

    return T_in, T_m, T_time                                 #terugsturen van de lijsten met binnentemperatuur en temperatuur van de bouwmassa                                #terugsturen van de lijsten met binnentemperatuur en temperatuur van de bouwmassa