# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 02:20:21 2017

@author: pi
"""

# Librería SenseHat
from sense_hat import SenseHat
sense=SenseHat()
from signal import pause
import RPi.GPIO as GPIO

# Librería emails
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Librería cámara
from picamera import PiCamera
import cv2
import time

# Variables  Sala
estado_sala = 0                 # Variable estado para diferentes estados de emergencia en la sala

# Variables Pass
pass_estado = 0                 # Vairable estado para diferentes estados de introducir contraseña
pass_ok = 0                     # Variable control pass introducirdo correcto
pass_cnt = 0                    # Variable control para número de veces introducir contraseña
pass_flag = 0                   # Variable flag para validación contraseña
pass_in = 0                     # Vairable bloqueo inicio sesión

# Variables Stick
sense.clear()


# Variables Display
R = [255, 0, 0]  # Rojo
V = [0, 255, 0]  # Verde
correcto=[
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
V,V,V,V,V,V,V,V,
]
incorrecto=[
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
]
neutro=[
R,V,R,V,R,V,R,V,
V,R,V,R,V,R,V,R,
R,V,R,V,R,V,R,V,
V,R,V,R,V,R,V,R,
R,V,R,V,R,V,R,V,
V,R,V,R,V,R,V,R,
R,V,R,V,R,V,R,V,
V,R,V,R,V,R,V,R,
]

# Direcciones email
direccion_fuente = "padialillo@gmail.com"                   # Dirección correo electrónico fuente
direccion_destino = "alvaropadialmoreno@gmail.com"          # Dirección correo electrónico destino

while True:                                                 # Bucle infinito
    # Recogida de medida de sensores
    Humedad=sense.get_humidity()
    Temp1=sense.get_temperature_from_humidity()
    Temp2=sense.get_temperature_from_pressure()
    Presion=sense.get_pressure()
    
    if estado_sala == 0:
        if Temp1 > 40 or Temp2 > 40 or Humedad > 50:
            fichero=open("reporte.txt", "w")
            fichero.write("Lectura de los senores atmosfericos:\n")   
            fichero.write("Temperaturas: %2.3f %2.3f\n" % (Temp1, Temp2))
            fichero.write("Humedad: %2.3f\n" % Humedad)
            fichero.close()
            time.sleep(1)
            estado_sala = 1
    
    if estado_sala == 1:
        # Configuración de camara
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.rotation = 180
        #camera.start_recording('/home/pi/proyecto/video.mp4')
        #time.sleep(5)
        #camera.stop_recording()
        camera.capture('/home/pi/proyecto/image.jpg')
        camera.close()
        time.sleep(1)
        estado_sala = 2
    
    if estado_sala == 2:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(direccion_fuente, "28a800p875m")
        #msg = ("La humedad es mayor del 50%")
        
        msg = MIMEMultipart()
        msg['From'] = direccion_fuente
        msg['To'] = direccion_destino
        msg['Subject'] = "Mensaje estado de la sala."
        
        fechasyhora = list(time.localtime())
        ano = str(fechasyhora[0])
        mes = str(fechasyhora[1])
        dia = str(fechasyhora[2])
        hora = str(fechasyhora[3])
        minutos = str(fechasyhora[4])
        segundos = str(fechasyhora[5])

        hora_completa = hora + ":" + minutos 
        fecha_completa = dia + "/" + mes + "/" + ano
        cuerpo_mensaje_5 = "\nEnviado a las " + hora_completa + " del " + fecha_completa
                
        cuerpo_mensaje_0 = "Consulte en el siguiente enlace las condiciones de la sala:\n"
        cuerpo_mensaje_1 = "http://localhost/reporte.php\n"
        cuerpo_mensaje_2 = "Lectura de los senores atmosfericos:\n"
        cuerpo_mensaje_3 = "Temperaturas: %2.3f %2.3f\n" % (Temp1, Temp2)
        cuerpo_mensaje_4 = "Humedad: %2.3f\n" % Humedad
        cuerpo_mensaje = cuerpo_mensaje_0 + cuerpo_mensaje_1 + cuerpo_mensaje_2 + cuerpo_mensaje_3 + cuerpo_mensaje_4 + cuerpo_mensaje_5
        msg.attach(MIMEText(cuerpo_mensaje,'plain'))

        archivo = "image.jpg"
        adjunto = open(archivo,"rb")
        part = MIMEBase('application','octet-stream')
        part.set_payload((adjunto).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=%s" % archivo)
        msg.attach(part)

        texto = msg.as_string()       
        
        server.sendmail(direccion_fuente, direccion_destino, texto)
        server.quit()
        time.sleep(1)
        estado_sala = 3
    
    if estado_sala == 3:
        if Temp1 < 40 and Temp2 < 40 and Humedad < 50:
            time.sleep(1)
            estado_sala = 0

########################################################################################

########################################################################################           
            
    # Siempre va a estar registrando los eventos del Stick
    events = sense.stick.get_events()
    
    if pass_estado == 0:                                    # Estado inicial para introducir contraseña
        
        if pass_in == 0:        
            for event in events:                                # Si ocurre un evento en el stick...      
                if event.direction  == "down":                  # Stick hacia abajo
                    pass_in = 1
                if event.direction  == "up":                    # Stick hacia arriba
                    pass_in = 1
                if event.direction  == "left":                  # Stick hacia la izquierda
                    pass_in = 1
                if event.direction  == "right":                 # Stick hacia la derecha
                    pass_in = 1
                if event.direction  == "middle":                # Stick en la posición central
                    bucle=False
                                                                # ...se habilitar la introducción de código
        if pass_in == 1:                                        # Si se ha habilitado...
            pass_cnt =  pass_cnt + 1                            # Incremento de variable contador de introducir contraseña
            if pass_cnt > 3:                                    # Si es mayor que tres...
                pass_estado = 2                                 # Se pasa directamente al estado 2
                pass_ok = 0                                     # Pass introducido erróneo un número n veces
            else:
                pass_estado = 1                                 # Si no... nuevo intento
                sense.show_message("Introduzca Pass:",text_colour=[255,128,32])         # Mensaje de info para introducir contraseña
        
    if pass_estado == 1:                                    # Estado introducir contraseña
        print("%d" %pass_cnt)        
        for event in events:                                    # Si ocurre un evento en el stick...
            if event.direction  == "down" and event.action != "released":                      # Stick hacia abajo
                if pass_flag == 0:                              # Si flag correcto y movimiento correcto...
                    pass_flag = 1                               # Aumenta nivel flag
                    sense.set_pixels(correcto)                  # Display de color verde
                    time.sleep(1)                    
                    sense.clear()
                else:
                    pass_flag = 0                               # Pone flag a 0
                    pass_estado = 0                             # Vuelta al estado inicial
                    sense.set_pixels(incorrecto)                # Display de color rojo
                    time.sleep(1)                    
                    sense.clear()
            if event.direction  == "up" and event.action != "released":                        # Stick hacia arriba
                if pass_flag == 2:                              # Si flag correcto y movimiento correcto...
                    pass_flag = 3                               # Aumenta nivel flag
                    sense.set_pixels(correcto)                  # Display de color verde
                    time.sleep(1)                    
                    sense.clear()
                else:
                    pass_flag = 0                               # Pone flag a 0
                    pass_estado = 0                             # Vuelta al estado inicial
                    sense.set_pixels(incorrecto)                # Display de color rojo
                    time.sleep(1)                    
                    sense.clear()
            if event.direction  == "left" and event.action != "released":                      # Stick hacia la izquierda
                if pass_flag == 3:                              # Si flag correcto y movimiento correcto...
                    pass_estado = 2                             # Aumenta nivel flag
                    pass_ok = 1                                 # Pass Ok
                    sense.set_pixels(correcto)                  # Display de color verde
                    time.sleep(1)
                    sense.clear()
                else:
                    pass_flag = 0                               # Pone flag a 0
                    pass_estado = 0                             # Vuelta al estado inicial
                    sense.set_pixels(incorrecto)                # Display de color rojo
                    time.sleep(1)
                    sense.clear()
            if event.direction  == "right" and event.action != "released":                     # Stick hacia la derecha
                if pass_flag == 1:                              # Si flag correcto y movimiento correcto...
                    pass_flag = 2                               # Aumenta nivel flag                  
                    sense.set_pixels(correcto)                  # Display de color verde
                    time.sleep(1)
                    sense.clear()
                else:
                    pass_flag = 0                               # Pone flag a 0
                    pass_estado = 0                             # Vuelta al estado inicial
                    sense.set_pixels(incorrecto)                # Display de color rojo
                    time.sleep(1)
                    sense.clear()
            if event.direction  == "middle":                    # Stick posición central
                time.sleep(1)                
                sense.clear()
                bucle=False
            
    if pass_estado == 2:                                    # Si ha pasado al estado 2...
        if pass_ok == 1:                                    # Si la contraseña intoducida es correcta...
            sense.show_message("PASS CORRECTO",text_colour=[32,128,255])            # Mensaje de contraseña correcta
            time.sleep(5)                                   # Espera 5 segundos
        else:                                               # De lo contrario...
            sense.show_message("PASS INCORRECTO",text_colour=[32,128,255])        # Mensaje de contraseña incorrecta
            # Envío de correo para informar de acceso denegado
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(direccion_fuente, "28a800p875m")
            #msg = ("Se ha intentando acceder a la sala de manera incorecta tres veces.\n")

            msg = MIMEMultipart()
            msg['From'] = direccion_fuente
            msg['To'] = direccion_destino
            msg['Subject'] = "Mensaje estado de la sala."
            
            fechasyhora = list(time.localtime())
            ano = str(fechasyhora[0])
            mes = str(fechasyhora[1])
            dia = str(fechasyhora[2])
            hora = str(fechasyhora[3])
            minutos = str(fechasyhora[4])
            segundos = str(fechasyhora[5])

            hora_completa = hora + ":" + minutos 
            fecha_completa = dia + "/" + mes + "/" + ano
            cuerpo_mensaje_2 = "\nEnviado a las " + hora_completa + " del " + fecha_completa
            
            cuerpo_mensaje_0 = "Se ha intentando acceder a la sala de manera incorecta tres veces.\n"
            cuerpo_mensaje_1 = "Pongase en contacto con el personal de la instalacion.\n"
            cuerpo_mensaje = cuerpo_mensaje_0 + cuerpo_mensaje_1 + cuerpo_mensaje_2
            msg.attach(MIMEText(cuerpo_mensaje,'plain'))            
            texto = msg.as_string()             
            
            server.sendmail(direccion_fuente, direccion_destino, texto)
            server.quit()
            time.sleep(5)                                   # Espera 5 segundos

        pass_ok = 0                                         # Limpia variable pass ok
        pass_cnt = 0                                        # Limpia contador
        pass_in = 0                                         # Limpia variable bloqueo
        pass_flag = 0                                       # Limpia flag
        pass_estado = 0                                     # Pasa al estado de inicio de contraseña

########################################################################################