import random
import pika
import json
import time
from datetime import datetime
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


    def insertInstrucoes(self):

        empregados = ["Afonso Rodrigues","Alexandre Pinto","Gonçalo Pereira","Pedro Jorge"]
        instrucoes = ["Atualizar os jogos das ligas.","Atualizar as datas dos jogos adiados devido à covid-19.","Verificar irregularidades."]
        datas = ["25/01/2022","26/01/2022","27/01/2022","28/01/2022","29/01/2022","30/01/2022"]
        estados = ["Pendente","Terminado","Em andamento"]

        for i in range(10):
            message = {'method': 'NEW_INSTRUCAO', 'employeeName': random.choice(empregados), 'instrucao': random.choice(instrucoes), 'data': random.choice(datas), 'estado': random.choice(estados)}
            self.send('beties', message)
        
        
    def send(self, topic=None, message=None):
        try:
            message = json.dumps(message)
            self.channel.basic_publish(exchange='', routing_key=topic, body=message)
        except:
            print("ERROR: Message to broker was not sent")  
                

def main():
    generator = DataGenerator()
    generator.insertInstrucoes()
        


if __name__ == "__main__":
    main()