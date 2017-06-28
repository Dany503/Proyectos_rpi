"""#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
#Script que ejecutará nuestro programa
#Clase que maneja nuestro twitter e interpreta los comandos
import twitterPi as TwitterPi
#Librerias usadas por los sensores

from time import sleep

import sensores as sensor


import RPi.GPIO as GPIO


def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup(36)
    GPIO.setup(36,GPIO.OUT)
    
    """Se crea el objeto que controla twitter"""
    twitter = TwitterPi.manejo_twitter()
    TempHumedad = sensor.sens_TempHumdd()
    TempPresion = sensor.sens_TempPres()
    Humedad = sensor.sens_Humedad()
    Presion = sensor.sens_Presion()
    Camara = sensor.ctrl_Camara()
    
    #Bucle infinito de la aplicación
    while True:
        print("while")
        valor = twitter.update_status()
        if (valor != 0): #Si vemos que tenemos un nuevo tweet
            print("update")
            orden_actual = twitter.leer_ordenes()
        

            #código con el manejo de los sensores
            if (orden_actual == 1):#Sensor de Temperatura a partir de la Humedad
                TempHumedad.tomar_medida()
                TempHumedad.guardar_medida()
            
            elif (orden_actual == 2):#Sensor de Temperatura a partir de la Presion
                TempPresion.tomar_medida()
                TempPresion.guardar_medida()

            elif (orden_actual == 3):#Sensor de Humedad               
                Humedad.tomar_medida()
                Humedad.guardar_medida()

            elif (orden_actual == 4):#Sensor de Presión               
                Presion.tomar_medida()
                Presion.guardar_medida()

            elif (orden_actual == 5):#Cámara
                Camara.tomar_foto()
                
            elif (orden_actual == 6): #Todo
                TempHumedad.tomar_medida()
                TempHumedad.guardar_medida()       
                TempPresion.tomar_medida()
                TempPresion.guardar_medida()
                Humedad.tomar_medida()
                Humedad.guardar_medida()                
                Presion.tomar_medida()
                Presion.guardar_medida()
                Camara.tomar_foto()
            elif (orden_actual == 7):#Cámara
                GPIO.output(36,1)
            elif (orden_actual == 8):#Cámara
                GPIO.output(36,0)                                              
            else:
                print("\nComando no reconocido")

            #Twitteamos el resultado de nuestros sensores
            twitter.escribir_resultado(orden_actual)


            
        #Dormimos aplicación 5 segundos    
        sleep(5)

    print("\nSaliendo de la aplicación") 
if __name__ == '__main__': #Cuerpo principal
    main()
    
