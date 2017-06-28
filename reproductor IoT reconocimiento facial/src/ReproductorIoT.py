# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 20:45:56 2016

@author: ManoloP
"""
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import os
from sklearn.decomposition import RandomizedPCA
import numpy as np
import glob
import math
import string
import mpd
from sense_hat import SenseHat
import threading

TEST_MPD_HOST     = "localhost"
TEST_MPD_PORT     = "6600"

final=0 #variable para cerrar los hilos
sense=SenseHat()
mutex=threading.Lock() #Creación del mutex para usar MPD

###################### Definición hilo salida #######################

def salida(): #función para finalizar hilo de pantalla
    global final
    final=1

###################### Definición hilo pantalla #####################

def HiloPantalla():
    client = mpd.MPDClient()
    #Intento conectarme al MPD
    try:
        client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
        print "Hilo Pantalla: Intento Conexion "
    except mpd.ConnectionError:
        print "error"
    time.sleep(3)
    while final==0:
        print  final
        print "Hilo PANTALLA: IDLE"
        client.idle()
        print "Hilo PANTALLA: Cambio en el reproductor"
        mutex.acquire()
        datos=client.currentsong()
        print datos
        mutex.release()
        print "Hilo PANTALLA: info por pantalla "
        #if datos['name']=='':
        try:
            sense.show_message(datos['title'],scroll_speed=0.05, text_colour=[0,100,0])
        except KeyError:
            try:
                sense.show_message(datos['name'],scroll_speed=0.05, text_colour=[0,100,0])
            except KeyError:
                try:
                    sense.show_message(datos['file'],scroll_speed=0.05, text_colour=[0,100,0])
                except KeyError:
                    sense.show_message('Radio '+datos['pos'],scroll_speed=0.05, text_colour=[0,100,0])
        
    return

###################### Definición hilo reproductor #####################

def Reproductor(id_persona): #Recibe como argumento el nombre de la playlist
    
    print "El valor del ID a reproducir es "
    print id_persona
    
    client = mpd.MPDClient()
    if id_persona=='1':
        print "Me he metido en el if de ceci"
        lista='ceci'
    else:
        if id_persona=='3':
            lista='ramon'

    print "la lista a reproducir es "
    print lista

    try:
        client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
        print "Intento Conexion "
    except mpd.ConnectionError:
        print "error"

    #lanzamos el hilo de la pantalla
    hiloPant=threading.Thread(target=HiloPantalla)
    hiloPant.start()
    
    client.update()
    print " Conexion correcta "
    client.stop()
    print " Cancion parada "
    client.clear()
    client.load(lista)
    print " Playlist anadida "
    client.play(0)
    print " Play "
    client.disconnect()

    Ciclo=True
    while Ciclo:
        time.sleep(0.5)
        events = sense.stick.get_events()
        for event in events:
            if event.direction  == "down" and event.action != "released":
                time.sleep(0.5)
                print "Boton Down "
                client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
                pausa=client.status()
                mutex.acquire()
                client.stop()
                mutex.release()
                client.disconnect()
            if event.direction == "up" and event.action != "released":
                time.sleep(0.5)
                print "Boton Up "
                client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
                estado=client.status()
                if estado['state']=='stop':
                    mutex.acquire()
                    client.play(int(pausa['song']))
                    mutex.release()
                else:
                    mutex.acquire()
                    client.pause()
                    mutex.release()
                client.disconnect()
            if event.direction  == "right" and event.action != "released":
                time.sleep(0.5)
                print "Boton right "
                client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
                mutex.acquire()
                client.next()
                mutex.release()
                client.disconnect()
            if event.direction  == "left" and event.action != "released":
                time.sleep(0.5)
                print "Boton Left "
                client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
                mutex.acquire()
                client.previous()
                mutex.release()
                client.disconnect()
            if event.direction  == "middle" and event.action != "released":
                print "Boton Enter "
                salida()
                print final
                client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
                mutex.acquire()
                client.stop()
                mutex.release()
                client.disconnect()
                Ciclo=False

#pasamos a reproducir la playlist(habria que poner como argumento la
#posicion que se ve haciendo client.playlistinfo()

    hiloPant.join() #Esperamos a que se cierre el hilo
    sense.clear()
    return




#################### Definición de funciones para reconocimiento facial ############################

#function to get ID from filename
def ID_from_filename(filename):
    part = string.split(filename, '/')
    return part[1].replace("s", "")
 
#Función para adaptar la imagen al formato correcto
def prepare_image(filename):
    img_color = cv2.imread(filename)
    img_gray = cv2.cvtColor(img_color, cv2.cv.CV_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    return img_gray.flat
    
def reconocimiento(IMG_RES,NUM_EIGENFACES,NUM_TRAINIMAGES):    

    #IMG_RES = 92 * 112 # img resolution
    #NUM_EIGENFACES = 10 # images per train person
    #NUM_TRAINIMAGES = 100 # total images in training set
    
    #Cargar las imágenes de la base de datos desde la carpeta train_faces (cargamos la base de datos de calibracion en variable folder)
    folders = glob.glob('train_faces/*')
     
    # Creamos un vector con las imagenes en blanco y negro
    # y un vector con los ID de cada persona en cada imagen
    X = np.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8')
    y = []
    

    c = 0
    for x, folder in enumerate(folders):  #Hace un bucle por las carpetas
        train_faces = glob.glob(folder + '/*')
        for i, face in enumerate(train_faces):
            X[c,:] = prepare_image(face)
            y.append(ID_from_filename(face))
            c = c + 1
    
    # Hacemos el análisis de las imagenes
    pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
    X_pca = pca.transform(X)
    
    # carga test faces (normalmente una), se encuentran en test_faces
    test_faces = glob.glob('test_faces/*')
    
    # crea un vector con las imágenes en blanco y negro
    X = np.zeros([len(test_faces), IMG_RES], dtype='int8')
     

    for i, face in enumerate(test_faces):
        X[i,:] = prepare_image(face)
     
    # Se ejecuta sobre una imagen de test (foto tomada)
    for j, ref_pca in enumerate(pca.transform(X)):
        distances = []
        # Se calcula la distancia euclidea desde la imagen tomada a cada una de las imagenes de la database y las guarda
        for i, test_pca in enumerate(X_pca):
            dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
            distances.append((dist, y[i]))
     
        found_ID = min(distances)[1]
    
        print "Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])+ ")"
    
    return found_ID
        
####################################################################################

        
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(320, 240))

display_window = cv2.namedWindow("Faces")

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')

time.sleep(1)
#i=1
found_id_ant=0
found_id=4
contador=0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        h=h+10
        if (y-5)>0 and (x)>0 and (x+(92*h/112))<360 and (y-5+h)<240:
            cv2.rectangle(gray,(x,y-5),(x+(92*h/112),y-5+h),(255,0,0),2)
            #Suponemos que solo va a haber una cara
            im_cut=gray[(y-5):(y-5+h),(x):(x+(92*h/112))]
            cv2.imshow("recortadas",im_cut)
            small = cv2.resize(im_cut, (92,112), 0, 0)
            cv2.imwrite('11.jpg',small)
            os.remove(os.path.join('test_faces', 'test.jpg'))
            cv2.imwrite(os.path.join('test_faces', 'test.jpg'), small)
            found_id=reconocimiento(92*112,10,30)
            time.sleep(1)
            if found_id==found_id_ant:
                contador=contador+1
            else:
                contador=0
            found_id_ant=found_id
    cv2.imshow("Faces", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    #if i==3:
    if key == ord("q") or contador==3:
        #cv2.imwrite('resultado.jpg',image)
        break
camera.close()
cv2.destroyAllWindows()

#Creamos el hilo del reproductor
#found_ID=3   #prueba de reproductor
hilo=threading.Thread(target=Reproductor,args=(found_id,))
hilo.start()
print "Tu padre te espera"
hilo.join()
print "Yo soy tu padre"

