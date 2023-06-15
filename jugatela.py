import os
import requests
from passlib.hash import sha256_crypt
import csv
import random
import matplotlib.pyplot as plt 
#permitir ingreso usuario y demas

def validar_mail(mail:str)->bool:
    
    pass

def user_registration()->str:
    #PRECONDICIONES: UN NUEVO USER QUIERE GENERAR UNA CUENTA 
    #POSTCONDICIONES: MAIL QUE DEBE SER UNICO
    #pido datos al user
    print("Ingrese los siguientes datos, como se detalle a continucion: ")
    mail = input("Correo electronico: ")
    """while(validar_mail(mail)==False):
        print("El correo electronico ingresado ya se encuentra en uso.")
        print("Ingrese otro.")
        mail = input("Correo electronico: ")"""
    name = input("Nombre Usuario: ")
    password = sha256_crypt.hash(input("Contraseña: "))
    money = float(input("Dinero inicial que desea ingresar: "))

    #desp de pedir la data del user nuevo, procede subir esta data
    #primero llamo a la funcion que me permite leer el archivo donde esta la data de los users
    users = archivo_csv_r_data_users()

    #las bets estan como 0 ya que es la primera vez que se registra, lo mismo para la fecha de apuesta(esta en none porqe todavia nunca aposta)
    users[mail]={'name':name,'password':password,'bets':0,'date':None,'money':money}

    #por ultimo se agrega este nuevo user al archivo
    archivo_csv_a_data_users(users)
    print(f"El usuario {name} ligado al correo electronico {mail} se ha registrado con exito.")

    return mail


def archivo_csv_r_data_users()->dict:

    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'

    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'name':row[1],'password':row[2],'bets':row[3],'date':row[4],'money': row[5]}
    return users

def archivo_csv_a_data_users(users:dict)->None:

    with open('data_users.csv', 'a', newline='', encoding='UTF-8') as archivo_csv: #aclaro con un 'w' que es un archivo de escritura

        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        
        for mail, data in users.items():
            csv_writer.writerow([mail,data['name'],data['password'],data['bets'],data['date'],data['money']])


def main()->None:

    print("Bienvenido a la mejor plataforma de apuestas futboleras")

    banana = user_registration()
    
    """banana = archivo_csv_r_data_users()"""

    

    """archivo_csv_a_data_users(banana)"""
    
main()