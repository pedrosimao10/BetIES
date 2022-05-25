import random
import pika
import json
import time
from datetime import datetime, timedelta
import mysql.connector

from pypika import Table, Query
import pyodbc

ligas = {}

class DataGenerator:
    
    def __init__(self):
        self.credentials = pika.PlainCredentials('beties','beties')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host= 'localhost', port = '5672', credentials= self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='beties', durable=True)

    def refresh(self):
        print("REFRESH")
        message = {'method': 'REFRESH'}
        self.send('beties', message)
        pass

    def insertInstrucoes(self):

        empregados = ["Afonso Rodrigues","Alexandre Pinto","Gonçalo Pereira","Pedro Jorge"]
        instrucoes = ["Atualizar os jogos das ligas.","Atualizar as datas dos jogos adiados devido à covid-19.","Verificar irregularidades."]
        datas = ["25/01/2022","26/01/2022","27/01/2022","28/01/2022","29/01/2022","30/01/2022"]
        estados = ["Pendente","Terminado","Em andamento"]

        for i in range(10):
            message = {'method': 'NEW_INSTRUCAO', 'employeeName': random.choice(empregados), 'instrucao': random.choice(instrucoes), 'data': random.choice(datas), 'estado': random.choice(estados)}
            self.send('beties', message)

    def criarJornada(self,equipas, liga):
        global ligas

        jogos = []

        while len(equipas)>1:
            equipa1 = random.choice(equipas)
            equipa2 = random.choice(equipas)
            while equipa2 == equipa1:
                equipa2 = random.choice(equipas)
            diferenca = equipas.index(equipa1) - equipas.index(equipa2)
            equipas.remove(equipa1)
            equipas.remove(equipa2)

            if diferenca>10:
                odd1 = round(4 + abs(diferenca)/8 + random.random(), 2)
                odd2 = round(3 + abs(diferenca)/10 + random.random(), 2)
                odd3 = round(1.01 + random.random()/2, 2)
            elif diferenca>5:
                odd1 = round(3 + abs(diferenca)/10 + random.random(), 2)
                odd2 = round(2 + abs(diferenca)/10 + random.random(), 2)
                odd3 = round(1 + abs(diferenca)/10 + random.random(), 2)
            elif diferenca>0:
                odd1 = round(2.5 + abs(diferenca)/12 + random.random(), 2)
                odd2 = round(2 - abs(diferenca)/12 + random.random(), 2)
                odd3 = round(2 - abs(diferenca)/12 + random.random(), 2)
            elif diferenca>-5:
                odd1 = round(2 - abs(diferenca)/12 + random.random(), 2)
                odd2 = round(2 - abs(diferenca)/12 + random.random(), 2)
                odd3 = round(2.5 + abs(diferenca)/12 + random.random(), 2) 
            elif diferenca>-10:
                odd1 = round(1 + abs(diferenca)/10 + random.random(), 2)
                odd2 = round(2 + abs(diferenca)/10 + random.random(), 2)
                odd3 = round(3 + abs(diferenca)/10 + random.random(), 2)
            else:
                odd1 = round(1.01 + random.random()/2, 2)
                odd2 = round(3 + abs(diferenca)/10 + random.random(), 2)
                odd3 = round(4 + abs(diferenca)/8 + random.random(), 2)

            if odd1<=1 or odd2<=1 or odd3<=1:                
                print("merda")
            if odd1 > 3 and odd3 > 3:
                print(str(equipa1) + " + " + str(equipa2))

            current_time = datetime.now()
            rand = random.randint(0, 4)
            dia = current_time + timedelta(days=rand)
            hora = random.randint(12, 21)
            minuto = random.randrange(0, 46, 15)

            if minuto == 0:
                horario = str(dia)[:11].replace('-', '') + str(hora) + ":00:00"
            else:
                horario = str(dia)[:11].replace('-', '') + str(hora) + ":" + str(minuto) + ":00"

            jogo = [[equipa1[1], odd1], odd2, [equipa2[1], odd3], horario]
            jogos.append(jogo)

            message = {'method': 'NEW_JORNADA', 'jogo': jogo, 'liga': liga, 'horario': horario}
            self.send('beties', message)

            print(jogo)

        pass

    def initialInserts(self):
        global ligas

        file1 = open('inserts.txt', 'r')
        Lines = file1.readlines()
        insertedDesporto = []
        insertedLiga = []

        for line in Lines:
            linhas = line.replace('\n', ' ').replace('\r', '').split(';')
            for linha in linhas:
                if len(linha)>1:
                    tmp = linha.split(',')
                    #print(tmp)
                    desporto = tmp[0].strip()
                    tmp.remove(tmp[0])
                    if desporto not in insertedDesporto:
                        insertedDesporto.append(desporto)
                        message = {'method': 'NEW_DESPORTO', 'desporto': desporto}
                        self.send('beties', message)
                    liga = tmp[0].strip()
                    tmp.remove(tmp[0])
                    if liga not in insertedLiga:
                        insertedLiga.append(liga)
                        message = {'method': 'NEW_LIGA', 'liga': liga, 'desporto': insertedDesporto.index(desporto)+1}
                        self.send('beties', message)
                    equipas = []
                    count = 1
                    for equipa in tmp:
                        message = {'method': 'NEW_EQUIPA', 'equipa': equipa.strip(), 'desporto':  int (insertedDesporto.index(desporto)+1), 'liga': int(insertedLiga.index(liga)+1)}
                        self.send('beties', message)
                        equipas.append([count, equipa.strip()])
                        count += 1
                    ligas[liga] = [desporto, equipas]
        

    def generatePassage(self):
        message = {'method': 'NEW_PASSAGE', 'identifier': random.randint(1, 2), 'scut': random.randint(1, 3), 'date': datetime.now().strftime("%Y-%m-%d"), 'time': datetime.now().strftime("%H:%M:%S")}
        self.send('beties', message)
        
    def send(self, topic=None, message=None):
        try:
            message = json.dumps(message)
            self.channel.basic_publish(exchange='', routing_key=topic, body=message)
            #print(message)
            #print(" [x] Sent 'MESSAGE!'")
        except:
            print("ERROR: Message to broker was not sent")  
                

def main():
    global ligas
    generator = DataGenerator()
    generator.initialInserts()
    generator.insertInstrucoes()
    
    for liga in ligas:
        print(liga)
        generator.criarJornada(ligas[liga][1], liga)

    while True:
        generator.refresh()
        t = random.randint(5, 10)
        time.sleep(t)
        


if __name__ == "__main__":
    main()