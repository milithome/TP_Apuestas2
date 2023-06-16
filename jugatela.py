import os
import requests
from passlib.hash import sha256_crypt
import csv
import random
import matplotlib.pyplot as plt 
#permitir ingreso usuario y demas

def validar_usuario(usuario:str)->bool:
    if usuario in ("a","b"):
        return True
    else: return False

def validar_mail(mail:str,ids:list)->bool:
    if mail not in ids:
        return True
    else: return False

def user_registration(id_usuarios:list)->str:
    #PRECONDICIONES: UN NUEVO USER QUIERE GENERAR UNA CUENTA 
    #POSTCONDICIONES: MAIL QUE DEBE SER UNICO
    #pido datos al user
    print("Ingrese los siguientes datos, como se detalle a continucion: ")
    mail = input("Correo electronico: ")
    while(validar_mail(mail,id_usuarios)==False):
        print("El correo electronico ingresado ya se encuentra en uso.")
        print("Ingrese otro.")
        mail = input("Correo electronico: ")
    name = input("Nombre Usuario: ")
    password = sha256_crypt.hash(input("Contraseña: "))
    money = float(input("Dinero inicial que desea ingresar: "))

    #por ultimo se agrega este nuevo user al archivo, con esta funcion se consigue guardar lo que ya estaba en el archivo y reescribirlo + el nuevo usuario
    archivo_csv_r_w_data_users(mail,name,password,money)
    print(f"El usuario {name} ligado al correo electronico {mail} se ha registrado con exito.")

    return mail


def archivo_csv_r_w_data_users(new_mail:str,new_name:str,new_password:str,new_money:float)->None:

    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'

    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'name':row[1],'password':row[2],'bets':row[3],'date':row[4],'money': row[5]}

    users[new_mail]={'name':new_name,'password':new_password,'bets':0,'date':None,'money':new_money}

    with open('data_users.csv', 'w', newline='', encoding='UTF-8') as archivo_csv: #aclaro con un 'w' que es un archivo de escritura

        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['name','password','bets','money'])
        for mail, data in users.items():
            csv_writer.writerow([mail,data['name'],data['password'],data['bets'],data['date'],data['money']])

def equipos_liga_2023 () -> dict:
    url = "https://v3.football.api-sports.io/teams"
    parameters = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", 
               "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    equipos_2023 = {}
    dict_equipos = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        equipos_2023 = data ["response"]

        for equipo in range (28):
            dict_equipos[equipos_2023[equipo]["team"]["name"]] = equipos_2023[equipo]["team"]["id"]

    #procesa la data y devuelve un dict
     
    else:
        print("Err", respuesta.status_code )

    return dict_equipos


def fechas_teams(id_team:int)->dict:
    
    url = "https://v3.football.api-sports.io/fixtures?"

    parameters = {"league": "128","season": 2023,"team":id_team}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    fechas = {}
    locales = {}
    visitantes = {}
    if respuesta.status_code == 200:
        data = respuesta.json()
        fechas = data['response']
        print(f"Fechas de Temporada 2023:")

        for fecha in range(len(fechas[0]['fixture'])):
            locales[fechas[0]['fixture']['teams']['home']['name']]= fechas[0]['fixture']['teams']['home']['id']
            visitantes[fechas[0]['fixture']['teams']['away']['name']] = fechas[0]['fixture']['teams']['away']['id'] 
            fechas[fecha] = [locales[fechas[0]['fixture']['teams']['home']['name']],visitantes[fechas[0]['fixture']['teams']['away']['name']]]           
        
        for i in (fechas):
            print(f"Fecha {i+1}: {fechas[i][0]} vs {fechas[i][1]}")

    else: print("Error al traer los datos")

    return fechas,locales,visitantes

def apuesta()->None:
    
    print("Estos son los equipos que estan participando del torneo 2023")

    equipos_dict = equipos_liga_2023()

    equipo_op = input("Elija por cual equipo desea apostar: ")
    while(equipo_op not in equipos_dict.values()):
        print("Opcion incorrecta, intente de nuevo")
        equipo_op = input("Elija por cual equipo desea apostar(ingrese el numero): ")

    id_equipo = equipos_dict[equipo_op]

    #funcion de buscar fechas
    dict_fechas,dict_locales,dict_visitantes = fechas_teams(id_equipo)

    fecha_elegida = input("Ingrese el num de fecha por el que desea apostar: ")





    
def main()->None:

    print("Bienvenido a la mejor plataforma de apuestas futboleras")
    ids_ingresados = []
    
    op = input("Desea acceder a la plataforma? y/n:")
    while(op.lower() not in ("y","n")):
        print("La opcion ingresada no se enuentra dentro de las posibles.")
        print("Ingrese de nuevo.")
        op = input("Desea acceder a la plataforma? y/n:")
    
    while(op.lower()!="n"):

        print("Jugatela: plataforma de apuestas.\nEsta plataforma requiere tener un usuario, elija segun el caso:")
        usuario = input("a-Iniciar sesion:\n b-Crearse una cuenta:\n")
        while(validar_usuario(usuario)==False):
            print("La opcion ingresada no se enuentra dentro de las posibles.")
            print("Ingrese de nuevo.")
            usuario = input("a-Iniciar sesion:\n b-Crearse una cuenta:\n")

        if usuario.lower()=="b":
            
            id_usario = user_registration(ids_ingresados)
            ids_ingresados.append(id_usario)

        elif usuario.lower()=="a":
            pass

        op = input("Desea acceder de nuevo a la plataforma? y/n:")

main()