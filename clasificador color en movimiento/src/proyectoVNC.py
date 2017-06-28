# -*- coding: utf-8 -*-

from sense_hat import SenseHat

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("anaramonpractica@gmail.com","anaramon")
emisor = "anaramopractica@gmail.com"
destinatario ="ramonromerogomez@gmail.com"
msg = "Vaciar Piezas Rojas"
msg2 = "Vaciar Piezas Azules"
sense=SenseHat()
#temperatura=int(round(sense.get_temperature_from_humidity(),0))

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640, 480))

events = sense.stick.get_events()

fondo = None
nuevaPiezaDetectada = 1
contadorAzules = 0
contadorRojas = 0

time.sleep(0.5)

sense.show_message('Inicio')

for frame in camera.capture_continuous(rawCapture, format ="bgr", use_video_port=True):
    
    image = frame.array
    
    gris = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    
    if fondo is None:
        fondo = gris
        
    diferencia = cv2.absdiff(fondo, gris)
    
    umbral = cv2.dilate(cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
    
    contornosimg = umbral.copy()
    
    contornos, hierarchy = cv2.findContours(contornosimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Detección de movimiento 
    movimientoDetectado = 0
    for contorno in contornos:
        
        if cv2.contourArea(contorno) < 500:
            continue
     
        if movimientoDetectado == 0:
            contornoMaximo = contorno
            movimientoDetectado = 1
        
        if cv2.contourArea(contorno) > cv2.contourArea(contornoMaximo):
            contornoMaximo = contorno
    
    # En caso de que se haya detectado algún movimiento            
    if movimientoDetectado:
        # Dibujar contorno
        (x, y, w, h) = cv2.boundingRect(contornoMaximo)
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        # Si es una pieza nueva        
        if nuevaPiezaDetectada == 1:
            nuevaPiezaDetectada = 0
            # Hacer diferencia entre piezas de dos colores
            azules = image[y:y+h,x:x+w,0]
            rojas = image[y:y+h,x:x+w,2]
            fil, col = azules.shape
            
            mediaAzules = np.sum(azules, dtype=np.int32)/(fil*col)
            mediaRojas = np.sum(rojas, dtype=np.int32)/(fil*col)
            
            if mediaAzules > mediaRojas:
                print('Nueva pieza AZUL detectada')
                contadorAzules = contadorAzules + 1
                sense.show_message('A',scroll_speed=0.02, text_colour=[0,0,255])
            else:
                print('Nueva pieza ROJA detectada')
                contadorRojas = contadorRojas + 1
                sense.show_message('R',scroll_speed=0.02, text_colour=[255,0,0])
                
            print(' Piezas Azules = %d' % contadorAzules)
            print(' Piezas Rojas = %d' % contadorRojas)
        
        #sense.show_message(str(temperatura),text_colour=[255,0,0])
    else:
        nuevaPiezaDetectada = 1

    # Descomentar estas líneas en pantalla VGA    
    cv2.imshow("Movimiento",image)
    #cv2.imshow("Umbral", umbral)
    #cv2.imshow("Resta", diferencia)
    #cv2.imshow("Contornos", contornosimg)
    
    bucle = True
    if contadorRojas == 3:
        print("Reiniciar")
        server.sendmail(emisor, destinatario, msg)
        sense.show_letter('R',text_colour=[255,0,0])
        while bucle:
            events = sense.stick.get_events()
            for event in events:
                if event.direction  == "middle":
                    bucle=False
                    contadorRojas=0
                    print("Reiniciado")
                    sense.clear()
                    
      
    sense.clear()


    if contadorAzules ==3:
        print("Reiniciar")
        server.sendmail(emisor, destinatario, msg2)
        sense.show_letter('A',text_colour=[0,0,255])
        while bucle:
            events = sense.stick.get_events()
            for event in events:
                if event.direction  == "middle":
                    bucle=False
                    contadorAzules=0
                    print("Reiniciado")
                    sense.clear()


    sense.clear()
    
    key = cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)
    
    if key == ord("s"):
                
        cv2.destroyAllWindows()        
        break
        
server.quit()    
    





