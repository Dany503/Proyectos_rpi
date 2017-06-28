
from mcpi.minecraft import Minecraft #funciones Minecraft
from mcpi import block #funciones bloques Minecraft
from sense_hat import SenseHat #funciones Sensehat
from twython import Twython #funciones Twitter
import time #funciones de tiempo
import subprocess #funciones para simular teclado
#---------------------------#
from picamera import PiCamera # Funciones para poder tomar foto y modificarlas
from PIL import Image 
#from time import sleep 
import webbrowser # Funciones para poder abrir el navegados


#Funcion tomar foto 
def funcion_foto():
	camera=PiCamera()
	camera.resolution=(640-250,480-200)
	camera.rotation=180
	camera.start_preview(fullscreen=False,window=(30,30,320,240))
	for i in range (0,5):
		print 5-i
		time.sleep(1)
	camera.capture('/home/pi/varios/imagen.jpg')
	camera.stop_preview()# Para ver la foto he utilizado otra libreria no se porque no me funiona esta 
	camera.close()
# Funcion detectar color
def funcion_color():
    funcion_foto()
    img=Image.open('/home/pi/varios/imagen.jpg')
    width,height=img.size
    r_ave=0
    g_ave=0
    b_ave=0
    for x in range (0, width):
        for y in range (0, height):
            r,g,b=img.getpixel((x,y))
            r_ave=(r+r_ave)/2
            g_ave=(g+g_ave)/2
            b_ave=(b+b_ave)/2
    average_colo=[r_ave,g_ave,b_ave]
    if max(average_colo)==r_ave:
        print('Color predominante es rojo')
        salida=0
    elif max(average_colo)==g_ave:
        print('Color predominante es verde')
        salida=1
    else: 
        print('Color predominante es azul')
        salida=2
    return(salida)

#----------------------------#
#conexion al juego
mc=Minecraft.create()
#AUXILIAR joystick
sense = SenseHat()
#define colores
r=[255,0,0]
e=[0,0,0]
g=[0,255,0]
b=[0,0,255]
w=[255,255,255]



#FUNCION AUXILIAR DISPLAY
def displayArrow(c,rot):
    arrow=[
        e,e,e,c,c,e,e,e,
        e,e,c,c,c,c,e,e,
        e,c,c,c,c,c,c,e,
        c,c,e,c,c,e,c,c,
        c,e,e,c,c,e,e,c,
        e,e,e,c,c,e,e,e,
        e,e,e,c,c,e,e,e,
        e,e,e,c,c,e,e,e]
    sense.set_rotation(rot)
    sense.set_pixels(arrow)

stop=[ #para parar de mostrar
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e]
salto=[
    b,b,e,e,e,e,b,b,
    e,b,b,e,e,b,b,e,
    e,e,b,b,b,b,e,e,
    e,e,e,b,b,e,e,e,
    e,e,e,b,b,e,e,e,
    e,e,b,b,b,b,e,e,
    e,b,b,e,e,b,b,e,
    b,b,e,e,e,e,b,b]



#Variables auxiliares 
t_partida=90 #tiempo partida
t_total=0 #tiempo total jugado
pasos_partida=0 #numero de pasos dados
pasos_total=0
bloques_partida=0 #numero de bloques cambiados
bloques_total=0
color=0; #determina que tipo de bloque pongo, inicializado a no hacer nada

#FUNCION MOVER PERSONAJE
def joystick(pasos): #devuelvo numero de pasos dados
    events=sense.stick.get_events()
    for event in events:
        if event.direction == "down" and event.action != "released": #pulsan joystick abajo, simulo pulsacion tecla s
            displayArrow(b,180) #pongo flecha girada 180
            #subprocess.call(["xdotool","key","s"])
            subprocess.call(["xdotool","keydown","s"])
            subprocess.call(["xdotool","keyup","s"])
            pasos=pasos+1; #actualizo pasos dados
        if event.direction == "up" and event.action != "released": #simulo w
            displayArrow(b,0)
            #subprocess.call(["xdotool","key","w"])
            subprocess.call(["xdotool","keydown","w"])
            subprocess.call(["xdotool","keyup","w"])
            pasos=pasos+1; #actualizo pasos dados
        if event.direction == "right" and event.action != "released":
            displayArrow(b,90)
            #subprocess.call(["xdotool","key","d"])
            subprocess.call(["xdotool","keydown","d"])
            subprocess.call(["xdotool","keyup","d"])
            pasos=pasos+1; #actualizo pasos dados
        if event.direction == "left" and event.action != "released":
            displayArrow(b,270)
            #subprocess.call(["xdotool","key","a"])
            subprocess.call(["xdotool","keydown","a"])
            subprocess.call(["xdotool","keyup","a"])
            pasos=pasos+1; #actualizo pasos dados
        if event.direction == "middle" and event.action == "pressed": #simulo espacio
            sense.set_pixels(salto)
            subprocess.call(["xdotool","keydown","space"])
            subprocess.call(["xdotool","keyup","space"])
        if event.action == "released":
            sense.set_pixels(stop)
    return(pasos)

#FUNCION GESTION GOLPES
def golpe(bloques,color):
    for hit in mc.events.pollBlockHits():
            if mc.getBlock(hit.pos.x, hit.pos.y, hit.pos.z) == 57:
                mc.postToChat("CAMARA ENCENDIDA")
                #LLAMADA FUNCION RIDA
                color=funcion_color()
            if mc.getBlock(hit.pos.x, hit.pos.y, hit.pos.z)!= 57:
                #si no le pego al bloque de diamante, lo modifico
                if color==0:
                    mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z,block.LAVA.id)
                if color==1:
                    mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z,block.LEAVES.id)
                if color==2:
                    mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z,block.WATER.id)
                #si no color no es ninguno de esos, dejo bloque tal cual
                bloques=bloques+1; #actualizo numero de golpes dados
    return(bloques,color) #sacamos el color para guardarlo

#FUNCION ACTUALIZAR FICHEROS
def actualiza_ficheros(t_partida, pasos_partida, bloques_partida):
    #Archivo de texto formato numero, solo guardo totales
    f=open('datos_aux.txt','r')
    fa=int(f.readline()) #leo primer caracter de primera linea
    fb=int(f.readline())
    fc=int(f.readline())
    f.close()
    f=open('datos_aux.txt','w') #reabro para machacar fichero
    t_total=fa #tiempo total jugado
    pasos_total=fb #pasos total
    bloques_total=fc #bloques total
    
    #Actualizo variables
    t_total=str(t_total+t_partida) #tiempo total jugado
    pasos_total=str(pasos_total+pasos_partida)
    bloques_total=str(bloques_total+bloques_partida)
    t_partida=str(t_partida)
    pasos_partida=str(pasos_partida)
    bloques_partida=str(bloques_partida)
    #Guardo datos
    ##Archivo de texto formato numeros
    f.write(t_total+"\n"+pasos_total+"\n"+bloques_total+"\n")
    ##Archivo de texto formato frase
    f2=open('datos.txt','w') #abro archivo para escribir
    #creo mensaje en formato cadena texto
    mensaje="Tpo. juego: "+t_partida+" s\nTpo. juego historial: "+t_total+" s\nPasos dados: "+pasos_partida+"\nPasos dados historial: "+pasos_total+"\nBloques cambiados: "+bloques_partida+"\nBloques cambiados historial: "+bloques_total
    f2.write(mensaje)
    f.close() #cierro fichero
    f2.close() #cierro fichero
    return (mensaje)


#FUNCION TWITTER
def sube_twitter(mensaje):
    APP_KEY = "cPhIoBvJgOqxzRGO7mlZ2yPjq"
    APP_SECRET = "N0OpngEL5fYBXd3CgM710KtL8Bg5g0IdLS37lL3MnoShlNsfBQ"
    OAUTH_TOKEN = "801872543292465156-XlH9ZGxpuZTNWqwXHLvygGSQX4in0iY"
    OAUTH_TOKEN_SECRET = "IHrTBCnOC2mCtQv4XcBTtQwBxPw6O0kyrd4qQrlnxeB18"
    
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    photo = open('/home/pi/varios/imagen.jpg', 'rb') 
    twitter.update_status_with_media(status=mensaje,media=photo)



#MAIN 

#Guardo hora para luego comparar
ini=time.time()
fin=time.time()
dif=fin-ini; 
mc.postToChat("Tienes 90 segundos para jugar")
mc.postToChat("Golpea diamante")

#pongo bloque diamante delante del jugador
p=mc.player.getTilePos()
mc.setBlock(p.x+1, p.y, p.z, block.DIAMOND_BLOCK)
#mc.postToChat("Bloque diamante creado en x=" + str(p.x+1) + ", y=" + 
#str(p.y) + ", z=" + str(p.z))

#BUCLE 
while dif<t_partida: #mientras no hayan pasado t_partida
# segundos desde que inicie
    #Movimiento y actualizacion pasos
    pasos_partida=pasos_partida+joystick(0)
    #Golpes y actualizacion bloques
    aux,color=golpe(0,color)
    bloques_partida=bloques_partida+aux
    #actualizo tiempo juego
    fin=time.time()
    dif=fin-ini

#FIN PARTIDA
sense.set_pixels(stop) #reseteo leds sensehat
mc.postToChat("FIN PARTIDA")
mc.postToChat("FOTO USUARIO")

#LLAMAR A FUNCION DE RIDA DE HACER UNA FOTO
funcion_foto()

#GUARDAR DATOS
#guardo datos y creo cadena texto
mensaje=actualiza_ficheros(t_partida, pasos_partida, bloques_partida)

#ABRIR NAVEGADOR
webbrowser.open('http://localhost/datos.php')

#SUBIR FOTO USUARIO Y DATOS A TWITTER
sube_twitter(mensaje)
