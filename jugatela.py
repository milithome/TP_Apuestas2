
#keys:  mili: a991e40daffd726206f67b1a40947c67
#       vicky : a991e40daffd726206f67b1a40947c67

import os
import requests
from passlib.hash import sha256_crypt
import csv
import random
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np 
from PIL import Image
import re 

def validar_mail_2(mail:str,password:str,users:dict)->bool:
    
    if mail in users.keys() and sha256_crypt.verify(password, users[mail]["password"]):
        return True
    else: return False

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
    #PRECONDICIONES: CREAR ARCHIVO DATA USUARIO
    #POSTCONDICIONES: ARCHIVO GUARDA DATA USUARIO

    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'

    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, 'r', newline='',encoding="UTF-8") as archivo_csv:
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


def inicio_sesion () -> dict: 
    #PRECONDICIONES: USUARIO YA INGRESADO SISTEMA INICIA SESION
    #POSTCONDICIONES: DEVUELVE  MAIL  Y CONTRASEÑA  GUARDADO EN EL ARCHIVO DATA_USERS (USERS)

   users = {} #dict donde se va a guardar la data del archivo
   archivo_csv_users = 'data_users.csv'

   if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users
       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'name':row[1],'password':row[2]}
   return users


def imprimir_opciones()->None:
    #PRECONDICIONES: IMPRIMIR MENU OPCIONES
    #POSTCONDICIONES: MOSTRAR OPCIONES USUARIO

    print("Bienvenido a la mejor plataforma de apuestas futboleras")
    print ("Seleccione una opcion: ")
    print ("1. Mostrar el plantel completo de un equipo de la Liga Profesional 2023")
    print ("2. Mostrar la tabla de posiciones de la Liga profesional")
    print ("3. Estadios y escudos de los equipos ")
    print ("4. Grafico goles equipo determinado")
    print ("5. Cargar dinero en cuenta ")
    print ("6. Usuario que más dinero apostó")
    print ("7. Usuario que más veces ganó")
    print ("8. Apuestas")
    print ("9. SALIR")

def opcion_seleccionada (opcion_elegida:int, mail:str):   #agregar mas parametros si es necesario , equipos_2023:dict, jugadores_2023:dict
    #PRECONDICIONES: USARIO ELIGE OPCION 
    #POSTCONDICIONES: EJECUTO OPCION ELEGIDA    
    equipos_dict,equipos_id = equipos_liga_2023()

    if opcion_elegida == 1:#finished
        print("--- Equipos de la Liga Profesional Temporada 2023---")
        equipos_2023 = equipos_liga_2023 ()
        opcion_ids_equipos,opciones_equipos = listar_equipos_2023(equipos_2023)
        equipo_usuario = int(input("Seleccione equipo(escriba el numero que tiene al lado): "))
        while equipo_usuario not in opcion_ids_equipos.keys():
            print("Opcion incorrecta, por favor intente de nuevo.")
            opcion_ids_equipos = listar_equipos_2023 (equipos_2023)
            equipo_usuario = int(input("Seleccione equipo(escriba el numero que tiene al lado): "))
        
        id_equipo_usuario = opcion_ids_equipos[equipo_usuario]
        equipo = opciones_equipos[equipo_usuario]
        jugadores_2023 = jugadores_equipos()
        plantel_2023(id_equipo_usuario, equipo, jugadores_2023)

    elif opcion_elegida == 2:#finished
        print("---Tabla de posiciones de la Liga profesional---")
        temps = {1:2015,2:2016,3:2017,4:2018,5:2019,6:2020,7:2021,8:2022}
        print("Temporadas (años):")
        for i in temps.keys():
            print(f"{i}-{temps[i]}")
        temporada = int(input("Ingrese una de las temporadas en pantalla(oprima el numero que tiene al comienzo): "))
        while(temporada not in temps.keys()):
            print("Opcion incorrecta, intente de nuevo")
            print("Temporadas (años):")
            for i in range (len(temps)):
                print(f"{i+1}-{temps[i]}")
            temporada = input("Ingrese una de las temporadas en pantalla(oprima el numero que tiene al comienzo): ")
        
        mostrar_tabla_posiciones(temps[temporada])

    elif opcion_elegida == 3:#finished
        print ("--- Escudos y Estadios ---")
        num_equipos,equipos_dict = mostrar_teams()
        equipo_seleccionado=int(input("Seleccione equipo dentro del listado:"))
        while equipo_seleccionado not in num_equipos.keys():
            print("Opcion invalida, intente nuevamente.")
            print ("--- Escudos y Estadios ---")
            num_equipos,equipos_dict = mostrar_teams()
            equipo_seleccionado=int(input("Seleccione equipo dentro del listado:"))
        iddelequipo = equipos_dict[num_equipos[equipo_seleccionado]]
        escudo_cancha(iddelequipo)

    elif opcion_elegida == 4:#finished
        print ("--- Grafico goles y minutos ---")
        num_equipos,equipos_dict = mostrar_teams()
        equipo_seleccionado =int(input("Seleccione equipo dentro del listado(escribir numero de al lado):"))
        while(equipo_seleccionado not in num_equipos.keys()):
            print("Opcion invalida, intente de nuevo.")
            equipo_seleccionado:str =input("Seleccione equipo dentro del listado:")
        equipo_id = equipos_dict[num_equipos[equipo_seleccionado]]

        grafico(equipo_id) 

    elif opcion_elegida == 5:
        print ("--- Cargar dinero a cuenta ---")
        dinero = float(input("Ingrese la cantidad de dinero que desea agregar a su cuenta:"))
        fecha = input ("Ingrese fecha en formato YYYY/MM/DD: ")
        while validacion_fecha(fecha)==False:
            print("Formato incorrecto, intente de nuevo")
            fecha = input ("Ingrese fecha en formato YYYY/MM/DD: ")
        cargar_dinero_cuenta_usuario(mail, dinero,fecha)
    
    elif opcion_elegida == 6:
        print ("--- Usuario que más dinero apostó ---")
        usuario_mas_aposto (mail, "", "") 
        

    elif opcion_elegida == 7:
        print ("--- Usuario que más veces gano ---")
        usuario_mas_veces_gano(mail, "", "")

    elif opcion_elegida == 8:
        print("--- APUESTAS ---")
        apuesta(mail)
       

    else:
        print("Intente seleccionar una opcion del menu.")
        opcion_seleccionada(opcion_elegida,equipos_2023, jugadores_2023 )


def plantel_2023(id_equipo:int,equipo:str, jugadores_2023:dict):
    #PRECONDICIONES: EVALUA EQUIPO INGRESADO COINCIDE CON EL GUARDADO EN EL DICT EQUIPOS 2023
    #POSTCONDICIONES: IMPRIME PLANTEL

    print(f"\nPlantel de {equipo}  con ID {id_equipo}:")
    for jugador in jugadores_2023:
        if jugador['statistics'][0]['team']['id'] == id_equipo:
            print(jugador['player']['name'])       



def equipos_liga_2023_2 () -> dict:
    #PRECONDICIONES: BUSCO DATO API SOBRE EQUIPOS LIGA 2023
    #POSTCONDICIONES: DEVUELVE DICT CON LA INFO DE LOS EQUIPOS_2023    
    
    url = "https://v3.football.api-sports.io/teams"
    
    parameters = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    equipos_2023 = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        equipos_2023 = data ["response"]

    #procesa la data y devuelve un dict
    else:
        print("Err", respuesta.status_code )
    return equipos_2023


def jugadores_equipos ()-> dict:  #obtengo toda info de los jugadores, la guardo en un dict
    #PRECONDICIONES: BUSCO DATO API SOBRE JUGADORES 2023
    #POSTCONDICIONES: DEVUELVE DICT CON LA INFO DE LOS JUGADORES    
    
    url = "https://v3.football.api-sports.io/players"
    parameters ={"league": "128", "season": 2023}
    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "a991e40daffd726206f67b1a40947c67"}
    respuesta = requests.get (url, params = parameters, headers = headers)
    jugadores_2023 = {}
    if respuesta.status_code == 200:
        data = respuesta.json ()
        jugadores_2023 = data ["response"]
    else:
        print("Err", respuesta.status_code)

    return jugadores_2023

def listar_equipos_2023 (equipos_2023:dict) -> dict: 
    # PRE : enumerar los equipos
    # POST:  muestro por consola 
    
    opcion_equipos={}
    opcion_ids = {}

    i = 1
    
    for id in equipos_2023[1].keys():

        opcion_equipos[i] = equipos_2023[1][id]
        opcion_ids[i] = id

        print(f"{i}-{equipos_2023[1][id]}")

        i+=1

    return opcion_ids, opcion_equipos
    

def buscar_id_equipo(equipos_2023:dict, equipo_usuario:str) -> None:   #obtnego id del equipo que pide usuario y lo verifico
#PRE: obtnego id del equipo que pide usuario y lo verifico
#POST : devuelve id_equipo, del equipo ingresado por el usuario
   
    id_equipo_usuario = None
    for equipo in equipos_2023:
        if equipo_usuario == equipo["team"]["name"]:
            id_equipo_usuario = equipo["team"]["id"]
    return id_equipo_usuario 


def mostrar_tabla_posiciones(temporada:int)->None:
    #PRE: busco info en la api sobre las posciones de la liga arg
    #POST : muestra tabla posciones


    url = "https://v3.football.api-sports.io/standings"
    
    params = {"league": "128","season": temporada}
    
    headers = {'x-rapidapi-host': "v3.football.api-sports.io",'x-rapidapi-key': "a991e40daffd726206f67b1a40947c67"}
    
    respuesta = requests.get(url, params=params, headers=headers)
    
    posiciones={}
    if respuesta.status_code == 200:
        data = respuesta.json()
        posiciones = data['response']
        print("Posicion---Equipo---Pts---P.J---P.G---P.E---P.P")
        for equipo in range(len(posiciones[0]['league']['standings'][0])):
            print(posiciones[0]['league']['standings'][0][equipo]['rank'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['team']['name'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['points'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['all']['played'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['all']['win'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['all']['draw'],"-"*3,posiciones[0]['league']['standings'][0][equipo]['all']['lose'])
    else:
        print("Error en la solicitud:", respuesta.status_code)


def equipos_liga_2023 () -> dict:
    #PRECONDICIONES: BUSCO DATO API SOBRE EQUIPOS LIGA 2023
    #POSTCONDICIONES: DEVUELVE  2 DICTs CON LA INFO DE LOS EQUIPOS_2023

    url = "https://v3.football.api-sports.io/teams"
    parameters = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    equipos_2023 = {}
    dict_equipos_n_id = {}
    dict_equipos_id_n = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        equipos_2023 = data ["response"]
        
        for equipo in range (28):
            dict_equipos_n_id[equipos_2023[equipo]["team"]["name"]] = equipos_2023[equipo]["team"]["id"]
            dict_equipos_id_n[equipos_2023[equipo]["team"]["id"]] = equipos_2023[equipo]["team"]["name"]
    else:
        print("Err", respuesta.status_code )

    return dict_equipos_n_id,dict_equipos_id_n

def escudo_cancha(id_team: int)->None:
    #PRECONDICIONES: BUSCO DATO API SOBRE EQUIPOS LIGA 2023 , permito ingreso equipo por el usuario
    #POSTCONDICIONES: muestro escudo e info del estadio del equipo seleccionado    
    
    url = "https://v3.football.api-sports.io/teams?"
    parameters = {"id": id_team,"country": "Argentina","league": "128","season": "2023"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

    respuesta = requests.get(url, params = parameters, headers = headers)

    info_club = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        info_club = data ["response"]
        
        print("Equipo:")
        print(info_club[0]['team']['name'])
        print("Escudo:")
        url1:str = info_club[0]['team']['logo']
        urllogo = url1.replace("'","")
        response1 = requests.get(urllogo, stream =True)
        img = Image.open(response1.raw)
        plt.imshow(img)
        plt.show()
        print("Nombre del estadio:")
        print(info_club[0]['venue']['name'])
        print("Direccion:")
        print(info_club[0]['venue']['address'],info_club[0]['venue']['city'])
        print("Foto del estadio:")
        url2:str = info_club[0]['venue']['image']
        urlcancha = url2.replace("'","")
        response2 = requests.get(urlcancha,stream=True)
        img2 = Image.open(response2.raw)
        plt.imshow(img2)
        plt.show()
        
    else:
        print("Err", respuesta.status_code )

def grafico(equipo_id:int)->None:
    #PRE : busco datos api sobre las estadicticas de los equipos
    #POST: muestra grafico goles por minuto equipo selccionado por el usuario    

    url = "https://v3.football.api-sports.io/teams/statistics?"

    parameters = {"league": "128","season": 2023,"team":equipo_id}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

    respuesta = requests.get(url, params = parameters, headers = headers)

    dict_info = {}

    golesxminuto = {}

    mins = []

    goles = []

    if respuesta.status_code == 200:
        data = respuesta.json()
        dict_info = data['response']
        
        for minutos in dict_info['goals']['for']['minute']:
            mins.append(minutos)
            goles.append(dict_info['goals']['for']['minute'][minutos]['total'])
            golesxminuto[minutos] = dict_info['goals']['for']['minute'][minutos]['total']
        

        for y in range(len(goles)):
            if goles[y]==None: goles[y]=0
            else:continue 

        plt.bar(mins,goles)
        plt.title("Goles por minuto")
        plt.xlabel("Intervalos de minutos")
        plt.ylabel("cant. goles")
        plt.show()


def cargar_dinero_cuenta_usuario(mail, dinero, fecha): 
    #PRE :  verifivo usuario en el archivo data_usuario
    #POST:  carga dinero dsiponible cuenta usuario ingesada
    
    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'
   
    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, 'r', newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'money': row[5]}

    if mail  in users.keys():
        dinero_en_cuenta = users[mail]['money'] 
        dinero_actualizado = float(dinero_en_cuenta) + float(dinero)
        dinero_actualizado = float(dinero_actualizado)
    print (f"Ahora posee {dinero_actualizado} disponible en su cuenta. ")
    
    registrar_transacciones_usuarios (mail,fecha, "Deposita", dinero) #carga deposito de dinero en el archivo transacciones
    modificar_dinero_cuenta_usuario (mail, dinero, fecha) #guardo plata agregada en cuenta usuario


def fechas_teams(id_team: int) -> dict:
    url = "https://v3.football.api-sports.io/fixtures?"
    parameters = {"league": "128", "season": 2023, "team": id_team}
    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "a991e40daffd726206f67b1a40947c67"}
    respuesta = requests.get(url, params=parameters, headers=headers)
    dict_fechas = {}
    locales = {}
    visitantes = {}
    id_fecha = {}
    x_op_l_v = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        fixtures = data['response']

        x_op = 1

        print("Fechas de Temporada 2023:")
        for fixture in fixtures:
            fecha_entera = fixture['fixture']['date']
            fecha = fecha_entera.split("T")[0]
            local = fixture['teams']['home']['name']
            visitante = fixture['teams']['away']['name']

            print(f"Fecha {x_op}: el {fecha} juegan -> {local} (L) vs {visitante}(V)")

            dict_fechas[fixture['fixture']['id']] = {'fecha': fecha, 'local': local, 'visitante': visitante}
            locales[local] = fixture['teams']['home']['id']
            visitantes[visitante] = fixture['teams']['away']['id']
            # dict_fechas[fixture['fixture']['id']] = [locales[local], visitantes[visitante]]
            id_fecha[(locales[local], visitantes[visitante])] = fixture['fixture']['id']
            x_op_l_v[x_op]= (locales[local], visitantes[visitante])

            x_op+=1
    else:
        print("Error al traer los datos")

    return dict_fechas, locales, visitantes,id_fecha, x_op_l_v


def mostrar_teams()->dict:
    
    equipos_dict,equipos_id = equipos_liga_2023()
    opcion_equipos = {}
    x = 1

    for i in equipos_id:
            print(f"{x}--{equipos_id[i]}--")
            opcion_equipos[x] = equipos_id[i]
            x+=1

    return opcion_equipos, equipos_dict

#validacion fecha --> usuario ingresa fecha y se corrobora que este en el formato correcto
def validacion_fecha (fecha:str) -> bool:
    fecha_valida = False
    while not fecha_valida:
        if re.match (r"\d{4}/\d{2}/\d{2}", fecha):
            fecha_valida = True
        else:
            fecha_valida = False
    return fecha_valida

def registrar_transacciones_usuarios (mail_usuario:str,fecha_actual:str, resultado: str, importe: int) -> dict:
    #mismo planteo e idea que el archivo usuarios

    transacciones_usuarios = {}
    archivo_transacciones = 'transacciones.csv'
    
    if  os.path.isfile(archivo_transacciones):
        with open(archivo_transacciones, 'r', newline='', encoding="UTF-8") as archivo_csv:
            csv_reader = csv.reader(archivo_csv, delimiter = ',')
            next (csv_reader) 
            for row in csv_reader:
                mail = row[0]
                transacciones_usuarios[mail] = {"fecha": row [1], "resultado": row [2], "importe": row[3]}


    transacciones_usuarios [mail] = {"fecha" : fecha_actual, "resultado": resultado, "importe" : importe}  #defino diccionario 
    
    with open("transacciones.csv", "w", newline= '', encoding="UTF-8") as archivo_csv: #aclaro con un 'w' que es un archivo de escritura
        
        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["mail","fecha","resultado","importe"]) #---> escribir encabezado
        for mail_usuario, data in transacciones_usuarios.items():
            csv_writer.writerow([mail_usuario, data["fecha"],data["resultado"], data["importe"]])

def validar_dinero_cuenta_usuario (mail: str, importe: float):
    #PRE: verifico dinero disponible usuario
    #POST: devuelve un booleano (si dinero en cuenta menor importe ---> dinero_insuficiente = FALSE)
    
    archivo_csv_users = 'data_users.csv'
    users = {}
    if os.path.isfile(archivo_csv_users):
       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'money': row[5]}
    
    dinero_insuficiente = False 

    if mail in users:
        dinero_cuenta = users[mail]['money']
        if dinero_cuenta < importe:
            dinero_insuficiente = True
    return dinero_insuficiente

def modificar_dinero_cuenta_usuario (mail:  str , dinero : float, fecha: str, restar: bool = False) -> None:
     #PRE: modifico dinero en cuenta usuario 
     #POST: obtengo archivo actualizado 
    
    filas_actualizadas  = []
    archivo_csv_users = 'data_users.csv'
    
    if os.path.isfile(archivo_csv_users):
       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)
           rows = list(csv_reader)
           usuario_modificar = mail
           for row in rows:
               if row[0] == usuario_modificar:
                    row [4] = fecha 
                    if dinero!='':
                        if restar:
                            row[5] = float (row[5]) - float(dinero)
                        else:
                            row[5] = float (row[5]) + float(dinero)
                    elif dinero== '':
                        if restar:
                            row[5] = float(row[5])
                        else:
                            row[5] = float(row[5])
               filas_actualizadas.append(row)
               
           with open('data_users.csv', 'w', newline='', encoding='UTF-8') as archivo_csv: 
               csv_writer = csv.writer(archivo_csv)
               csv_writer. writerows (filas_actualizadas)



def registrar_plata_apostada_usuario (mail:  str , apuesta: float, fecha: str):
     archivo_csv_users = 'data_users.csv'
     filas_actualizadas  = []
     if os.path.isfile(archivo_csv_users):
       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)
           rows = list(csv_reader)
           usuario_modificar = mail
           for row in rows:
               if row[0] == usuario_modificar:
                   row [3] = apuesta
                   row[4] = fecha
               
               filas_actualizadas.append(row)

           with open('data_users.csv', 'w', newline='', encoding='UTF-8') as archivo_csv: 
               csv_writer = csv.writer(archivo_csv)
               csv_writer. writerows (filas_actualizadas)



def win_or_draw_f(id_partido:int)->int:
    #PRE: busco datos api sobre las predcciones partidos de la liga
    #POST: devuelve win_or_draw (booleano)

    url = "https://v3.football.api-sports.io"

    parameters = {"fixture":id_partido}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

    respuesta = requests.get(url, params = parameters, headers = headers)

    predictions = {}
    if respuesta.status_code == 200:
        data = respuesta.json()
        predictions = data['response'][0]

        win_or_draw = predictions['predictions']['winner']['id'] #id del equipo en el que el winordraw esta true

    return win_or_draw


def apuesta(mail:str)->None:

    print("Estos son los equipos que estan participando del torneo 2023")
     
    equipos_enumerados, dict_equipos =mostrar_teams()
    
    equipos_dict,equipos_id = equipos_liga_2023()

    equipo_op = int(input("Elija por cual equipo desea apostar: "))
    while(equipo_op not in equipos_enumerados.keys()):
        print("Opcion incorrecta, intente de nuevo")
        equipos_enumerados, dict_equipos =mostrar_teams()
        equipo_op = int(input("Escriba por el equipo que desea apostar: "))

    id_equipo = equipos_dict[equipos_enumerados[equipo_op]]

    #pide fecha usuario y evaulua qwue coincida con id del partido
    dict_fechas, dict_locales, dict_visitantes, ids_fechas, dicc_lv_idfecha = fechas_teams(id_equipo)
    fecha_elegida = int(input("Ingrese la fecha por la que desea apostar(ingrese numero que tiene al lado): "))
    
    while(fecha_elegida not in dicc_lv_idfecha.keys()):
        print("Opcion invalida, intente de nuevo.")
        dict_fechas, dict_locales, dict_visitantes, ids_fechas, dicc_lv_idfecha = fechas_teams(id_equipo)
        fecha_elegida = int(input("Ingrese la fecha por la que desea apostar(ingrese numero que tiene al lado): "))
    
    id_partido = ids_fechas[dicc_lv_idfecha[fecha_elegida]]
    
    local = equipos_dict[dict_fechas[id_partido]['local']]
    visitante = equipos_dict[dict_fechas[id_partido]['visitante']]

    apuesta = int(input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local \n 2-Empatan\n 3-Gana Visitate"))
    while(apuesta not in (1,2,3)):
        print("Opcion invalida, intente de nuevo.")
        apuesta = input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local \n 2-Empatan\n 3-Gana Visitate")
    fecha = input("Ingrese la fecha de hoy( asi YYYY/MM/DD): ")
    while(validacion_fecha(fecha)==False):
        print("Fecha incorrecta, intente de nuevo")
        fecha = input("Ingrese la fecha de hoy( asi YYYY/MM/DD): ")
    
    casos = {1:"gana local",2:"empatan",3:"gana visitante"}

    print(f"Usted a decidido apostar que {equipos_id[local]}vs{equipos_id[visitante]}, {casos[apuesta]} en la fecha {fecha_elegida}")

    dado_resultado:int = random.randrange(1,4)#para definir si gana L/V o empatan
    cant_q_se_paga:int = random.randrange(1,5)#cuanto se le paga al ganador respecto a lo apostado
    
    plata_apostada:float = input("Ingrese monto de dinero que desea apostar: ")

    dinero_insuficiente = validar_dinero_cuenta_usuario (mail, plata_apostada)
    if dinero_insuficiente == False:
        registrar_plata_apostada_usuario(mail, plata_apostada, fecha)


    id_win_or_draw = win_or_draw_f(id_partido) #win_or_draw=true para el id del equipo que devuelve

    if dado_resultado==apuesta:

        print("Ha ganado la apuesta!")
        if dado_resultado==1 and id_win_or_draw == local:#aposto al local y tiene true el w_o_d
            pago = plata_apostada*(cant_q_se_paga/10)
        elif dado_resultado==1 and id_win_or_draw!=local:#aposto al local pero estaba False para local
            pago = plata_apostada*(cant_q_se_paga)
        elif dado_resultado==2:#aposto a que empataban, gano tarifa de empate
            pago = plata_apostada*(0.5)
        elif dado_resultado==3 and id_win_or_draw == visitante:#aposto a visitante y el true estaba para visitante
            pago = plata_apostada*(cant_q_se_paga/10)
        elif dado_resultado==3 and id_win_or_draw!=visitante:#aposto al visitante pero estaba False para visitante
            pago = plata_apostada*(cant_q_se_paga)

        print(f"Dinero ganado: {pago}")

        bet = "+" #como resulto la apuesta 

        # sumarle lo que gano a la plata que ya tenia 
        pago = float(pago)
        registrar_transacciones_usuarios (mail,fecha, "Gana", " (+)", pago)
        modificar_dinero_cuenta_usuario (mail, pago, fecha)
    else: 
        print("Lo sentimos, usted a perdido la apuesta")
        bet = "-"#como resulto la apuesta 
        # descontarle lo que apostp de la cuenta 

        registrar_transacciones_usuarios (mail,fecha, "pierde", " (-)", plata_apostada)
        modificar_dinero_cuenta_usuario (mail , float(plata_apostada), fecha, restar = True)
     


def usuario_mas_aposto(mail: str, users: dict, apuesta: float) :
    maximo_apostador = {}
    users = {} 
    archivo_csv_users = 'data_users.csv'
    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users
       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'bets':row[3]}

       if mail in users:
           users[mail]["bets"] = apuesta
           for apostador, datos in users.items():
                if apostador not in maximo_apostador or datos ["bets"] > maximo_apostador[apostador]:
                 maximo_apostador [apostador] = datos["bets"]
                 
    importes_ordenados = sorted(maximo_apostador.values (), reverse = True)           #----> ordenar descendente (reverse = True)
    importe_maximo_valor = importes_ordenados [0]


    print(f"Los apuestas fueron {importes_ordenados}, el usuario, {mail}, fue quien mas aposto con un total de {importe_maximo_valor} ")
    
    
    #ususario mas veces gano

def usuario_mas_veces_gano (transacciones_usuarios: dict, mail: str)-> None:
    maximo_ganador = {}
    transacciones_usuarios = {}

    nombre_archivo_transacciones= "transacciones.csv"
    if  os.path.isfile (nombre_archivo_transacciones):
            with open ("transacciones.csv", newline='', encoding="UTF-8") as archivo_csv:
                csv_reader = csv.reader (archivo_csv, delimiter = ",")
                next (csv_reader) 
                for row in csv_reader:
                    mail = row[0]
                    transacciones_usuarios[mail] = {"fecha": row [1], "resultado": row [2], "importe": row[3]}
    
    for transaccion in transacciones_usuarios.values():
        if transaccion["resultado"] == "gana":
            mail = transaccion[mail]
            if mail not in maximo_ganador:
                maximo_ganador[mail] = 1
            else:
                maximo_ganador[mail] += 1

    victorias = sorted(maximo_ganador.values (), reverse = True) 
    if len(victorias) == 0:
        print("Todavia no hay valores para analizar") 
    else:    
        max_victoria = victorias [0]
        print(f"El usuario, {mail}, fue el ganador con {max_victoria} victorias")
        

def main()->None:
    fin = False

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
            op = input("Desea acceder a la plataforma? y/n:")
            print("Jugatela: plataforma de apuestas.\nEsta plataforma requiere tener un usuario, elija segun el caso:")
            usuario = input("a-Iniciar sesion:\n b-Crearse una cuenta:\n")

        elif usuario.lower()=="a":
            mail = input("Correo electronico: ")
            password = input("Contraseña: ") 
            users = inicio_sesion()
            while(validar_mail_2(mail,password,users)==False):
                print("Mail incorrecto. Si usted ya posee una cuenta, ingrese correctamente el mail")
                mail = input("Correo electronico: ")
                password =input("Contraseña: ")
                users = inicio_sesion()
  
        while not fin :
            imprimir_opciones()
            opcion_elegida = int(input ("Seleccione una opcion del menu: "))
            if opcion_elegida != 9 :
                opcion_seleccionada(opcion_elegida,mail)#, equipos_2023, jugadores_2023
            else:
                fin = True
                print("¡Gracias por su vista! Dejanos una opinion: ")
                opinion = input ("Opinion:")

    
 

main()

"""equipos_2023 = equipos_liga_2023_2()
   jugadores_2023 = jugadores_equipos ()
        mostrar_tabla_posiciones(2022)
        apuesta()"""

#idea original de apuestas que no funcionaba
    
    # print("Estos son los equipos que estan participando del torneo 2023")
     
    # mostrar_teams()
    
    # equipos_dict,equipos_id = equipos_liga_2023()

    # equipo_op = input("Elija por cual equipo desea apostar: ")
    # while(equipo_op not in equipos_id.values()):
    #     print("Opcion incorrecta, intente de nuevo")
    #     equipo_op = input("Escriba por el equipo que desea apostar: ")

    # id_equipo = equipos_dict[equipo_op]

    # #funcion de buscar fechas
    # dict_fechas,dict_locales,dict_visitantes,ids_fechas = fechas_teams(id_equipo)
    # fecha_elegida:int = input("Ingrese el num de fecha por el que desea apostar: ")

    # while(fecha_elegida not in dict_fechas.keys()):
    #     print("Fecha inexistente, intentelo de nuevo")
    #     dict_fechas,dict_locales,dict_visitantes = fechas_teams(id_equipo)
    #     fecha_elegida:int = input("Ingrese el num de fecha por el que desea apostar: ")

    # partido:list = dict_fechas[fecha_elegida]

    # id_partido:int = ids_fechas[partido]
    # apuesta:int = input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local \n 2-Empatan\n 3-Gana Visitate")
    # while(apuesta not in (1,2,3)):
    #     print("Opcion invalida, intente de nuevo.")
    #     apuesta = input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local \n 2-Empatan\n 3-Gana Visitate")

    # casos = {1:"gana local",2:"empatan",3:"gana visitante"}

    # print(f"Usted a decidido apostar que {partido[0]}vs{partido[1]}, {casos[apuesta]} en la fecha {fecha_elegida}")

    # dado_resultado:int = random.randrange(1,4)#para definir si gana L/V o empatan
    # cant_q_se_paga:int = random.randrange(1,5)#cuanto se le paga al ganador respecto a lo apostado
    
    # plata_apostada:float = input("Ingrese monto de dinero que desea apostar: ")
    # id_usuario = input("MAIL: ")
    # dinero_insuficiente = validar_dinero_cuenta_usuario (id_usuario, plata_apostada)
    # if dinero_insuficiente == False:
    #     fecha = validacion_fecha ()
    #     registrar_plata_apostada_usuario (id_usuario, plata_apostada, fecha)


    # local = dict_locales[dict_fechas[fecha_elegida][0]]
    # visitante = dict_visitantes[dict_fechas[fecha_elegida][1]]

    # id_win_or_draw = win_or_draw_f(id_partido) #win_or_draw=true para el id del equipo que devuelve

    # if dado_resultado==apuesta:

    #     print("Ha ganado la apuesta!")
    #     if dado_resultado==1 and id_win_or_draw == local:#aposto al local y tiene true el w_o_d
    #         pago = plata_apostada*(cant_q_se_paga/10)
    #     elif dado_resultado==1 and id_win_or_draw!=local:#aposto al local pero estaba False para local
    #         pago = plata_apostada*(cant_q_se_paga)
    #     elif dado_resultado==2:#aposto a que empataban, gano tarifa de empate
    #         pago = plata_apostada*(0.5)
    #     elif dado_resultado==3 and id_win_or_draw == visitante:#aposto a visitante y el true estaba para visitante
    #         pago = plata_apostada*(cant_q_se_paga/10)
    #     elif dado_resultado==3 and id_win_or_draw!=visitante:#aposto al visitante pero estaba False para visitante
    #         pago = plata_apostada*(cant_q_se_paga)

    #     print(f"Dinero ganado: {pago}")

    #     bet = "+" #como resulto la apuesta 

    #     # sumarle lo que gano a la plata que ya tenia 
    #     pago = float(pago)
    #     registrar_transacciones_usuarios (id_usuario,fecha, "Gana", " (+)", pago)
    #     modificar_dinero_cuenta_usuario (id_usuario , pago, fecha)
    # else: 
    #     print("Lo sentimos, usted a perdido la apuesta")
    #     bet = "-"#como resulto la apuesta 
    #     # descontarle lo que apostp de la cuenta 

    # registrar_transacciones_usuarios (id_usuario,fecha, "pierde", " (-)", plata_apostada)
    # modificar_dinero_cuenta_usuario (id_usuario , float(-plata_apostada), fecha)

#base dict de fechas
    # def fechas_teams(id_team:int)->dict:
#     #PRE: datos api de los partidos a jugar
#     #POST: devuelve 3 dicts con fechas, equipos localaes y equipos visitantes
#     url = "https://v3.football.api-sports.io/fixtures?"

#     parameters = {"league": "128","season": 2023,"team":id_team}

#     headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "a991e40daffd726206f67b1a40947c67" }

#     respuesta = requests.get(url, params = parameters, headers = headers)
#     fechas = {}
#     locales = {}
#     visitantes = {}
#     id_fecha = {}
#     if respuesta.status_code == 200:
#         data = respuesta.json()
#         fechas = data['response']
#         print(f"Fechas de Temporada 2023 ( se lee asi Local vs Visitante):")

#         for fecha in range(len(fechas[0]['fixture'])):
#             locales[fechas[0]['fixture']['teams']['home']['name']]= fechas[0]['fixture']['teams']['home']['id']
#             visitantes[fechas[0]['fixture']['teams']['away']['name']] = fechas[0]['fixture']['teams']['away']['id'] 
#             fechas[fecha] = [fechas[0]['fixture']['teams']['home']['name'],fechas[0]['fixture']['teams']['away']['name']]     
#             id_fecha[fechas[0]['fixture']['teams']['home']['name'],fechas[0]['fixture']['teams']['away']['name']] = fechas[0]['fixture']['id']  
        
#         for i in (fechas):
#             print(f"Fecha {i+1}: {fechas[i][0]} vs {fechas[i][1]}")

#     else: print("Error al traer los datos")

#     return fechas,locales,visitantes,id_fecha