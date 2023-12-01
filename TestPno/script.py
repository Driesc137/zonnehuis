from flask import Flask, render_template, request, jsonify
from getfromdb import getFromDB,getTempFromDB
from TEST_controller.TEST_Controller import controller
import random
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
    
    return jsonify(opgewekte_energie)
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
        global rad
        template = request.form['template'] #templates
        button1 = request.form.get('button1') == 'true' #datum
        button2 = request.form.get('button2') == 'true'
        button3 = request.form.get('button3') == 'true'
        button4 = request.form.get('button4') == 'true'
        button5 = request.form.get('button5') == 'true'
        prijs1 = request.form.get('price1')
        keuken = get_keuken()
        auto_knop = request.form.get('auto') == 'true'
        wasmachine_knop = request.form.get('wasmachine') == 'true'
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
        opgewekte_energie = []
        global totaal_opgewekte_energie
        totaal_opgewekte_energie = 0
        
        if template == 'true':
            if lage_elec == True:
                data = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]    
            if fluc_elec == True:
                data = [150,450,-20,35,0,500,-10,70,9,12,-1,110,12,44,-14,150,155,-35,18,190,2,210,-22,23]
            if hoge_elec == True:
                data = [400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400]
            if koud == True:
                temp= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if gematigd == True:
                temp = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
            if warm == True:
                temp = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
            if button5 == True:
                rad1 = [random.choice([0, 0.1, 0.2,0.3,0.4,0.5]) for _ in range(9)]
                rad2 = [0,0,0,0,0,0,0,0,0,0]
                rad3 = [random.choice([0, 0.1, 0.2,0.3,0.4,0.5]) for _ in range(5)]
                rad = rad1 + rad2 + rad3
            if button4 == True:
                rad1 = [random.choice([1.5, 1, 1.1,1.4]) for _ in range(9)]
                rad2 = [0,0,0,0,0,0,0,0,0,0]
                rad3 = [random.choice([1.5, 1, 1.1,1.4]) for _ in range(5)]
                rad = rad1 + rad2 + rad3
            if button3 == True:
                rad1 = [random.choice([3.5, 4, 3.7,3.2,4.1]) for _ in range(9)]
                rad2 = [0,0,0,0,0,0,0,0,0,0]
                rad3 = [random.choice([3.5, 4, 3.7,3.2,4.1]) for _ in range(5)]
                rad = rad1 + rad2 + rad3
        if button1 == True:
            data = getFromDB(selected_date)
            [temp,rad] = getTempFromDB(selected_date)
        [auto, wasmachine,gekochte_energie,verkochte_energie,verbruikwarmtepomp,binnentemp] = controller(temp,data,rad,wasmachine_knop,auto_knop)
        result = "Dit is de uitvoer van de Python-code."
        for i in range(0,len(rad)):
            a = rad[i]*0.2*22.4 #opgewekte energie
            totaal_opgewekte_energie = totaal_opgewekte_energie + a
            opgewekte_energie.append(a)
        totaal_opgewekte_energie = round(totaal_opgewekte_energie,2)
        return render_template('index.html', selectedDate=selected_date, result=result,keuken=keuken,totaal_opgewekte_energie=totaal_opgewekte_energie)
    return render_template('indextest.html')
@app.route('/page1.html')
def pagina1():
    return render_template('index.html')

@app.route('/page2.html')
def pagina2():
    weather_statuses = ['cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny']
    return render_template('page2.html', weather_statuses=weather_statuses)

@app.route('/page3.html')
def pagina3():
    return render_template('page1.html')
if __name__ == '__main__':
    app.run()
#host='192.168.98.15'