import os
import requests
from passlib.hash import sha256_crypt
import csv
import random
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np 
from PIL import Image

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

def imprimir_opciones()->None:

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

def opcion_seleccionada (opcion_elegida:int, equipos_2023:dict, jugadores_2023:dict):   #agregar mas parametros si es necesario 
    
    equipos_dict,equipos_id = equipos_liga_2023()

    if opcion_elegida == 1:#finished
        print("--- Equipos de la Liga Profesional Temporada 2023---")
        equipos_2023 = equipos_liga_2023 ()
        listar_equipos_2023 (equipos_2023)
        id_equipo_usuario = None # Valor predeterminado
        while id_equipo_usuario is None:
            equipo_usuario = input("Seleccione equipo: ").capitalize()
            id_equipo_usuario = buscar_id_equipo(equipos_2023, equipo_usuario)
            jugadores_2023 = jugadores_equipos()
            plantel_2023(id_equipo_usuario, jugadores_2023)

    elif opcion_elegida == 2:#finished
        print("---Tabla de posiciones de la Liga profesional---")
        temps = [2015,2016,2017,2018,2019,2020,2021,2022]
        print("Temporadas (años):")
        for i in range (len(temps)):
            print(f"{i+1}-{temps[i]}")
        temporada = input("Ingrese una de las temporadas en pantalla(oprima el numero que tiene al comienzo): ")
        while(temporada not in (1,2,3,4,5,6,7,8)):
            print("Opcion incorrecta, intente de nuevo")
            print("Temporadas (años):")
            for i in range (len(temps)):
                print(f"{i+1}-{temps[i]}")
            temporada = input("Ingrese una de las temporadas en pantalla(oprima el numero que tiene al comienzo): ")
        
        mostrar_tabla_posiciones(temps[temporada])

    elif opcion_elegida == 3:#finished
        print ("--- Escudos y Estadios ---")
        mostrar_teams()
        equipo_seleccionado=input("Seleccione equipo dentro del listado:")
        iddelequipo = equipos_dict[equipo_seleccionado]
        escudo_cancha(iddelequipo)

    elif opcion_elegida == 4:#finished
        print ("--- Grafico goles y minutos ---")
        mostrar_teams()
        equipo_seleccionado:str =input("Seleccione equipo dentro del listado:")
        while(equipo_seleccionado not in equipos_id.values()):
            print("Opcion invalida, intente de nuevo.")
            equipo_seleccionado:str =input("Seleccione equipo dentro del listado:")
        grafico(equipo_seleccionado) 

    elif opcion_elegida == 5:
        print ("--- Cargar dinero a cuenta ---")
        id_usuario = input ("MAIL: ")
        cargar_dinero_cuenta_usuario (id_usuario, "","")
    
    elif opcion_elegida == 6:
        print ("--- Usuario que más dinero apostó ---")
        #usuario_mas_aposto () 
        #basarme transacciones.csv

    elif opcion_elegida == 7:
        print ("--- Usuario que más veces gano ---")
        #usuario_ganador ()
        #registo en transacciones.csv / data_users.csv

    elif opcion_elegida == 8:
        print("--- APUESTAS ---")
        apuesta()
        #registro si gana/deposita (+), si pierde (-) en transacciones
        #voy al data.csv al final para sumar o restar el dinero, ya con resultado de la apuesta

    else:
        print("Intente seleccionar una opcion del menu.")
        opcion_seleccionada(opcion_elegida,equipos_2023, jugadores_2023 )
    
def plantel_2023(id_equipo:int, jugadores_2023:dict):
    for jugador in jugadores_2023:
        equipo = equipos_liga_2023()
        id_equipo = equipo['team']['id']
        print(f"\nPlantel de {equipo['team']['name']}:")
        if jugador['statistics'][0]['team']['id'] == id_equipo:
            print(jugador['player']['name'])

def equipos_liga_2023_2 () -> dict:
    url = "https://v3.football.api-sports.io/teams"
    
    parameters = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

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
    url = "https://v3.football.api-sports.io/players"
    parameters ={"league": "128", "season": 2023}
    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "407726f0daca539a383c3c8ca8e4ca93"}
    respuesta = requests.get (url, params = parameters, headers = headers)
    jugadores_2023 = {}
    if respuesta.status_code == 200:
        data = respuesta.json ()
        jugadores_2023 = data ["response"]
    else:
        print("Err", respuesta.status_code)

    return jugadores_2023

def listar_equipos_2023 (equipos_2023:dict) -> None:  
    for i in range (1, 29):       #enumerar los equipos, y los muestro por consola 
        for  equipo in  equipos_2023:
            nombre_equipo = equipo["team"]["name"]
            print(f"{i}. {nombre_equipo}")

def buscar_id_equipo(equipos_2023:dict, equipo_usuario:str) -> None:   #obtnego id del equipo que pide usuario y lo verifico
    id_equipo_usuario = None
    for equipo in equipos_2023:
        if equipo_usuario == equipo["team"]["name"]:
            id_equipo_usuario = equipo["team"]["id"]
    return id_equipo_usuario 

def mostrar_tabla_posiciones(temporada:int)->None:
    url = "https://v3.football.api-sports.io/standings"
    
    params = {"league": "128","season": temporada}
    
    headers = {'x-rapidapi-host': "v3.football.api-sports.io",'x-rapidapi-key': "6560a6c96c1a8e1c14463129104c7c84"}
    
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

def cargar_dinero_cuenta_usuario(id_usuario, dinero, fecha): 
    
    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'
   
    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'money': row[5]}

    if id_usuario  in users[mail]:
        dinero = input ("Dinero a cargar: ")
        dinero = float(dinero)
        dinero_en_cuenta = users[mail]['money'] 
        users[mail]["money"] = dinero_en_cuenta + dinero
    else:
        print("Mail invalido")

    print (f"Ahora posee {users[mail]['money']} disponible en su cuenta. ")
    
    #actualizar_dinero_en_cuenta() #actauliza csv usuarios con deposito (carga de dinero)
    #registrar_nueva_transaccion() #en desarollo

def equipos_liga_2023 () -> dict:
    url = "https://v3.football.api-sports.io/teams"
    parameters = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

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

    url = "https://v3.football.api-sports.io/teams?"
    parameters = {"id": "434","country": "Argentina","league": "128","season": "2023"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io","x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

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

def grafico(equipo:str)->None:

    dicts_equipos = equipos_liga_2023()

    id_equipo = dicts_equipos[equipo]

    url = "https://v3.football.api-sports.io/teams/statistics?"

    parameters = {"league": "128","season": 2023,"team":id_equipo}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

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
            goles.append(dict_info['goals']['for']['minute '][minutos]['total'])
            golesxminuto[minutos] = dict_info['goals']['for']['minute'][minutos]['total']
        

        for y in range(len(goles)):
            if goles[y]==None: goles[y]=0
            else:continue 

        plt.bar(mins,goles)
        plt.title("Goles por minuto")
        plt.xlabel("Intervalos de minutos")
        plt.ylabel("cant. goles")
        plt.show()

def fechas_teams(id_team:int)->dict:
    
    url = "https://v3.football.api-sports.io/fixtures?"

    parameters = {"league": "128","season": 2023,"team":id_team}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    fechas = {}
    locales = {}
    visitantes = {}
    id_fecha = {}
    if respuesta.status_code == 200:
        data = respuesta.json()
        fechas = data['response']
        print(f"Fechas de Temporada 2023 ( se lee asi Local vs Visitante):")

        for fecha in range(len(fechas[0]['fixture'])):
            locales[fechas[0]['fixture']['teams']['home']['name']]= fechas[0]['fixture']['teams']['home']['id']
            visitantes[fechas[0]['fixture']['teams']['away']['name']] = fechas[0]['fixture']['teams']['away']['id'] 
            fechas[fecha] = [locales[fechas[0]['fixture']['teams']['home']['name']],visitantes[fechas[0]['fixture']['teams']['away']['name']]]     
            id_fecha[[locales[fechas[0]['fixture']['teams']['home']['name']],visitantes[fechas[0]['fixture']['teams']['away']['name']]]] = fechas[0]['fixture']['id']  
        
        for i in (fechas):
            print(f"Fecha {i+1}: {fechas[i][0]} vs {fechas[i][1]}")

    else: print("Error al traer los datos")

    return fechas,locales,visitantes,id_fecha

def mostrar_teams()->None:
    equipos_dict,equipos_id = equipos_liga_2023()

    for i in equipos_id:
            print(f"--{equipos_id[i]}--")


#no muy segura validar las fechas asi
# def validacion_fecha ():
#     fecha_valida = False
#     while not fecha_valida:
#         fecha_actual = input ("Ingrese fecha en formato YYYY/MM/DD: ")
#         if re.match (r"\d{4}/\d{2}/\d{2}", fecha_actual):
#             fecha_valida = True
#         else:
#             print("Por favor ingrese la fecha en el formato dado (YYYY/MM/DD)")
#             fecha_actual = input ("Ingrese fecha en formato YYYY/MM/DD: ")
#     return fecha_actual

def archivo_transacciones_usuarios (id_usuario:str,fecha_actual:str, resultado: str, importe: int) -> dict:
    #mismo planteo e idea que el archivo usuarios
    transacciones_usuarios = {}
    nombre_archivo_transacciones= "transacciones.csv"
    if  os.path.isfile (nombre_archivo_transacciones):
        with open ("transacciones.csv", newline='', encoding="UTF-8") as archivo_csv:
            csv_reader = csv.reader (archivo_csv, delimiter = ",")
            next (csv_reader) 
            for row in csv_reader:
                mail = row[0]
                transacciones_usuarios[mail] = {"fecha": row [1], "resultado": row [2], "importe": row[3]}


    transacciones_usuarios [id_usuario] = {"fecha" : fecha_actual, "resultado": resultado, "importe" : importe}  #defino diccionario 
    
    with open("transacciones.csv", "w", newline= '', encoding="UTF-8") as archivo_csv: #aclaro con un 'w' que es un archivo de escritura
        
        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["mail","fecha","resultado","importe"]) #---> escribir encabezado
        for mail, data in transacciones_usuarios.items():
            csv_writer.writerow({"mail": mail, "fecha": data["fecha"],"resultado": data["resultado"], "importe":data["importe"]})

def win_or_draw_f(id_partido:int)->int:

    url = "https://v3.football.api-sports.io"

    parameters = {"fixture":id_partido}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)

    if respuesta.status_code == 200:
        data = respuesta.json()
        predictions = data['response']

        id_equipo_true = predictions['winner']['id']

        win_or_draw = id_equipo_true

    return win_or_draw



def win_or_draw_f(id_partido:int)->int:

    url = "https://v3.football.api-sports.io"

    parameters = {"fixture":id_partido}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)

    if respuesta.status_code == 200:
        data = respuesta.json()
        predictions = data['response']

        id_equipo_true = predictions['winner']['id']

        win_or_draw = id_equipo_true

    return win_or_draw



def apuesta()->None:
    
    print("Estos son los equipos que estan participando del torneo 2023")
    listar_equipos_2023(equipos_liga_2023_2())
     
    mostrar_teams()
    
    equipos_dict,equipos_id = equipos_liga_2023()

    equipo_op = input("Elija por cual equipo desea apostar: ")
    while(equipo_op not in equipos_dict.values()):
        print("Opcion incorrecta, intente de nuevo")
        equipo_op = input("Escriba por el equipo que desea apostar: ")

    id_equipo = equipos_dict[equipo_op]

    #funcion de buscar fechas
    dict_fechas,dict_locales,dict_visitantes,ids_fechas = fechas_teams(id_equipo)
    fecha_elegida:int = input("Ingrese el num de fecha por el que desea apostar: ")

    while(fecha_elegida not in dict_fechas.keys()):
        print("Fecha inexistente, intentelo de nuevo")
        dict_fechas,dict_locales,dict_visitantes = fechas_teams(id_equipo)
        fecha_elegida:int = input("Ingrese el num de fecha por el que desea apostar: ")

    partido:list = dict_fechas[fecha_elegida]

    id_partido:int = ids_fechas[partido]

    apuesta:int = input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local/Visitante \n 2-Empatan\n ")
    while(apuesta not in (1,2,3)):
        print("Opcion invalida, intente de nuevo.")
        apuesta = input("Ingrese el numero correspondiente al tipo de apuesta: \n 1- Gana Local \n 2-Empatan\n 3-Gana Visitate")

    casos = {1:"gana local",2:"empatan",3:"gana visitante"}

    print(f"Usted a decidido apostar que {partido[0]}vs{partido[1]}, {casos[apuesta]} en la fecha {fecha_elegida}")

    dado_resultado:int = random.randrange(1,4)#para definir si gana L/V o empatan
    cant_q_se_paga:int = random.randrange(1,5)#cuanto se le paga al ganador respecto a lo apostado
    plata_apostada:float = input("Ingrese monto de dinero que desea apostar")

    local = dict_locales[dict_fechas[fecha_elegida][0]]
    visitante = dict_locales[dict_fechas[fecha_elegida][1]]

    id_win_or_draw = win_or_draw_f(id_partido) #win_or_draw=true para el id del equipo que devuelve



    if dado_resultado==apuesta:

        print("Ha ganado la apuesta!")
        if dado_resultado==1 and id_win_or_draw == local:#aposto al local y tiene true el w_o_d
            pago = plata_apostada*(cant_q_se_paga)
        elif dado_resultado==1 and id_win_or_draw!=local:#aposoto al local pero estaba False para local
            pago = plata_apostada*(cant_q_se_paga/10)
        elif dado_resultado==2:#aposto a que empataban, gano tarifa de empate
            pago = plata_apostada*(0.5)
        elif dado_resultado==3 and id_win_or_draw == visitante:#aposto a visitante y el true estaba para visitante
            pago = plata_apostada*(cant_q_se_paga)
        elif dado_resultado==3 and id_win_or_draw!=visitante:#aposto al visitante pero estaba False para visitante
            pago = plata_apostada*(cant_q_se_paga/10)

        print(f"Dinero ganado: {pago}")

        bet = "+" #como resulto la apuesta 

        #aca habria que sumarle lo que gano a la plata que ya tenia 

    else: 
        print("Lo sentimos, usted a perdido la apuesta")
        bet = "-"#como resulto la apuesta 
        #aca habria que descontarle lo que apostp de la cuenta 
        
    #falta verificar que el usuario tenga la plata en cuenta para apostar la cant que este apostando 
    #falta la parte de transacciones aca, tamb la de user_data(o sea agregar a la parte de bets lo que resulto de la variable bet y agregar la plata ganada o perdida a la cuenta)

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

        jugar = input ("Desea ver nuestras actuvidades disponibles? (y/n): ").lower()

        while jugar != "n":
            equipos_2023 = equipos_liga_2023()
            jugadores_2023 = jugadores_equipos ()
            imprimir_opciones()
            opcion_elegida = input ("Seleccione una opcion del menu: ")
            opcion_elegida = int(opcion_elegida)
            if opcion_elegida != 9  or  opcion_elegida != 0:
                opcion_seleccionada(opcion_elegida, equipos_2023, jugadores_2023)   
            else:
                print("¡Gracias por su vista! Dejanos una opinion: ")
                opinion = input ()
        if jugar == "n":
            print("¡Gracias por su vista! Dejanos una opinion: ")
            opinion = input ()


main()