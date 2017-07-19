# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:38:20 2017

@author: pi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:56:37 2017

@author: Gloria
"""
import telebot # Importamos las libreria
import threading
from telebot import types
from picamera import PiCamera
from time import sleep
import time
from sense_hat import SenseHat
import datetime

#Definición de variables globales
global flag
global block

#Esta bandera evita que pregunte continuamente por las altas temperaturas hasta que no se reciban respuestas
flag=0

TOKEN = '294193814:AAHeD6CYOKVR1z_oApwH4_fhxQ7sExWo94s'
chat_gloria = "385937705" 
#La identificacion de mi chat para enviar mensajes


#message = input("Que mensaje quiere enviar? ")
#Activamos la comunicaion con el bot de telegram
tb = telebot.TeleBot(TOKEN)
#Ventana de opciones cuando salta la alarma de incendios
markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Llamar a bomberos')
itembtn2 = types.KeyboardButton('Falsa alarma')
markup.add(itembtn1, itembtn2)
#Ventana de opciones inicial
markup2 = types.ReplyKeyboardMarkup(row_width=2)
itembtn3 = types.KeyboardButton('Comprobar seguridad')
itembtn4 = types.KeyboardButton('Programacion de lavado')
markup2.add(itembtn3, itembtn4)

hideBoard=types.ReplyKeyboardRemove(selective=False)

sense=SenseHat()

#Variable bandera que se activa cuando se espere la hora de programacion de la lavadora
block=0

def hacer_foto():
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.rotation = 180
    camera.start_preview(fullscreen=False, window=(30,30,320,240))
    for i in range(0,2):
        sleep(1)
    camera.capture('/home/pi/imagen.jpg')
    camera.stop_preview()
    camera.close()

    photo = open('/home/pi/imagen.jpg', 'rb')
    return photo
    
#La rutina que comprueba la temperatura de los sensores
def worker():
    global flag
    while 1:
        Temp1=round(sense.get_temperature_from_humidity(),2)
        Temp2=round(sense.get_temperature_from_pressure(),2)
        print("Temperaturas: %2.3f %2.3f" % (Temp1,Temp2))
        if flag == 0 and Temp1 > 38:
            photo = hacer_foto()
            tb.send_photo(chat_gloria, photo, "Temperatura muy alta: " + str(Temp1))
            tb.send_message(chat_gloria, "Que prefieres hacer?:", reply_markup=markup)
            flag = 1
        sleep(5)

t = threading.Thread(target=worker)
t.setDaemon(True)
t.start()


def visor(message):
    global flag
    global block
    ret = False
    if message.text == "Llamar a bomberos":
        ret = True
        tb.send_message(chat_gloria, "Llamando bomberos...",reply_markup=hideBoard)
        flag = 0

    elif message.text == "Falsa alarma":
        ret = True
        tb.send_message(chat_gloria, "Alarma desactivada",reply_markup=hideBoard)
        flag = 0

    elif message.text == "Comprobar seguridad":
        ret = True
        photo = hacer_foto()
        tb.send_photo(chat_gloria,photo, "Foto tomada:\n"+ datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), reply_markup=hideBoard)
        flag = 0

    elif message.text == "Programacion de lavado":
        ret = True
        tb.send_message(chat_gloria, "Introduzca hora de finalizacion del lavado",reply_markup=hideBoard )
        block=1
        
    return ret

def finlavado():
    global block
    tb.send_message(chat_gloria, "Lavadora finalizada a las "+ datetime.datetime.now().strftime("%H:%M"))
    t.join()
    block=0

@tb.message_handler(commands=['start'])
def send_welcome(message):
    tb.send_message(chat_gloria, "Que te apetece hacer?", reply_markup=markup2)

@tb.message_handler(commands=['photo'])
def make_photo(message):
    photo = hacer_foto()
    tb.send_photo(message.chat.id, photo,"Foto tomada: "+ datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))        
        
@tb.message_handler(func=visor)
def alarma(message):
    return True

    
@tb.message_handler(func=lambda message: True)
def echo_all(message):
    global block
    if block==0:
        tb.send_message(message.chat.id, "Comando desconocido.")
    #Podemos realizar aqui la preparacion de la alarma sin tener que crear otra funcion
    else:
        hora_prog=datetime.datetime.strptime(message.text, "%H:%M")
        hora_act=datetime.datetime.now()
        hora=datetime.datetime.now().strftime("%H:%M")
        if hora_prog.hour<hora_act.hour:
            h_res=hora_prog.hour+24-hora_act.hour
        else:
            h_res=hora_prog.hour-hora_act.hour
        if hora_prog.minute<hora_act.minute:
            m_res=hora_prog.minute+24-hora_act.minute
            m_res=abs
            
        else:
            m_res=hora_prog.minute-hora_act.minute
        sec=h_res*3600+m_res*60
        timer=threading.Timer(sec, finlavado)
        timer.start()
        tb.send_message(message.chat.id, "La lavadora finalizara en: " + str(h_res)+ " horas " + str(m_res)+ " mins")
        #El boqueo acaba en la funcion que se ejecute al final del timer
        
        



tb.polling()
        
        
        
        
