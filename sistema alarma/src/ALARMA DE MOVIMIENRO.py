# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:43:14 2017

@author: pi
"""

# importamos todos los modulos

from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#inicializamos pines de salida y entrada

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # definimos la numeracion

sensor=7
GPIO.setup(7, GPIO.IN) # definimos el pin como entrada

pulsador=3
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

rojo=11
GPIO.setup(11, GPIO.OUT)
GPIO.output(rojo, False)

verde=13
GPIO.setup(13, GPIO.OUT)
GPIO.output(verde, True)

#configuramos dirección de mail

direccion_fuente = "alarmadeii2@gmail.com"
direccion_destino = "alarmadeii2@gmail.com"
password = "alarmamii"

def espera_boton(pin):
    leeboton=GPIO.input(pin)
    while leeboton==1:
        leeboton=GPIO.input(pin)
    time.sleep(0.02)
    while leeboton==0:
        leeboton=GPIO.input(pin)
    time.sleep(0.02)

def enviamail():
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()
    server.login(direccion_fuente, password)

    msg = MIMEMultipart()
    msg['From'] = direccion_fuente
    msg['To'] = direccion_destino
    msg['Subject'] = "Alarma de intruso"

    cuerpo_mensaje = "La alarma de movimiento ha sido activada. Se adjunta imagen con el motivo de la activación"
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

    archivo = "sensormov.jpg"
    adjunto = open(archivo, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((adjunto).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % archivo)
    msg.attach(part)

    texto = msg.as_string()
    print texto
            
    try:
        print "Enviando email"
        print server.sendmail(direccion_fuente, direccion_destino, texto)
    except:
        print "Error al enviar el email"
        server.quit()

    server.quit()

def parpadea(led,tiempototal):

    for i in range(0,2*tiempototal):
        if i%2==0:                      #parpadeo led rojo
            GPIO.output(led, False)
            print tiempototal-i/2
        else:
            GPIO.output(led, True)       #al final queda encendido
        time.sleep(0.5)  
    
def esperayenvia(tiempototal):
    for i in range (0,tiempototal*10):

        time.sleep(0.1)

        if i%5==0:
            if i%10==0:
                print tiempototal-i/10
                GPIO.output(verde, False)
            else:
                GPIO.output(verde, True)
                
        if GPIO.input(pulsador)==1:
           GPIO.output(verde,True) 
           print"Alarma desactivada a tiempo. Bienvenido a casa."
           return
           
    enviamail()
    print "El aviso ha sido enviado a su mail, la alarma se desactivará."

           

# ESTE SERÁ EL BUCLE QUE SE REPETIRÁ SIEMPRE

while(1):

    print "Pulse el boton para activar la alarma"

    espera_boton(pulsador)      

    GPIO.output(verde, False)

    #configuramos camara

    camera = PiCamera()
    camera.resolution = (640,480)
    camera.rotation = 180
    camera.start_preview(fullscreen=False, window=(30,30,320,240))
    
    print "La alarma se activará en..."
    parpadea(rojo,10)       
    print "¡Alarma activada!"
    
    espera_boton(sensor)

    camera.capture('/home/pi/ProyectoDEII/sensormov.jpg')
    camera.stop_preview()
    camera.close()
    
    print "Movimiento detectado. Dispone de 10 segundos para apagar la alarma..."
    
    GPIO.output(verde, True) #enciende el led verde también

    esperayenvia(10)

    GPIO.output(rojo, False)
    time.sleep(1)                    
        

