
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:25:15 2017

@author: pi
"""
import time
import smtplib
from sense_hat import SenseHat


sense=SenseHat()

from picamera import PiCamera
camera = PiCamera()
camera.resolution = (640,480)
camera.rotation = 360
cont=1
cont_n=0

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

direccion_fuente = "nombrepractica2016@gmail.com"

direccion_destino = "simon.martinez.rzs@gmail.com, pablogg_sfc@hotmail.com"
server = smtplib.SMTP('smtp.gmail.com', 587)

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


#VALORES DE VARIABLES A GUARDAR PARA SUBIR AL SERVIDOR
Humedad=sense.get_humidity()
HMtr=str(round(Humedad,2))
Temp1=sense.get_temperature_from_humidity()
Temp2=sense.get_temperature_from_pressure()
TStr=str(round(Temp1,2))

Presion=sense.get_pressure()
PStr=str(round(Presion,2))

medidas=open("medidas_sala_emergencia.txt","w")
medidas.write("MEDICIONES AMBIENTALES EN SALA DE EMERGENCIA \n\n")
medidas.write("Humedad: %s\n" %Humedad)
medidas.write("Temperatura1: %s\n" %Temp1)
medidas.write("Temperatura2: %s\n" %Temp2)
medidas.write("Presión: %s\n" %Presion)
medidas.close()


bucle=True
while bucle:
    
    events = sense.stick.get_events()
    for event in events:
        if event.direction  == "down" and event.action != "released":
            print("Humedad: %2.3f" %Humedad)            
            sense.show_message("HM:"+HMtr)
            time.sleep(2)
            sense.clear()
            medidas=open("medidas_sala_emergencia.txt","w")
            medidas.write("MEDICIONES AMBIENTALES EN SALA DE EMERGENCIA \n\n")
            medidas.write("Humedad: %s\n" %Humedad)
            medidas.write("Temperatura1: %s\n" %Temp1)
            medidas.write("Temperatura2: %s\n" %Temp2)
            medidas.write("Presión: %s\n" %Presion)
            medidas.close()

        if event.direction  == "up"and event.action != "released":
            print("Temperaturas: %2.3f %2.3f" % (Temp1,Temp2))            
            sense.show_message("T:"+TStr)
            time.sleep(2)
            sense.clear()
            medidas=open("medidas_sala_emergencia.txt","w")
            medidas.write("MEDICIONES AMBIENTALES EN SALA DE EMERGENCIA \n\n")
            medidas.write("Humedad: %s\n" %Humedad)
            medidas.write("Temperatura1: %s\n" %Temp1)
            medidas.write("Temperatura2: %s\n" %Temp2)
            medidas.write("Presión: %s\n" %Presion)
            medidas.close()
            
        if event.direction  == "left"and event.action != "released":
            print("Presión: %4.2f" %Presion)
            sense.show_message("PS:"+PStr)
            time.sleep(2)
            sense.clear()
            medidas=open("medidas_sala_emergencia.txt","w")
            medidas.write("MEDICIONES AMBIENTALES EN SALA DE EMERGENCIA \n\n")
            medidas.write("Humedad: %s\n" %Humedad)
            medidas.write("Temperatura1: %s\n" %Temp1)
            medidas.write("Temperatura2: %s\n" %Temp2)
            medidas.write("Presión: %s\n" %Presion)
            medidas.close()
            
        if event.direction  == "right"and event.action != "released":
            camera.start_preview(fullscreen=False, window=(30,30,320,240))
            for i in range(0,5):
                print 5-i
                time.sleep(1)
                
            camera.capture('/home/pi/foto_%d.jpg' %cont)
            camera.stop_preview()
            time.sleep(1)
            cont=cont+1
            cont_n=cont-1
 

                        
        if (event.direction  == "middle" and event.action != "released"): #or (line==1):
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
            msg['Subject'] = "Estado Sala de Emergencia"
            
            
            cuerpo_mensaje = "Informacion de Sala de Emergencia: \n" + fecha_hora_msg  + "\n Humedad: %2.3f" %Humedad + "\n Temperatura1: %2.3f" %Temp1 + "\n Temperatura2: %2.3f" % Temp2   + "\n Presión: %4.2f" %Presion 
            msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
            
            archivo = ("foto_%d.jpg" %cont_n) 
            
            adjunto = open(archivo, "rb")
             
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((adjunto).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % archivo)
            msg.attach(part)
            
            texto = msg.as_string()
            print texto
            
            try:
                print "Enviando email" + fecha_hora_msg
                print server.sendmail(direccion_fuente, direccion_destino, texto)
            except:
                print "Error al enviar el email"
                server.quit()
                
            server.quit()

           
sense.clear()