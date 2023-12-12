from GetfromDB import getFromDB
from GetfromDB import getTempFromDB
from Controller import controller
testdag = "2022-10-30"
temp_out = getTempFromDB(testdag)[0]
temp_out = [30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
radiation = getTempFromDB(testdag)[1]
price = getFromDB(testdag)
ewm = 2.5  # verbruik wasmachine (kW = kWh/h)
eau = 7.4  # vermogen laadpaal (kW)
ekeuken = 2.11  # vermogen keuken (kW)
[auto_final, wm_final, keuken_final, ebuy_final, esell_final, ebuy_final_sum, esell_final_sum, wpsum_final,
        aircosum_final, wp_actions, airco_actions, T_in_final, T_m_final, zonne_energie, zonne_energie_sum,
        T_in_simulatie, T_m_simulatie, T_time_simulatie, opslag_resultaat, kostprijs_energie, batstate_final,
        batcharge_final, batdischarge_final] = controller(temp_out, price, radiation, True,True, True, True, True, True)
wm_verbruik = sum(wm_final) * ewm
auto_verbruik = sum(auto_final) * eau
keuken_verbruik = sum(keuken_final) * ekeuken
'''wp_verbruik = sum(wpsum_final)/1000
airco_verbruik = sum(aircosum_final)/1000'''
wp_verbruik = sum(wp_actions) / 2000
airco_verbruik = sum(airco_actions) / 2000
print(f"wp_verbruik: {wp_verbruik}")
print(f"airco_verbruik: {airco_verbruik}")
tot_verbruik = wm_verbruik + auto_verbruik + keuken_verbruik + wp_verbruik + airco_verbruik
print(f"tot_verbruik: {tot_verbruik}")

