import numpy as np
import cv2
from picamera.array import PiRGBArray
import picamera
import time
import random
import sqlite3
import smtplib
from __builtin__ import raw_input
from email.MIMEText import MIMEText
from PIL import Image
import facebook
import os


con=sqlite3.connect('/home/pi/Documents/Trabajo/bbdd.db')  #conexion a la base de datos
cursor=con.cursor() #con el objeto cursor se accede a ella

camera=picamera.PiCamera()
camera.resolution=(640,480)
camera.framerate=32
camera.rotation=180

rawCapture=PiRGBArray(camera,size=(640,480))

def crear_tabla(): #crea la tabla donde se almacenan los resultados
    cursor.execute("""CREATE TABLE IF NOT EXISTS RANKING
           (NIVEL PRYMARY TEXT NOT NULL,
           NOMBRE KEY TEXT NOT NULL,
           CORREO TEXT NOT NULL,
            PUNTOS INT NOT NULL)""",)
    #print("Tabla creada con exito")
    
def insertar_datos(nivel,nombre,correo,puntos): #se inserta los datos del usuario
    cursor.execute("INSERT INTO RANKING(NIVEL,NOMBRE,CORREO,PUNTOS)\
               VALUES(?,?,?,?)",(nivel,nombre,correo,puntos))
     
    con.commit() #grabar los datos
    #print("Se guardo correctamente")
    
def comprobarUsuario(nivel,nombre,puntos):  #Comprueba si el usuario ya ha jugado en dicho nivel.
    cursor.execute("SELECT NIVEL,NOMBRE,CORREO,PUNTOS FROM RANKING")
    flag=0
    for i in cursor:
        if i[0]==nivel and i[1]==nombre:
            flag=1
            if puntos>i[3]:  #Si el usuario ya ha jugado en ese nivel
                actualizar_datos(nivel,nombre,puntos) #Se actualizan los datos
    return flag
def actualizar_datos(nivel,nombre,puntos): #cambiar puntuacion
    cursor.execute("UPDATE RANKING set PUNTOS=(?) where NOMBRE=(?) and NIVEL=(?)",(puntos,nombre,nivel))
    #print("Operacion satisfactoria")
    con.commit() #grabar los datos
    
def leer_tabla(): #leer tabla
    cursor.execute("SELECT NIVEL,NOMBRE,CORREO,PUNTOS FROM RANKING")
    #for i in cursor:
        #print "NIVEL= ",i[0]
        #print "NOMBRE= ",i[1]
        #print "CORREO= ", i[2]
        #print "PUNTOS= ",i[3]
        
def get_posts(imagen,nivel):
    cursor.execute("SELECT *  FROM RANKING ORDER BY PUNTOS DESC")
    con.commit();
    ind=2
    cv2.putText(imagen,"NOMBRE",(10,30),font,0.8,(0,0,255),2)
    cv2.putText(imagen,"NIVEL",(250,30),font,0.8,(0,0,255),2)
    cv2.putText(imagen,"PUNTOS",(490,30),font,0.8,(0,0,255),2)
    
    for i in cursor:
        if ind<12:
            if i[0]==nivel:
                cv2.putText(imagen,i[1],(10,30*ind),font,0.6,(0,0,255),2)
                cv2.putText(imagen,i[0],(250,30*ind),font,0.6,(0,0,255),2)
                cv2.putText(imagen,str(i[3]),(490,30*ind),font,0.6,(0,0,255),2)
                ind=ind+1
    

def comprobar_record(nivel,nombre,puntos):
    cursor.execute("SELECT * FROM RANKING WHERE PUNTOS>=(?) AND NIVEL=(?)",(puntos,nivel))
    x=0
    for i in cursor:
        if puntos==i[3] or puntos<i[3]:
            x=x+1
    if x==0:
        print("NUEVO RECORD!!!")
        emailFlag=1
    else:
        emailFlag=0
        
    return emailFlag
        
        
        #ENVIAR CORREO

def obtener_Record(nivel): #Para obtener los datos del mejor usuario segun cada nivel
    cursor.execute("SELECT NIVEL,NOMBRE,CORREO,PUNTOS FROM RANKING")
    puntos=0
    nombre=[]
    correo=[]
    for i in cursor:
        if nivel==i[0] and i[3]>puntos:
            nombre= i[1]
            correo= i[2]
            puntos= i[3]
    return nivel,nombre,correo,puntos

def enviaEmail(campeon,ptos,nivel):
    emisor="yismatoy@gmail.com"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emisor, "yismatoy22")
    cursor.execute("SELECT NIVEL,NOMBRE,CORREO,PUNTOS FROM RANKING")
    mensaje=MIMEText(campeon + " ha obtenido un nuevo record con " + str(ptos) + " puntos, nivel " + str(nivel) )
    mensaje['Subject']="Yismatoy, NUEVO RECORD"
    mensaje['From']=emisor
    
    for i in cursor:
        try:
            mensaje['To']=i[2]
            server.sendmail(emisor,i[2],mensaje.as_string())
            del mensaje['To']
            #print("Se ha enviado el correo a "+ i[1])
        except:
            print("No se ha enviado el correo a "+ i[1])
            
def postFacebook(campeon,ptos,nivel,foto):
    cursor.execute("SELECT NIVEL,NOMBRE,CORREO,PUNTOS FROM RANKING")
    mensaje=campeon + " ha obtenido un nuevo record con " + str(ptos) + " puntos, nivel " + str(nivel) 
    graph=facebook.GraphAPI('EAAD1lu9hZC3UBAJkMv8FpaIJk3vHxcZCZCbvgmwd0B09FO94q3g6QFaPABCRFqP64P9ZCTO12vx0J2xnrdoCZCNEAYaZANm93Bi962MpGirQuinkUmfBWHS2sj9rBQc4IKqsitdAPa2Sj4cTTrYivKkabhQ4KYJYYcsC0PAu1dqAZDZD')
    photo=open(foto,"rb")
    graph.put_photo(photo,message=mensaje)
    photo.close()

    

    
def foto(nombre,imagen,t0,comienzo):
    font=cv2.FONT_HERSHEY_SIMPLEX
    comienzo=comienzo
    if time.clock()-t0>0 and time.clock()-t0 < 1:
        num=3
    elif time.clock()-t0>1 and time.clock()-t0 < 2:
        num=2
    elif time.clock()-t0>2 and time.clock()-t0 < 3:
        num=1
    else:
        num=0
        comienzo=1
    cv2.putText(imagen,"Foto en ...",(10,70),font,2,(0,0,255),2)
    cv2.putText(imagen,str(num),(100,150),font,3,(0,0,255),2)
    return comienzo
        
            
    
    

class bola:
    
    def __init__(self): #Constructor de la clase bola. 
        self.x=random.randrange(100,500) #Define un valor aleatorio en eje x a la bola creada. Da un margen para que no se coma el lateral
        self.y=20 
    def mov(self,nivel): #metodo para configurar la velocidad de la bola
        if nivel=="bajo":
            self.y=self.y+1
        elif nivel=="alto":
            self.y=self.y+5
        else:
            self.y=self.y+3
    
    def dibujo(self,marco,im): #metodo para dibujar la bola
        if self.y<415:
#             cv2.circle(frame,(self.x,self.y),20,(0,0,255),-1)
             for c in range(0,3):
                 marco[self.y:self.y+im.shape[0], self.x:self.x+im.shape[1],c] = im[:,:,c]*(1-im[:,:,0]/255)+marco[self.y:self.y+im.shape[0], self.x:self.x+im.shape[1],c]*(im[:,:,0]/255)
        else:
            del(self)
    def _del_(self):
        print("Objeto destruido")
        
class vida:
    def __init__(self): #Constructor de la clase bola. 
        self.x=10
        self.y=10
    def dibujo(self,marco,im): #metodo para dibujar la bola
        for c in range(0,3):
            marco[self.y:self.y+im.shape[0], self.x:self.x+im.shape[1],c] = im[:,:,c]*(1-im[:,:,0]/255)+marco[self.y:self.y+im.shape[0], self.x:self.x+im.shape[1],c]*(im[:,:,0]/255)
    def _del_(self):
        print("Objeto destruido")
    
        
  
flagTime=0
nombre=raw_input("Nombre:")
correo=raw_input("Inserta correo: ")
dificultad=raw_input("Nivel de dificultad: bajo,medio o alto: ")

puntos=0
vidas=3
borra=0


imagen=cv2.imread('/home/pi/Documents/Trabajo/gota.jpg') # Se abre la imagen que se quiera superponer
cora=cv2.imread('//home//pi//Documents//Trabajo//corazon.png')
#print("Fin imagen")
#marco
overlay2=cv2.imread('/home/pi/Documents/Trabajo/marco1.png') # Se abre la imagen que se quiera superponer
overlayMask2 = cv2.cvtColor( overlay2, cv2.COLOR_BGR2GRAY ) # detecta la transparencia de la imagen para encontrar el hueco en que se enmarca
res, overlayMask2 = cv2.threshold( overlayMask2, 10, 1, cv2.THRESH_BINARY_INV)
h,w = overlayMask2.shape
overlayMask2 = np.repeat( overlayMask2, 3).reshape( (h,w,3) )
# fin marco

#print("Fin Marco")
#print(cora)
overlay = cv2.resize(imagen,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
overlayCora = cv2.resize(cora,None,fx=0.15, fy=0.15, interpolation = cv2.INTER_CUBIC)        
bolas=[] #Lista vacia que va a ir almacenando todas las bolas que se vayan creando
t=0 #inicializacion de variable para usar como temporizador
vida1=vida()
vida2=vida()
vida3=vida()
vida1.x=10
vida2.x=50
vida3.x=90

dif=np.zeros((480,640,3), np.uint8)
flagIni=0
num=3
comienzo=0
t0=time.clock()

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    image1=frame.array
    image2=frame.array
    image1=rawCapture.array
    image2=rawCapture.array
    imagen1=image1.copy()
    imagen1=cv2.flip(imagen1,1)
    imagen2=cv2.flip(image2,1)
     
    
    if flagIni==0:
        dif=np.zeros((480,640,3), np.uint8)
        flagIni=1
        
    else:
        dif=np.zeros((480,640,3), np.uint8)
        dif=cv2.absdiff(imagenAnt,imagen1)
        
    if comienzo==1:
        if vidas!=0:    
            if t==0 or t==50 or t==100 or t==150 or t==200 or t==250 or t==350 or t==400 or t==450 or t==300: #En estos instantes vamos creando bolas
                x=bola()  #Instanciamos un objeto
                bolas.append(x)
            for c in bolas: #Recorremos los objetos que se hayan creado
                #print(c.x,c.y,imagen1.shape)
                #if (sum(dif[c.y,c.x][0:3])>50):
                if (sum(dif[c.y,c.x][0:3])>50):
                    bolas.remove(c)
                    puntos=puntos+1
                    #print('Se explota')
                    
                c.dibujo(imagen1,overlay)  #Dibujamos la bola
                c.mov(dificultad) #Segun la dificultad se desplazara a una velocidad diferente
                if c.y>420:  #si una bola llega al final la eliminamos de la lista para que no ocupe memoria
                    bolas.remove(c)
                    vidas=vidas-1
                    #Borra vidas
                    if vidas==2:
                        del(vida3);
                    elif vidas==1:
                        del(vida2);
                    elif vidas==0:
                        del(vida1);
            #Manuela aniade:
            #Se aniade el marco
            imagen1 *= overlayMask2
            imagen1 += overlay2   
            if dificultad=="bajo":
                t=t+1
            elif dificultad=="medio":
                t=t+3
            else:
                t=t+5
                
            if t==480:  #Cuando llegue al final del marco se reinicia el temporizador
                t=0
                
            # FIN BOLAS
            
            #Pinta vidas
            if vidas==3:
                vida1.dibujo(imagen1,overlayCora)
                vida2.dibujo(imagen1,overlayCora)
                vida3.dibujo(imagen1,overlayCora)
            elif vidas==2:
                vida1.dibujo(imagen1,overlayCora)
                vida2.dibujo(imagen1,overlayCora)
            elif vidas==1:
                vida1.dibujo(imagen1,overlayCora)
                
            #Pinta puntos
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imagen1,("Score: " + str(puntos)),(450,30),font,1,(0,0,255),2)
    
        if vidas==0:
            for c in bolas:
                bolas.remove(c)
            #print(puntos)
            crear_tabla()
            emailFlag=comprobar_record(dificultad, nombre, puntos)
            res=comprobarUsuario(dificultad, nombre, puntos)
            if res==0:
                insertar_datos(dificultad, nombre, correo, puntos)
            leer_tabla()
            if emailFlag==1:
                enviaEmail(nombre,puntos,dificultad)
                postFacebook(nombre,puntos,dificultad,filee)
                
            get_posts(imagen1,dificultad) # para colocar el ranking
            if borra==0:
                os.remove(filee)
                borra=1
        
    elif comienzo==0:
        comienzo=foto(nombre,imagen1,t0,comienzo)
        if comienzo==1:
            #im=Image.fromarray(image1)
            filee="/home/pi/Documents/Trabajo/"+nombre+".jpg"
            cv2.imwrite(filee,imagen2)          
            

            #im.save(filee)
            
            #camera.capture(filee)
            
            
    cv2.moveWindow('video1',10,10)
    cv2.imshow('video1',imagen1)
    #cv2.imshow('video2',dif)

    imagenAnt=imagen2.copy()
    key=cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key==ord('q'):
        break
   
camera.close()
for i in range(1,10):
    cv2.destroyAllWindows()
    cv2.waitKey(1)
