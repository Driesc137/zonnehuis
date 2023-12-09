from functools import reduce
import mysql.connector
def vervang_komma_door_punt(input_string):
    # Vervang alle komma's door punten
    output_string = input_string.replace(',', '.')
    return output_string
def removeSpaces(string):
        return reduce(lambda x, y: (x + y) if (y != " ") else x, string, ""); 
import mysql.connector

def getFromDB(date):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Azerty123",
        database="pno3"
    )
    lijst = []
    datum = str(date)
    if datum[8] != "0":
        datum0 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 0:00:00"
        datum1 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 1:00:00"
        datum2 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 2:00:00"
        datum3 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 3:00:00"
        datum4 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 4:00:00"
        datum5 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 5:00:00"
        datum6 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 6:00:00"
        datum7 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 7:00:00"
        datum8 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 8:00:00"
        datum9 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 9:00:00"
        datum10 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 10:00:00"
        datum11 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 11:00:00"
        datum12 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 12:00:00"
        datum13 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 13:00:00"
        datum14 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 14:00:00"
        datum15 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 15:00:00"
        datum16 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 16:00:00"
        datum17 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 17:00:00"
        datum18 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 18:00:00"
        datum19 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 19:00:00"
        datum20 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 20:00:00"
        datum21 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 21:00:00"
        datum22 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 22:00:00"
        datum23 = datum[8] + datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 23:00:00"
    else:
        datum0 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 0:00:00"
        datum1 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 1:00:00"
        datum2 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 2:00:00"
        datum3 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 3:00:00"
        datum4 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 4:00:00"
        datum5 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 5:00:00"
        datum6 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 6:00:00"
        datum7 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 7:00:00"
        datum8 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 8:00:00"
        datum9 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 9:00:00"
        datum10 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 10:00:00"
        datum11 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 11:00:00"
        datum12 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 12:00:00"
        datum13 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 13:00:00"
        datum14 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 14:00:00"
        datum15 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 15:00:00"
        datum16 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 16:00:00"
        datum17 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 17:00:00"
        datum18 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 18:00:00"
        datum19 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 19:00:00"
        datum20 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 20:00:00"
        datum21 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 21:00:00"
        datum22 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 22:00:00"
        datum23 = datum[9] + "/" + datum[5] + datum[6] + "/" + datum[0] + datum[1] + datum[2] + datum[3] + " 23:00:00"

    mycursor = db.cursor()
    
    # Gebruik parameterisatie om de datumvariabele in de query in te voegen
    query = "SELECT name, address FROM personen WHERE name = %s"
    
    # Voer de query uit met de datum als parameter
    mycursor.execute(query, (datum0,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum1,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum2,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum3,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum4,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum5,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum6,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum7,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum8,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum9,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum10,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum11,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum12,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum13,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum14,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum15,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum16,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum17,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum18,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum19,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum20,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum21,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum22,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    mycursor.execute(query, (datum23,))
    resultaat = mycursor.fetchone()
    if resultaat:
        resultaat = list(resultaat)
        resultaat[1] = removeSpaces(resultaat[1])
        resultaat[1] = vervang_komma_door_punt(resultaat[1])
        lijst.append(float(resultaat[1]))
    
    return lijst

def getTempFromDB(date):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Azerty123",
        database="pno3"
    )
    temp = []
    solarenergy = []
    datum = str(date)
    datum0 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T00:00:00"
    datum1 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T01:00:00"
    datum2 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T02:00:00"
    datum3 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T03:00:00"
    datum4 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T04:00:00"
    datum5 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T05:00:00"
    datum6 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T06:00:00"
    datum7 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T07:00:00"
    datum8 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T08:00:00"
    datum9 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T09:00:00"
    datum10 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T10:00:00"
    datum11 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T11:00:00"
    datum12 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T12:00:00"
    datum13 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T13:00:00"
    datum14 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T14:00:00"
    datum15 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T15:00:00"
    datum16 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T16:00:00"
    datum17 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T17:00:00"
    datum18 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T18:00:00"
    datum19 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T19:00:00"
    datum20 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T20:00:00"
    datum21 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T21:00:00"
    datum22 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9] + "T22:00:00"
    datum23 = datum[0] + datum[1] + datum[2] + datum[3] + "-" + datum[5] + datum[6] + "-" + datum[8] + datum[9]+ "T23:00:00"
    print(datum0)
    mycursor = db.cursor()
    query = "SELECT datum, temp, solarradiation FROM weer WHERE datum = %s"
    
    mycursor.execute(query, (datum0,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum1,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum2,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum3,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum4,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum5,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum6,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum7,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum8,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum9,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum10,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum11,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum12,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum13,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum14,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum15,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum16,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum17,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum18,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum19,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum20,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum21,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum22,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))

    mycursor.execute(query, (datum23,))
    resultaat = mycursor.fetchone()
    temp.append(float(resultaat[1]))
    solarenergy.append(float(resultaat[2]))
    return temp, solarenergy
    
# Test met een voorbeelddatum
#result = getFromDB("2022-12-11")
#if result:
    #print(result)
   #print('test')
#else:
    #print("Geen resultaat gevonden.")
reult = getTempFromDB("2022-03-27")
print(reult)