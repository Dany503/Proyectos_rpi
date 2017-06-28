# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:29:47 2016

@author: pi
"""

import RPi.GPIO as GPIO
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Configuracion pines
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.IN)
GPIO.setup(5,GPIO.IN)
GPIO.setup(7,GPIO.IN)
GPIO.setup(11,GPIO.OUT)

# Correo
dir_fuente = "xxxxx"
dir_destino = "xxxxxx"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(dir_fuente, "123456gj")

msg = MIMEMultipart()
msg['From'] = dir_fuente
msg['To'] = dir_destino

# Definicion de funciones
def envia_correo(asunto,cuerpo):
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))
    texto = msg.as_string()
    server.sendmail(dir_fuente, dir_destino, texto)

# Programa
tor_asada = 1
cnt_asada = 0
tor_helada = 1
cnt_helada = 0
while (1):
    
    # Avisos
    tor_asada = GPIO.input(3)
    tor_helada = GPIO.input(5)
    print "tor_asada: %d, tor_helada: %d cnt_asada: %d, cnt_helada : %d" %(tor_asada,tor_helada,cnt_asada,cnt_helada)
    if tor_asada == 0 and cnt_asada == 0:
        envia_correo("Tortuga: Temperatura muy alta", "La temperatura ambiente es superior a 35 ºC.")
        cnt_asada = 20000;
    else: 
        if cnt_asada > 0:
            cnt_asada = cnt_asada - 1;
            
    if tor_helada == 0 and cnt_helada == 0:
        envia_correo("Tortuga: Temperatura muy baja", "La temperatura ambiente es inferior a 15 ºC.")
        cnt_helada = 20000;
    else: 
        if cnt_helada > 0:
            cnt_helada = cnt_helada - 1;
            
    # Actuador
    if GPIO.input(7) == 0:
        GPIO.output(11, GPIO.HIGH)
    else:
        GPIO.output(11, GPIO.LOW)
    print "rele input: %d" %(GPIO.input(7))
    time.sleep(2)
            
