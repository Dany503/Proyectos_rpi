# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 19:31:07 2017

@author: pi
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 18:31:26 2017

@author: pi
"""

#!/usr/bin/env python

__author__ = 'Carlos y Ruben'

"""importamos librerias necesarias"""
import tweepy 
from subprocess import call  #para subproceso twitter
from datetime import datetime #Para fecha y hora 
import httplib, urllib 
#import math
import time
sleep = 20 # Tiempo de espera
sleep2= 60
global y
y=0
key = '0WMY9VZ5MUQZ1URW'  #Clave de Thingspeak
global temp
temp =0
global humedad
humedad=0
global presion
presion=0
global libre
libre=1

from sense_hat import SenseHat#importamos libreria de sensehat
sense = SenseHat()

"""Funcion de adquisicion de datos de temperatura, humedad y presion"""

def adquisicion():
    tempsuma=0
    humedadsuma=0
    presionsuma=0
    for i in range(10):
        #LEEMOS TEMPERATURA
        temp = sense.get_temperature()      
        temp = round(temp, 1)
        tempsuma=tempsuma+temp
        #LEEMOS HUMEDAD
        humedad = sense.get_humidity()
        humedad = round(humedad, 1)
        humedadsuma=humedadsuma+humedad
        #LEEMOS PRESION 
        presion = sense.get_pressure()
        presion = round(presion, 1)
        presionsuma=presionsuma+presion
    tempsuma=tempsuma/10
    humedadsuma=humedadsuma/10
    presionsuma=presionsuma/10
    print('******************************')
    print('**Nueva Adquisicion de Datos**')
    print('******************************')    
    print'El valor de la temperatura media es',tempsuma
    print'El valor de la humedad media es',humedadsuma
    print'El valor de la presion media es',presionsuma
    print('Envio de Datos a ThingSpeak')
    global temp
    global humedad
    global presion
    temp=tempsuma
    temp = round(temp, 1)
    humedad=humedadsuma
    humedad = round(humedad, 1)
    presion=presionsuma
    presion = round(presion, 1)


def enviartemperatura():
    while True:
        global temp
 #ENVIAMOS TEMPERATURA       
        params = urllib.urlencode({'field1': temp,'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print temp
            print response.status, response.reason
            response.read()
            conn.close()
        except:
            print "connection failed"
        break
    
def enviarhumedad(): 
    while True:
        global humedad
 #ENVIAMOS HUMEDAD 
        params2 = urllib.urlencode({'field2': humedad, 'key':key }) 
        headers2 = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn2 = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn2.request("POST", "/update", params2, headers2)
            response2 = conn2.getresponse()
            print humedad
            print response2.status, response2.reason
            response2.read()
            conn2.close()
        except:
            print "connection failed"
        break
        
def enviarpresion():
    while True:
        global presion
 #ENVIAMOS PRESION         
        params3 = urllib.urlencode({'field3': presion, 'key':key }) 
        headers3 = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn3 = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn3.request("POST", "/update", params3, headers3)
            response3 = conn3.getresponse()
            print presion
            print response3.status, response3.reason
            response3.read()
            conn3.close()
        except:
            print "connection failed"
        break
    
def enviarfototwitter():
    while True:
        print('Enviando Tweet...')
        i = datetime.now()               #Adquiere la fecha y la hora para el tuit  
        now = i.strftime('%Y%m%d-%H%M%S')  
        photo_name = now + '.jpg'  
        cmd = 'raspistill -t 500 -w 1024 -h 768 -o /home/pi/' + photo_name   
        call ([cmd], shell=True)         #Echa la foto 
  
        # Consumer keys and access tokens, used for OAuth  
        consumer_key = 'KQw7OqYQdxACCjtzOSQ1h3f55'  
        consumer_secret = 'Grl8pqlsPa4pAmlXmKxksS1fayqLz9tvXn4bPjRwN1PhyFUs70'  
        access_token = '827656432556339200-dNl078kPhPz1eJtRYULdwcMOJAzUNaq'  
        access_token_secret = 'sqGzITNIe709CWky7k0M6rKuxjD3eIrBPbRlI210Qql6U'  
  
  # OAuth process, using the keys and tokens  
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
        auth.set_access_token(access_token, access_token_secret)  
   
   # Creation of the actual interface, using authentication  
        api = tweepy.API(auth)  
  
   # Send the tweet with photo  
        photo_path = '/home/pi/' + photo_name  
        status = 'Consulta los datos meteorologicos aqui: https://thingspeak.com/channels/219113' + i.strftime('fecha de tweet: %Y/%m/%d %H:%M:%S')   
        api.update_with_media(photo_path, status=status)
        print('**Tweet enviado**')
        break

def arriba ():
        global y
        y=0         
        sense.set_pixel(3, 0, 255, 255, 255)
        sense.set_pixel(4, 0, 255, 255, 255)
        sense.set_pixel(3, 1, 255, 255, 255)
        sense.set_pixel(4, 1, 255, 255, 255)
        sense.set_pixel(3, 2, 255, 255, 255)
        sense.set_pixel(4, 2, 255, 255, 255)
        sense.set_pixel(3, 3, 255, 255, 255)
        sense.set_pixel(4, 3, 255, 255, 255)
        sense.set_pixel(3, 4, 255, 255, 255)
        sense.set_pixel(4, 4, 255, 255, 255)
        sense.set_pixel(3, 5, 255, 255, 255)
        sense.set_pixel(4, 5, 255, 255, 255)
        sense.set_pixel(3, 6, 255, 255, 255)
        sense.set_pixel(4, 6, 255, 255, 255)
        sense.set_pixel(3, 7, 255, 255, 255)
        sense.set_pixel(4, 7, 255, 255, 255)
        sense.set_pixel(0, 3, 255, 255, 255)
        sense.set_pixel(1, 2, 255, 255, 255)
        sense.set_pixel(2, 1, 255, 255, 255)
        sense.set_pixel(5, 1, 255, 255, 255)
        sense.set_pixel(6, 2, 255, 255, 255)
        sense.set_pixel(7, 3, 255, 255, 255)
        adquisicion()
        enviartemperatura()
        time.sleep(3)
        
      
      
def derecha():
        global y
        y=0
        sense.set_pixel(0, 3, 255, 255, 255)
        sense.set_pixel(0, 4, 255, 255, 255)
        sense.set_pixel(1, 3, 255, 255, 255)
        sense.set_pixel(1, 4, 255, 255, 255)
        sense.set_pixel(2, 3, 255, 255, 255)
        sense.set_pixel(2, 4, 255, 255, 255)
        sense.set_pixel(3, 3, 255, 255, 255)
        sense.set_pixel(3, 4, 255, 255, 255)
        sense.set_pixel(4, 3, 255, 255, 255)
        sense.set_pixel(4, 4, 255, 255, 255)
        sense.set_pixel(5, 3, 255, 255, 255)
        sense.set_pixel(5, 4, 255, 255, 255)
        sense.set_pixel(6, 3, 255, 255, 255)
        sense.set_pixel(6, 4, 255, 255, 255)
        sense.set_pixel(7, 3, 255, 255, 255)
        sense.set_pixel(7, 4, 255, 255, 255)
        sense.set_pixel(4, 0, 255, 255, 255)
        sense.set_pixel(5, 1, 255, 255, 255)
        sense.set_pixel(6, 2, 255, 255, 255)
        sense.set_pixel(6, 5, 255, 255, 255)
        sense.set_pixel(5, 6, 255, 255, 255)
        sense.set_pixel(4, 7, 255, 255, 255)
        adquisicion()
        enviarhumedad()
        time.sleep(3)
        
        
        
        
        
def izquierda():
        global y
        y=0
        sense.set_pixel(0, 3, 255, 255, 255)
        sense.set_pixel(0, 4, 255, 255, 255)
        sense.set_pixel(1, 3, 255, 255, 255)
        sense.set_pixel(1, 4, 255, 255, 255)
        sense.set_pixel(2, 3, 255, 255, 255)
        sense.set_pixel(2, 4, 255, 255, 255)
        sense.set_pixel(3, 3, 255, 255, 255)
        sense.set_pixel(3, 4, 255, 255, 255)
        sense.set_pixel(4, 3, 255, 255, 255)
        sense.set_pixel(4, 4, 255, 255, 255)
        sense.set_pixel(5, 3, 255, 255, 255)
        sense.set_pixel(5, 4, 255, 255, 255)
        sense.set_pixel(6, 3, 255, 255, 255)
        sense.set_pixel(6, 4, 255, 255, 255)
        sense.set_pixel(7, 3, 255, 255, 255)
        sense.set_pixel(7, 4, 255, 255, 255)
        sense.set_pixel(3, 0, 255, 255, 255)
        sense.set_pixel(2, 1, 255, 255, 255)
        sense.set_pixel(1, 2, 255, 255, 255)
        sense.set_pixel(1, 5, 255, 255, 255)
        sense.set_pixel(2, 6, 255, 255, 255)
        sense.set_pixel(3, 7, 255, 255, 255)
        adquisicion()
        enviarpresion()
        time.sleep(3)
        
        
        
        
        
def abajo():
        global y
        y=0
        sense.set_pixel(3, 0, 255, 255, 255)
        sense.set_pixel(4, 0, 255, 255, 255)
        sense.set_pixel(3, 1, 255, 255, 255)
        sense.set_pixel(4, 1, 255, 255, 255)
        sense.set_pixel(3, 2, 255, 255, 255)
        sense.set_pixel(4, 2, 255, 255, 255)
        sense.set_pixel(3, 3, 255, 255, 255)
        sense.set_pixel(4, 3, 255, 255, 255)
        sense.set_pixel(3, 4, 255, 255, 255)
        sense.set_pixel(4, 4, 255, 255, 255)
        sense.set_pixel(3, 5, 255, 255, 255)
        sense.set_pixel(4, 5, 255, 255, 255)
        sense.set_pixel(3, 6, 255, 255, 255)
        sense.set_pixel(4, 6, 255, 255, 255)
        sense.set_pixel(3, 7, 255, 255, 255)
        sense.set_pixel(4, 7, 255, 255, 255)
        sense.set_pixel(0, 4, 255, 255, 255)
        sense.set_pixel(1, 5, 255, 255, 255)
        sense.set_pixel(2, 6, 255, 255, 255)
        sense.set_pixel(5, 6, 255, 255, 255)
        sense.set_pixel(6, 5, 255, 255, 255)
        sense.set_pixel(7, 4, 255, 255, 255)
        enviarfototwitter()
        time.sleep(3)
        
        
        
def centro ():
        global y
        y=0
        sense.set_pixel(3, 3, 255, 255, 255)
        sense.set_pixel(3, 4, 255, 255, 255)
        sense.set_pixel(4, 3, 255, 255, 255)
        sense.set_pixel(4, 4, 255, 255, 255)
        adquisicion()
        enviartemperatura()
        time.sleep(sleep)
        enviarhumedad()
        time.sleep(sleep)
        enviarpresion()
        time.sleep(sleep)
        enviarfototwitter()
        

realiza_proceso=1

while realiza_proceso==1:
    sense.clear()
    time.sleep(0.1)
    y=y+1
    if y==1200:
        adquisicion()
        enviartemperatura()
        time.sleep(sleep)
        enviarhumedad()
        time.sleep(sleep)
        enviarpresion()
        time.sleep(sleep)
        enviarfototwitter()
        y=0
    for event in sense.stick.get_events():
            print("Movimiento del joystick: {} {}".format(event.action, event.direction))
            if event.direction == "down" and event.action != "released":
                abajo()
            if event.direction == "up" and event.action != "released":
                arriba()
            if event.direction == "left" and event.action != "released":
                izquierda()
            if event.direction == "right" and event.action != "released":
                derecha()    
            if event.direction == "middle" and event.action == "pressed":
                centro()
                
            if event.direction =="middle" and event.action == "held":

                sense.clear()
                realiza_proceso=0
        
    
        