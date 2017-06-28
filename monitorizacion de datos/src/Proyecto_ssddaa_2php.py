# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 14:58:26 2016

@author: dany
"""
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sense_hat import SenseHat
sense=SenseHat()


fechasyhora = list(time.localtime())
ano = str(fechasyhora[0])
mes = str(fechasyhora[1])
dia = str(fechasyhora[2])
hora = str(fechasyhora[3])
minutos = str(fechasyhora[4])
segundos = str(fechasyhora[5])
hora_completa = hora + ":" + minutos 
fecha_completa = dia + "/" + mes + "/" + ano
fecha_hora_msg = "\n Enviado a las " + hora_completa + " del " + fecha_completa + "\n"


Humedad=sense.get_humidity()
HMtr=str(round(Humedad,2))
Temp1=sense.get_temperature_from_humidity()
Temp2=sense.get_temperature_from_pressure()
TStr=str(round(Temp1,2))
Presion=sense.get_pressure()
PStr=str(round(Presion,2))


direccion_fuente = "nombrepractica2016@gmail.com"
direccion_destino = "simon.martinez.rzs@gmail.com"
# sustituir s1 por la dirección email fuente
# sustituir d1 por la dirección email destino
 
server = smtplib.SMTP('smtp.gmail.com', 587)
#server = smtplib.SMTP('smtp.live.com', 587) # para servidor hotmail
server.starttls()
server.login(direccion_fuente, "raspberrypi3")
# sustituir x1 por la contraseña

msg = MIMEMultipart()
msg['From'] = direccion_fuente
msg['To'] = direccion_destino
msg['Subject'] = "Sistemas Digitales Presente"

cuerpo_mensaje = "Informacion de Sala de Emergencia: \n" + fecha_hora_msg  + "\n Humedad: %2.3f" %Humedad + "\n Temperatura1: %2.3f" %Temp1 + "\n Temperatura2: %2.3f" % Temp2   + "\n Presión: %4.2f" %Presion 
msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
 

texto = msg.as_string()
print texto

try:
    print "Enviando email"
    print server.sendmail(direccion_fuente, direccion_destino, texto)
except:
    print "Error al enviar el email"
    server.quit()
    
server.quit()
