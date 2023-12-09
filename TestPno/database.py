import csv
from functools import reduce
import mysql.connector

def removeSpaces(string):
        return reduce(lambda x, y: (x + y) if (y != " ") else x, string, "");

def removeLetter(letter):
    csv_file=open("test.csv")
    csv_reader=csv.reader(csv_file,delimiter=";")
    lijnen=[]
    for line in csv_reader:
        lijnen.extend(line)
    l = 0
    while l < len(lijnen):
        lijnen[l]=lijnen[l].replace(letter,"")
        l+=1
    return lijnen

def leesIn(bestand):
    csv_file=open(bestand)
    csv_reader=csv.reader(csv_file,delimiter=",")
    lijnen=[]
    for line in csv_reader:
        lijnen.extend(line)
    return lijnen

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Azerty123",
    database="pno3"
    )
data=removeLetter("Ä")
data2 = leesIn("test2.csv")
mycursor = db.cursor()
for element in data:
    removeSpaces(element)
    element.strip()

mycursor.execute("DROP TABLE weer")
mycursor.execute("CREATE TABLE weer (id INT AUTO_INCREMENT PRIMARY KEY, naam VARCHAR(255),datum VARCHAR(255),temp VARCHAR(255),feelslike VARCHAR(255),dew VARCHAR(255),humidity VARCHAR(255),precip VARCHAR(255),precipprob VARCHAR(255),preciptype VARCHAR(255),snow VARCHAR(255),snowdepth VARCHAR(255),windgust VARCHAR(255),windspeed VARCHAR(255),winddir VARCHAR(255),sealevelpressure VARCHAR(255),cloudcover VARCHAR(255),visibility VARCHAR(255),solarradiation VARCHAR(255),solarenergy VARCHAR(255),uvindex VARCHAR(255),severerisk VARCHAR(255),conditions VARCHAR(255),icon VARCHAR(255),stations VARCHAR(255))")
mycursor.execute("DROP TABLE personen")
mycursor.execute("CREATE TABLE personen (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
#mycursor.execute("INSERT INTO personen (name, address) VALUES (%s, %s)", ("senne", "test"))


sql = "INSERT INTO personen(name,address) VALUES (%s,%s)"
i = 0
while i < len(data):
    mycursor.execute(sql,(data[i],data[i+1]))
    i+=2
db.commit()
#mycursor.execute("SELECT * FROM personen")
mycursor.execute("SELECT name, address FROM personen WHERE name = '11/10/2022 11:00:00'")
for x in mycursor:
    resultaat = (list(x))
resultaat[1] = removeSpaces(resultaat[1])
print(removeSpaces(resultaat[1]))


sql1 = "INSERT INTO weer(naam,datum,temp,feelslike,dew,humidity,precip,precipprob,preciptype,snow,snowdepth,windgust,windspeed,winddir,sealevelpressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,severerisk,conditions,icon,stations) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
i = 0
while i < len(data2):
    mycursor.execute(sql1,(data2[i],data2[i+1],data2[i+2],data2[i+3],data2[i+4],data2[i+5],data2[i+6],data2[i+7],data2[i+8],data2[i+9],data2[i+10],data2[i+11],data2[i+12],data2[i+13],data2[i+14],data2[i+15],data2[i+16],data2[i+17],data2[i+18],data2[i+19],data2[i+20],data2[i+21],data2[i+22],data2[i+23]))
    i+=24
db.commit()
sql = "INSERT INTO weer (naam, datum, temp, feelslike, dew, humidity, precip, precipprob, preciptype, snow, snowdepth, windgust, windspeed, winddir, sealevelpressure, cloudcover, visibility, solarradiation, solarenergy, uvindex, severerisk, conditions, icon, stations) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Vul de waarden in voor het nieuwe record
values = (
    'naam_value',
    '2022-03-27T02:00:00',
    '9.7',
    '7.9',
    '6.2',
    '78.83',
    '0',
    '0',
    '',
    '0',
    '0',
    '28.4',
    '12.7',
    '50',
    '1031.7',
    '0',
    '10',
    '0',
    '0',
    '0',
    '10',
    'clear',
    'clear-night',
    ''
)

mycursor.execute(sql, values)

# Commit de transactie
db.commit()




# Stel de datum in die je wilt verwijderen
teVerwijderenDatum = '2022-10-30T02:00:00'

# Voer de DELETE-query uit om het record met de opgegeven datum te verwijderen
sql = "DELETE FROM weer WHERE datum = %s"
mycursor.execute(sql, (teVerwijderenDatum,))

# Commit de transactie
db.commit()



sql = "INSERT INTO weer (naam, datum, temp, feelslike, dew, humidity, precip, precipprob, preciptype, snow, snowdepth, windgust, windspeed, winddir, sealevelpressure, cloudcover, visibility, solarradiation, solarenergy, uvindex, severerisk, conditions, icon, stations) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Vul de waarden in voor het nieuwe record
values = (
    'naam_value',
    '2022-10-30T02:00:00',
    '16.4',
    '7.9',
    '6.2',
    '78.83',
    '0',
    '0',
    '',
    '0',
    '0',
    '28.4',
    '12.7',
    '50',
    '1031.7',
    '0',
    '10',
    '0',
    '0',
    '0',
    '10',
    'clear',
    'clear-night',
    ''
)

mycursor.execute(sql, values)

# Commit de transactie
db.commit()

#mycursor.execute("SELECT * FROM weer")
mycursor.execute("SELECT datum, temp FROM weer WHERE datum = '2022-03-27T02:00:00'")
for x in mycursor:
    resultaat2 = (list(x))
resultaat2[1] = removeSpaces(resultaat2[1])
print(removeSpaces(resultaat2[1]))

#2022-03-27T02:00:00