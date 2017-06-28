from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

### Parametros
NPASOS = 50
tpwm = 0.08
angPaso = -(2*math.pi)/NPASOS # Cambiar el signo segun el sentido de giro
th = 4 # threshold
ms = 1.5000
LIMZ = 22e-2 # Limite en m delo lejos que puede estar un punto

width = 320
height = 240
exp_time = 5000

centerx = width/2
centery = height/2
f = 3.04e-3   # Distancia focal [mm]
tampixel = (1.12e-6)*2592/width  # um
beta = 30.0 # grados
D = 19.8e-2 # Cm

vx = math.sin((90-beta)*math.pi/180)
vz = math.cos((90-beta)*math.pi/180)

### Vectores
vpm = np.zeros((height))  # vector con los puntos tras hacer la media de cada fila
vp = np.zeros((height,3))  # Vector de puntos calculados repecto al sistema 
                           # de referencia de la camara
vpg = np.zeros((height,3)) # vp resecto al centro de giro
npt = 0 # Numero total de puntos procesados
vpc = np.zeros((height*NPASOS,3))   # Vector de puntos completo respecto al centro de giro

### Configuracion PWM
# Direcciones de pines respecto a la numeracion de la placa
GPIO.setmode(GPIO.BOARD)

# El pin PWM debe ser configurado como pin de salida
GPIO.setup(18,GPIO.OUT)

# Se crea el objeto PWM (pasandole la frencuencia y el pin de salida)
pwm = GPIO.PWM(18,50)

# Calculo del duty cycle
dc = 100-(ms*5)

### Configuracion de la camara
camera = PiCamera()
camera.resolution = (width,height)
camera.shutter_speed = exp_time
camera.awb_gains = 1,1
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(width,height))

### Comienza el escaneo
k = 0
while k < NPASOS:
    if k == 0:
        pwm.start(dc)
        pwm.stop()
        time.sleep(tpwm)
    else:
        pwm.start(dc)
        time.sleep(tpwm)
        pwm.stop()    
    
    ### Captura de la imagen
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    rawCapture.truncate(0)
    
    ### ------ Procesado de la imagen ------
    
    # Se pasa la imagen a escala de grises
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    # Se Pasa la imagen por un umbral
    ret,imabin = cv2.threshold(gray,th,255,cv2.THRESH_BINARY)
    
    # Se calcula la media de posicion de cada fila y se guarda en un vector para luego
    # ser procesados los valores
    npfila = 0 
    media = 0
    for i in range(height):
        media = 0
        npfila = 0
        for j in range(width):
            if imabin[i,j] >= 255:
                media = media + j
                npfila = npfila + 1
        if npfila > 0:
            media = media/npfila
        else:
            media = 0
        vpm[i] = media        
    
    ### Reconstruccion 3D
    
    # Se recorren todos los puntos que deben ser reconstruidos y se calcula
    # su posicion XYZ respecto al sistema de referencia de la camara
    for i in range(height):
        if vpm[i] > 0:
            vp[i,2] = D/(1+vx*(tampixel*(vpm[i] - centerx))/(f*vz)) # coord z
            z = vp[i,2]
            vp[i,1] = -(tampixel*(i - centery))*z/f # coord y
            vp[i,0] = (tampixel*(vpm[i] - centerx))*z/f # coord x
            
            # No se procesan puntos demasiado lejanos
            if z < LIMZ:            
                vpg[i,2] = (vp[i,2] - D)
                vpg[i,1] = vp[i,1]
                vpg[i,0] = vp[i,0]          
                
                # Se guarda el punto en la lista de puntos procesados
                # Para ello deben girarse los puntos respecto al centro de giro
                # tanto como haya girado la plataforma
        
                # Se trata de un giro 2D (ejes Z y X, la Y permanece intacta)
                vpc[npt,0] = vpg[i,0]*math.cos(angPaso*k) - vpg[i,2]*math.sin(angPaso*k)   # x girada
                vpc[npt,1] = vpg[i,1]
                vpc[npt,2] = vpg[i,0]*math.sin(angPaso*k) + vpg[i,2]*math.cos(angPaso*k)   # z girada
                
                npt = npt + 1

    k = k+1
    print "%d" %k
    
#    ### Visualizacion de resultados
#    fig = plt.figure()
#    plt.hold(True)
#    ax = fig.gca(projection='3d')
#    ax.scatter(vpc[:,0],vpc[:,1],vpc[:,2])
#    
#    max_range = np.array([vpc[:,0].max()-vpc[:,0].min(),vpc[:,1].max()-vpc[:,1].min(),vpc[:,2].max()-vpc[:,2].min()]).max()/2.0
#    
#    mid_x = (vpc[:,0].max()+vpc[:,0].min())*0.5
#    mid_y = (vpc[:,1].max()+vpc[:,1].min())*0.5
#    mid_z = (vpc[:,2].max()+vpc[:,2].min())*0.5
#    ax.set_xlim(mid_x - max_range, mid_x + max_range)
#    ax.set_ylim(mid_y - max_range, mid_y + max_range)
#    ax.set_zlim(mid_z - max_range, mid_z + max_range)
#    
#    plt.show()

### Visualizacion de resultados
fig = plt.figure()
plt.hold(True)
ax = fig.gca(projection='3d')
ax.scatter(vpc[0:npt,0],vpc[0:npt,1],vpc[0:npt,2])

max_range = np.array([vpc[0:npt,0].max()-vpc[0:npt,0].min(),vpc[0:npt,1].max()-vpc[0:npt,1].min(),vpc[0:npt,2].max()-vpc[0:npt,2].min()]).max()/2.0

mid_x = (vpc[0:npt,0].max()+vpc[0:npt,0].min())*0.5
mid_y = (vpc[0:npt,1].max()+vpc[0:npt,1].min())*0.5
mid_z = (vpc[0:npt,2].max()+vpc[0:npt,2].min())*0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

plt.show()

### Se espera la pulscion de una tecla antes de salir
key = cv2.waitKey(0)

### Liberar recursos antes de cerrar
camera.close()
GPIO.cleanup()
