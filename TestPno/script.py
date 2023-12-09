from flask import Flask, render_template, request, jsonify
from TEST_controller.GetfromDB import getFromDB,getTempFromDB
from TEST_controller.Controller import controller
from zonderoptimalisatie import custom_dag
import random
from datetime import datetime, timedelta
def filter_indices(input_list):
    # Maak een nieuwe lijst met elementen waarvan de index een veelvoud is van 60
    filtered_list = [input_list[i] for i in range(0, len(input_list), 15)]
    return filtered_list
def check_float(array):
    for element in array:
        if not isinstance(element, (float, int)):
            return False
    return True

def recursive_float_conversion(element):
    if isinstance(element, list):
        return [recursive_float_conversion(item) for item in element]
    else:
        return float(element)


def get_next_day(input_date):
    # Converteer de invoerdatumstring naar een datetime-object
    date_object = datetime.strptime(input_date, '%Y-%m-%d')

    # Voeg één dag toe aan de datum
    next_day = date_object + timedelta(days=1)

    # Converteer de resulterende datum naar een string in hetzelfde formaat
    next_day_str = next_day.strftime('%Y-%m-%d')

    return next_day_str

app = Flask(__name__)

def get_keuken():
    keuken = 122.69
    return keuken
# Simuleer het verkrijgen van gegevens vanuit Python
def get_data(date):
    # Voer je Python-code uit om de gegevens op te halen
    data = getFromDB(date)
    [temp,rad] = getTempFromDB(date)
    opgewekte_energie = []
    for i in range(0,len(rad)):
        a = rad[i]*0.2*22.4
    #[auto, wasmachine,gekochte_energie,verkochte_energie,verbruikwarmtepomp,binnentemp] = controller(temp,data,rad,True,auto_knop)
    #print(str(date))
    #
    data = [10.5, 20, 15, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
    #print(data)
    print("Button 1:" + str(button1))
    print("Button 2:" + str(button2))
    print("Button 3:" + str(button3))
    print("Button 4:" + str(button4))
    print("Button 5:" + str(button5))
    print("Prijs 1:" + (str(prijs1)))
    print("Template:" + (str(template)))
    return data

@app.route('/get-data', methods=['GET'])
def get_data_route():
    print('peer')
    print(auto)
    print(totaal_verbruikte_energie_auto)
    print('appel')
    return jsonify([opgewekte_energie,verbruikte_energie,totaal_verbruikte_energie_wasmachine,totaal_verbruikte_energie_auto,totaal_verbruikte_energie_warmtepomp,auto,wasmachine,verbruikwarmtepomp,binnentemp,temp,totaal_verbruikte_energie_keuken,keuken_verbruik,verbruikeAirco,total_verbruikeAirco,filter_indices(gekkeTemp),batpercentage,rad,dataprijs])
    #selected_date = request.args.get('selectedDate')
    #print(str(selected_date))
    

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
       
        return render_template('index.html', selectedDate=selected_date)
    return render_template('indextest.html')

@app.route('/run-python', methods=['GET', 'POST'])
def run_python_code():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
        # Voer hier je Python-code uit en retourneer het resultaat
        #print(str(selected_date))
        global button1 #datum
        global button2
        global button3
        global button4
        global button5
        global template #templates
        global prijs1
        global auto_knop
        global wasmachine_knop
        global warm
        global gematigd
        global koud
        global hoge_elec
        global lage_elec
        global fluc_elec
        global customrad5
        global rad
        #global wasSlider
        global keuken
        global result
        global temp
        global keuken_boolean
        #wasSlider = request.form.get('sliderWas')
        thuis_zijn = request.form.get('verwarming') == 'true'
        keuken_boolean = request.form.get('keuken') == 'true'
        template = request.form['template'] #templates
        button1 = request.form.get('button1') == 'true' #datum
        button2 = request.form.get('button2') == 'true'
        button3 = request.form.get('button3') == 'true'
        button4 = request.form.get('button4') == 'true'
        button5 = request.form.get('button5') == 'true'
        button6 = request.form.get('button6') == 'true'

        prijs0 = request.form.get('price0')
        prijs1 = request.form.get('price1')
        prijs2 = request.form.get('price2')
        prijs3 = request.form.get('price3')
        prijs4 = request.form.get('price4')
        prijs5 = request.form.get('price5')
        prijs6 = request.form.get('price6')
        prijs7 = request.form.get('price7')
        prijs8 = request.form.get('price8')
        prijs9 = request.form.get('price9')
        prijs10 = request.form.get('price10')
        prijs11 = request.form.get('price11')
        prijs12 = request.form.get('price12')
        prijs13 = request.form.get('price13')
        prijs14 = request.form.get('price14')
        prijs15 = request.form.get('price15')
        prijs16 = request.form.get('price16')
        prijs17 = request.form.get('price17')
        prijs18 = request.form.get('price18')
        prijs19 = request.form.get('price19')
        prijs20 = request.form.get('price20')
        prijs21 = request.form.get('price21')
        prijs22 = request.form.get('price22')
        prijs23 = request.form.get('price23')
        customTemp0 = request.form.get('hour0')
        customTemp1 = request.form.get('hour1')
        customTemp2 = request.form.get('hour2')
        customTemp3 = request.form.get('hour3')
        customTemp4 = request.form.get('hour4')
        customTemp5 = request.form.get('hour5')
        customTemp6 = request.form.get('hour6')
        customTemp7 = request.form.get('hour7')
        customTemp8 = request.form.get('hour8')
        customTemp9 = request.form.get('hour9')
        customTemp10 = request.form.get('hour10')
        customTemp11 = request.form.get('hour11')
        customTemp12 = request.form.get('hour12')
        customTemp13 = request.form.get('hour13')
        customTemp14 = request.form.get('hour14')
        customTemp15 = request.form.get('hour15')
        customTemp16 = request.form.get('hour16')
        customTemp17 = request.form.get('hour17')
        customTemp18 = request.form.get('hour18')
        customTemp19 = request.form.get('hour19')
        customTemp20 = request.form.get('hour20')
        customTemp21 = request.form.get('hour21')
        customTemp22 = request.form.get('hour22')
        customTemp23 = request.form.get('hour23')
        customrad0 = request.form.get('solar0')
        customrad1 = request.form.get('solar1')
        customrad2 = request.form.get('solar2')
        customrad3 = request.form.get('solar3')
        customrad4 = request.form.get('solar4')
        customrad5 = request.form.get('solar5')
        customrad6 = request.form.get('solar6')
        customrad7 = request.form.get('solar7')
        customrad8 = request.form.get('solar8')
        customrad9 = request.form.get('solar9')
        customrad10 = request.form.get('solar10')
        customrad11 = request.form.get('solar11')
        customrad12 = request.form.get('solar12')
        customrad13 = request.form.get('solar13')
        customrad14 = request.form.get('solar14')
        customrad15 = request.form.get('solar15')
        customrad16 = request.form.get('solar16')
        customrad17 = request.form.get('solar17')
        customrad18 = request.form.get('solar18')
        customrad19 = request.form.get('solar19')
        customrad20 = request.form.get('solar20')
        customrad21 = request.form.get('solar21')
        customrad22 = request.form.get('solar22')
        customrad23 = request.form.get('solar23')

        keuken = get_keuken()
        auto_knop = request.form.get('auto') == 'true'
        wasmachine_knop = request.form.get('wasmachine') == 'true'
        airco_knop = request.form.get('airco') == 'true'
        batterij_knop = request.form.get('batterij') == 'true'
        warm = request.form.get('warm') == 'true'
        gematigd = request.form.get('gematigd') == 'true'
        koud = request.form.get('koud') == 'true'
        hoge_elec = request.form.get('hoge_elec') == 'true'
        lage_elec = request.form.get('lage_elec') == 'true'
        fluc_elec = request.form.get('fluc_elec') == 'true'
        global wasmachine
        global auto
        global gekochte_energie
        global verkochte_energie
        global verbruikwarmtepomp
        global binnentemp
        global opgewekte_energie
        global verbruikte_energie
        global totaal_verbruikte_energie
        global totaal_verbruikte_energie_auto
        global totaal_verbruikte_energie_wasmachine
        global totaal_verbruikte_energie_warmtepomp
        global totaal_verbruikte_energie_airco
        global totaal_verbruikte_energie_keuken
        global totale_prijs_energie
        global gemiddeldeTemperatuur
        global gemiddeldeBinnenTemperatuur
        global keuken_verbruik
        global verbruikeAirco
        global testHALLO
        global gekkeTemp
        global gemiddeldeElektriciteitsprijs
        opgewekte_energie = []
        global totaal_opgewekte_energie
        global dataprijs
        global kost_zonderOP
        global kostverschil
        totaal_opgewekte_energie = 0
        if button6 == True:
            dataprijs = [float(prijs12), float(prijs13), float(prijs14), float(prijs15), float(prijs16), float(prijs17), float(prijs18), float(prijs19), float(prijs20), float(prijs21), float(prijs22), float(prijs23), float(prijs0), float(prijs1), float(prijs2), float(prijs3), float(prijs4), float(prijs5), float(prijs6), float(prijs7), float(prijs8), float(prijs9), float(prijs10), float(prijs11)]
            temp = [float(customTemp12), float(customTemp13), float(customTemp14), float(customTemp15), float(customTemp16), float(customTemp17), float(customTemp18), float(customTemp19), float(customTemp20), float(customTemp21), float(customTemp22), float(customTemp23), float(customTemp0), float(customTemp1), float(customTemp2), float(customTemp3), float(customTemp4), float(customTemp5), float(customTemp6), float(customTemp7), float(customTemp8), float(customTemp9), float(customTemp10), float(customTemp11)]
            rad = [float(customrad12), float(customrad13), float(customrad14), float(customrad15), float(customrad16), float(customrad17), float(customrad18), float(customrad19), float(customrad20), float(customrad21), float(customrad22), float(customrad23), float(customrad0), float(customrad1), float(customrad2), float(customrad3), float(customrad4), float(customrad5), float(customrad6), float(customrad7), float(customrad8), float(customrad9), float(customrad10), float(customrad11)]
        if template == 'true':
            if lage_elec == True:
                data0 = getFromDB('2022-05-26')
                next_day = get_next_day('2022-05-26')
                data2 = getFromDB(next_day)
                dataprijs = data0[-18:] + data2[:6]   
            if fluc_elec == True:
                data0 = getFromDB('2022-04-22')
                next_day = get_next_day('2022-04-22')
                data2 = getFromDB(next_day)
                dataprijs = data0[-18:] + data2[:6]
            if hoge_elec == True:
                data0 = getFromDB('2022-08-29')
                next_day = get_next_day('2022-08-29')
                data2 = getFromDB(next_day)
                dataprijs = data0[-18:] + data2[:6]
            if koud == True:
                [temp0,rad0] = getTempFromDB('2022-01-05')
                next_day = get_next_day('2022-01-05')
                [temp2,radM] = getTempFromDB(next_day)
                temp = temp0[-18:] + temp2[:6]

            if gematigd == True:
                [temp0,rad0] = getTempFromDB('2022-05-12')
                next_day = get_next_day('2022-05-12')
                [temp2,radM] = getTempFromDB(next_day)
                temp = temp0[-18:] + temp2[:6]
            if warm == True:
                [temp0,rad0] = getTempFromDB('2022-06-18')
                next_day = get_next_day('2022-06-18')
                [temp2,radM] = getTempFromDB(next_day)
                temp = temp0[-18:] + temp2[:6]
                for i in range(len(temp)):
                    temp[i] = temp[i] +10
            if button5 == True:
                rad1 = [random.choice([0, 0.1, 0.2,0.3,0.4,0.5]) for _ in range(17)]
                rad2 = [0,0,0,0,0,0,0]
                rad = rad1 + rad2 
            if button4 == True:
                rad1 = [random.choice([1.5, 1, 1.1,1.4]) for _ in range(17)]
                rad2 = [0,0,0,0,0,0,0]
                rad3 = [random.choice([1.5, 1, 1.1,1.4]) for _ in range(5)]
                rad = rad1 + rad2 
            if button3 == True:
                rad1 = [random.choice([3.5, 4, 3.7,3.2,4.1]) for _ in range(17)]
                rad2 = [0,0,0,0,0,0,0]
                rad3 = [random.choice([3.5, 4, 3.7,3.2,4.1]) for _ in range(5)]
                rad = rad1 + rad2 
        if button1 == True:
            data0 = getFromDB(selected_date)
            [temp0,rad0] = getTempFromDB(selected_date)
            next_day = get_next_day(selected_date)
            data2 = getFromDB(next_day)
            [temp2,radM] = getTempFromDB(next_day)
            dataprijs = data0[-18:] + data2[:6]
            temp = temp0[-18:] + temp2[:6]
            rad = rad0[-18:] + radM[:6]
            
            testHALLO = 'hallo'
        [auto, wasmachine,keuken_verbruik,gekochte_energie,verkochte_energie,suM1, suM2,sum3,sum4, verbruikwarmtepomp,verbruikeAirco,binnentemp,buitemuur,zonne_energie, zonne_energie_sum,gekkeTemp,t1,t2,opslag,kostprijs_en,bat1,bat2,bat3] = controller(temp,dataprijs,rad,wasmachine_knop,auto_knop,keuken_boolean,airco_knop,batterij_knop,thuis_zijn)
        result = "Dit is de uitvoer van de Python-code."
        global batpercentage
        global total_verbruikeAirco
        batpercentage = bat1
        batpercentage = batpercentage[0:24]
        total_verbruikeAirco = sum(verbruikeAirco)/1000
        for i in range(0,len(rad)):
            a = rad[i]*0.2*22.4 #opgewekte energie
            totaal_opgewekte_energie = totaal_opgewekte_energie + a
            opgewekte_energie.append(a)
        totaal_opgewekte_energie = round(totaal_opgewekte_energie,2)
        opgewekte_energie = zonne_energie
        totaal_opgewekte_energie = zonne_energie_sum/1000
        verbruikte_energie_auto = []
        verbruikte_energie_wasmachine = []
        verbruikte_energie_keuken = []
        totaal_verbruikte_energie_auto = 0
        totaal_verbruikte_energie_wasmachine = 0
        totaal_verbruikte_energie_keuken = 0

        totaal_verbruikte_energie_warmtepomp = sum(verbruikwarmtepomp)/1000
        totaal_verbruikte_energie_airco = sum(verbruikeAirco)/1000
        totaal_verbruikte_energie_warmtepomp = round(totaal_verbruikte_energie_warmtepomp,2)
        totaal_verbruikte_energie_airco = round(totaal_verbruikte_energie_airco,2)
        #verbruikeAirco = [verbruikeAirco[i] * 1000 for i in range(48)]
        #verbruikwarmtepomp = [verbruikwarmtepomp[i] * 1000 for i in range(48)]
        for i in auto:
            if i == 1.0:
                verbruikte_energie_auto.append(7400)
                totaal_verbruikte_energie_auto = totaal_verbruikte_energie_auto + 7400
            else:
                verbruikte_energie_auto.append(0)
        for i in wasmachine:
            if i == 1:
                verbruikte_energie_wasmachine.append(2500)
                totaal_verbruikte_energie_wasmachine = totaal_verbruikte_energie_wasmachine + 2500
            else:
                verbruikte_energie_wasmachine.append(0)
        for i in keuken_verbruik:
            if i == 1:
                verbruikte_energie_keuken.append(2100)
                totaal_verbruikte_energie_keuken = totaal_verbruikte_energie_keuken + 2100
            else:
                verbruikte_energie_keuken.append(0)
        verbruikte_energie = [verbruikte_energie_auto[i] + verbruikte_energie_wasmachine[i]+verbruikte_energie_keuken[i] + verbruikwarmtepomp[i*2]/2 + verbruikeAirco[i*2+1]/2 +verbruikeAirco[i*2]/2 + verbruikwarmtepomp[i*2+1]/2 for i in range(24)]
        totale_prijs_energie = kostprijs_en
        
        totale_prijs_energie = round(totale_prijs_energie,2)
        totaal_verbruikte_energie = sum(verbruikte_energie)/1000
        totaal_verbruikte_energie_auto = totaal_verbruikte_energie_auto / 1000
        totaal_verbruikte_energie_wasmachine = totaal_verbruikte_energie_wasmachine / 1000
        totaal_verbruikte_energie_keuken = totaal_verbruikte_energie_keuken / 1000
        gemiddeldeTemperatuur = sum(temp)/len(temp)
        gemiddeldeBinnenTemperatuur = sum(binnentemp)/len(binnentemp)
        totaal_verbruikte_energie = round(totaal_verbruikte_energie,2)
        totaal_opgewekte_energie = round(totaal_opgewekte_energie,2)
        gemiddeldeTemperatuur = round(gemiddeldeTemperatuur,2)
        gemiddeldeBinnenTemperatuur = round(gemiddeldeBinnenTemperatuur,2)
        gemiddeldeElektriciteitsprijs = sum(dataprijs)/len(dataprijs)
        gemiddeldeElektriciteitsprijs = gemiddeldeElektriciteitsprijs/1000
        gemiddeldeElektriciteitsprijs = round(gemiddeldeElektriciteitsprijs,5)
        kost_zonderOP = custom_dag(dataprijs,rad,thuis_zijn,True,wasmachine_knop,auto_knop,keuken_boolean,temp)
        kost_zonderOP = round(kost_zonderOP,2)
        kostverschil = kost_zonderOP - totale_prijs_energie
        kostverschil = round(kostverschil,2)
        for i in range(len(verbruikte_energie)):
            verbruikte_energie[i] = verbruikte_energie[i] / 1000
        for i in range(len(opgewekte_energie)):
            opgewekte_energie[i] = opgewekte_energie[i] / 1000
        for i in range(len(verbruikeAirco)):
            verbruikeAirco[i] = verbruikeAirco[i] / 1000
        
        return render_template('index.html', selectedDate=selected_date, result=result,keuken=keuken,totaal_opgewekte_energie=totaal_opgewekte_energie, totaal_verbruikte_energie = totaal_verbruikte_energie,totale_prijs_energie=totale_prijs_energie,gemiddeldeElektriciteitsprijs=gemiddeldeElektriciteitsprijs,kost_zonderOP=kost_zonderOP,kostverschil=kostverschil)
    return render_template('indextest.html')
@app.route('/page1.html')
def pagina1():
    return render_template('index.html', selectedDate=selected_date, result=result ,keuken=keuken,totaal_opgewekte_energie=totaal_opgewekte_energie, totaal_verbruikte_energie = totaal_verbruikte_energie,totale_prijs_energie=totale_prijs_energie,gemiddeldeElektriciteitsprijs=gemiddeldeElektriciteitsprijs,kost_zonderOP=kost_zonderOP,kostverschil=kostverschil)

@app.route('/page2.html')
def pagina2():
    weather_statuses = ['cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny']
    return render_template('page2.html', weather_statuses=weather_statuses, gemiddeldeTemperatuur=gemiddeldeTemperatuur, gemiddeldeBinnenTemperatuur=gemiddeldeBinnenTemperatuur,totaal_verbruikte_energie_airco=totaal_verbruikte_energie_airco,totaal_verbruikte_energie_warmtepomp=totaal_verbruikte_energie_warmtepomp)

@app.route('/page3.html')
def pagina3():
    return render_template('page1.html')
if __name__ == '__main__':
    app.run()
#host='192.168.98.15'




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

