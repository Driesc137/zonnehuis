#Simulatie warmte model
import numpy as np
import matplotlib.pyplot as plt
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
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp

    #Celsius to Kelvin
    T_out = T_out + 273.15              #omzetten van buitentemperatuur van Celsius naar Kelvin
    T_in_0 = T_in_0 + 273.15            #omzetten van begintemperatuur van de binnentemperatuur van Celsius naar Kelvin
    T_m_0 = T_m_0 + 273.15              #omzetten van begintemperatuur van de bouwmassa van Celsius naar Kelvin

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
    teval = np.arange(60*60)
    oplossing = solve_ivp(equations, t_span, y0,t_eval=teval , args=p)

    '''#plot resultaten
    t = np.linspace(t0,t_end, n)                            #tijd wordt opgedeeld in n gelijke stukken van lengte h
    plt.figure("Temperatuur")                               #maak een figuur met naam "Temperatuur"
    plt.plot(t/(60*60),T_in-273.15,'b', label='T_in')       #plot binnentemperatuur (Celsius) i.f.v. tijd (uur)
    plt.plot(t/(60*60),T_m-273.15,'g', label='T_m')         #plot temperatuur (Celsius) van de bouwmassa i.f.v. tijd (uur)
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Temperatuur (°C)')                          #label y-as
    plt.title('Binnen- en buitentemperatuur zonnehuis')     #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.legend(loc='upper right')                           #legende rechtsboven
    plt.figure("Warmtepomp")                                #maak een figuur met naam "Warmtepomp"
    plt.plot(t/(60*60),P_in)                                #plot vermogen (W) van de warmtepomp i.f.v. tijd (uur)
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Vermogen (W)')                              #label y-as
    plt.title('Vermogen van de warmtepomp')                 #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.show()                                              #toon de grafieken
    Handig?'''

    #data terugsturen naar controller.py
    T_in = oplossing.y[0, :]
    T_m = oplossing.y[1, :]
    T_in_time = oplossing.t
    T_m_time = oplossing.t
    T_in = [round(i-273.15,4) for i in T_in]
    T_m = [round(i-273.15,4) for i in T_m]
    T_in_time = [round(i/(60*60),4) for i in T_in_time]
    T_m_time = [round(i/(60*60),4) for i in T_m_time]
    return T_in, T_m, T_in_time, T_m_time, oplossing                                      #terugsturen van de lijsten met binnentemperatuur en temperatuur van de bouwmassa

#test
#[T_in, T_m, T_in_time, T_m_time] = simuleer_warmte_model(0, 10, 0, 20, 20)
#create a loop that runs the simulation for 24 hours and uses the last element of T_in and T_m as the new T_in_0 and T_m_0
#make sure all temperatures are stored in one list, so it can be plotted
'''for i in range(11):
    [T_in_temp, T_m_temp, T_in_temp_t, T_m_temp_t] = simuleer_warmte_model(0, 10, 20, T_in[-1], T_m[-1])
    T_in = np.concatenate((T_in, T_in_temp))
    T_m = np.concatenate((T_m, T_m_temp))
    T_in_temp_t = [(i+j) for j in T_m_temp_t]
    T_m_temp_t = [(i+j) for j in T_m_temp_t]
    T_in_time = np.concatenate((T_in_time, T_in_temp_t))
    T_m_time = np.concatenate((T_m_time, T_m_temp_t))
for i in range(6):
    [T_in_temp, T_m_temp, T_in_temp_t, T_m_temp_t] = simuleer_warmte_model(2000, 15, 100, T_in[-1], T_m[-1])
    T_in = np.concatenate((T_in, T_in_temp))
    T_m = np.concatenate((T_m, T_m_temp))
    T_in_temp_t = [((11+i)+j) for j in T_m_temp_t]
    T_m_temp_t = [((11+i)+j) for j in T_m_temp_t]
    T_in_time = np.concatenate((T_in_time, T_in_temp_t))
    T_m_time = np.concatenate((T_m_time, T_m_temp_t))
for i in range(6):
    [T_in_temp, T_m_temp, T_in_temp_t, T_m_temp_t] = simuleer_warmte_model(0, 15, 0, T_in[-1], T_m[-1])
    T_in = np.concatenate((T_in, T_in_temp))
    T_m = np.concatenate((T_m, T_m_temp))
    T_in_temp_t = [((17+i)+j) for j in T_m_temp_t]
    T_m_temp_t = [((17+i)+j) for j in T_m_temp_t]
    T_in_time = np.concatenate((T_in_time, T_in_temp_t))
    T_m_time = np.concatenate((T_m_time, T_m_temp_t))'''

'''print(T_in)
print(T_m)
print(T_in_time)
print(T_m_time)
print(len(T_in))
print(len(T_in_time))
t = np.linspace(0,len(T_in), len(T_in))                            #tijd wordt opgedeeld in n gelijke stukken van lengte h
plt.figure("Temperatuur")                               #maak een figuur met naam "Temperatuur"
plt.plot(T_in_time,T_in,'b', label='T_in')       #plot binnentemperatuur (Celsius) i.f.v. tijd (uur)
plt.plot(T_m_time,T_m,'g', label='T_m')         #plot temperatuur (Celsius) van de bouwmassa i.f.v. tijd (uur)
plt.xlabel('Tijd (uur)')                                #label x-as
plt.ylabel('Temperatuur (°C)')                          #label y-as
plt.title('Binnen- en buitentemperatuur zonnehuis')     #titel van de grafiek
plt.grid()                                              #raster op de grafiek
plt.legend(loc='upper right')                           #legende rechtsboven
plt.show()'''