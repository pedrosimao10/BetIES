import pyodbc
import random
import sys
import time
import datetime 

server = 'pedrojorge-Legion-Y540-15IRH-PG0'
database = 'betIES'
username = 'beties'
password = 'projeto.1'   
driver= '{ODBC Driver 17 for SQL Server}'
ligas = {}

def main():
    global server, database, username, password, driver, ligas
    
    inserts()

    for liga in ligas:
        criarJornada(ligas[liga][1], liga)
    
    refresh()

def refresh():
    global server, database, username, password, driver, ligas

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+'; Trusted_Connection=yes;') as conn:
        with conn.cursor() as cursor:
            while True:
                print("refresh")
                dicionario = {}
                cursor.execute("SELECT * from jogos")
                row = cursor.fetchone()
                
                while row:
                    jogoId = row.id
                    odd1 = float(row.odd1)
                    odd2 = float(row.odd2)
                    odd3 = float(row.odd3)
                    rand = random.random()
                    randOdd = random.random()
                    
                    if odd1<=1 or odd2<=1 or odd3<=1:                
                        print(row)
                    if odd1 > 3 and odd3 > 3:
                        print(row)
                    
                    if odd1 > 2.8 and odd3 > 2.8:
                        newOdd1 = round(odd1 - randOdd/40 , 2)
                        newOdd3 = round(odd3 - randOdd/40 , 2)
                    elif odd1 < 1.05:
                        newOdd1 = round(odd1 + randOdd/40 , 2)
                        newOdd3 = round(odd3 - randOdd/40 , 2)
                    elif odd3 < 1.05:
                        newOdd1 = round(odd1 - randOdd/40 , 2)
                        newOdd3 = round(odd3 + randOdd/40 , 2)
                    elif rand >= 0.5:
                        newOdd1 = round(odd1 + randOdd/40 , 2)
                        newOdd3 = round(odd3 - randOdd/40 , 2)
                    elif rand < 0.5:
                        newOdd1 = round(odd1 - randOdd/40 , 2)
                        newOdd3 = round(odd3 + randOdd/40 , 2)
                    else:
                        print("\n\n\nnão devia chegar aqui\n\n\n")

                    if odd2 < 1.05:
                        newOdd2 = round(odd2 + randOdd/40, 2)
                    elif rand > 0.5:
                        newOdd2 = round(odd2 - randOdd/40, 2)
                    else:
                        newOdd2 = round(odd2 + randOdd/40, 2)

                    dicionario[jogoId] = [newOdd1, newOdd2, newOdd3]
                    
                    row = cursor.fetchone()
                
                for jogo in dicionario:
                    cursor.execute("update jogos set odd1 = ?, odd2 = ?, odd3 = ? where id = ?", dicionario[jogo][0], dicionario[jogo][1], dicionario[jogo][2], jogo)
                    conn.commit()

                time.sleep(5)

def inserts():
    global server, database, username, password, driver, ligas

    file1 = open('inserts.txt', 'r')
    Lines = file1.readlines()
    insertedDesporto = []
    insertedLiga = []
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+'; Trusted_Connection=yes;') as conn:
        with conn.cursor() as cursor:
            for line in Lines:
                #print(line)
                linhas = line.replace('\n', ' ').replace('\r', '').split(';')
                for linha in linhas:
                    if len(linha)>1:
                        tmp = linha.split(',')
                        #print(tmp)
                        desporto = tmp[0].strip()
                        tmp.remove(tmp[0])
                        if desporto not in insertedDesporto:
                            insertedDesporto.append(desporto)
                            cursor.execute("insert into desportos(nome) values (?)", desporto)
                            conn.commit()
                        liga = tmp[0].strip()
                        tmp.remove(tmp[0])
                        if liga not in insertedLiga:
                            insertedLiga.append(liga)
                            cursor.execute("insert into ligas(nome, desporto) values (?, ?)", liga, insertedDesporto.index(desporto)+1)
                            conn.commit()
                        equipas = []
                        count = 1;
                        for equipa in tmp:
                            cursor.execute("insert into equipas(nome, desporto, liga) values (?, ?, ?)", equipa.strip(), insertedDesporto.index(desporto)+1, insertedLiga.index(liga)+1)
                            conn.commit()
                            equipas.append([count, equipa.strip()])
                            count += 1
                        ligas[liga] = [desporto, equipas]


def criarJornada(equipas, liga):
    global server, database, username, password, driver, ligas
    
    jogos = []

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+'; Trusted_Connection=yes;') as conn:
        with conn.cursor() as cursor:

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

                current_time = datetime.datetime.now()
                rand = random.randint(0, 4)
                dia = current_time + datetime.timedelta(days=rand)
                hora = random.randint(12, 21)
                minuto = random.randrange(0, 46, 15)

                if minuto == 0:
                    horario = str(dia)[:11].replace('-', '') + str(hora) + ":00:00"
                else:
                    horario = str(dia)[:11].replace('-', '') + str(hora) + ":" + str(minuto) + ":00"
                #print(horario)

                jogo = [[equipa1[1], odd1], odd2, [equipa2[1], odd3], horario]
                jogos.append(jogo)
                cursor.execute("SELECT id from equipas where ? = nome and (select id from ligas where ? = nome) = liga", equipa1[1], liga)
                row = cursor.fetchone()
                while row:
                    equipa1id = row.id
                    row = cursor.fetchone()
                cursor.execute("SELECT id from equipas where ? = nome and (select id from ligas where ? = nome) = liga", equipa2[1], liga)
                row = cursor.fetchone()
                while row:
                    equipa2id = row.id
                    row = cursor.fetchone()
                cursor.execute("insert into jogos(equipa1, equipa2, odd1, odd2, odd3, hora) values (?, ?, ?, ?, ?, ?)", equipa1id, equipa2id, odd1, odd2, odd3, horario)
                conn.commit()
    return jogos

if __name__ == "__main__":
    if len(sys.argv) > 1:
        refresh()
    else:
        main()