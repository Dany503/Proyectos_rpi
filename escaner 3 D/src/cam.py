from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

### Configuracion de la camara
camera = PiCamera()
camera.resolution = (160,120)
camera.shutter_speed = 5000
camera.awb_gains = 1,1
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(160,120))

### Captura de la imagen
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
rawCapture.truncate(0)


### ------ Procesado de la imagen ------

# Parametros
th = 4 # threshold

# Se pasa la imagen a escala de grises
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Se Pasa la imagen por un umbral
ret,imabin = cv2.threshold(gray,th,255,cv2.THRESH_BINARY)

# Se calcula la media de posicion de cada fila y se guarda en un vector para luego
# ser procesados los valores
[height, width] = imabin.shape
npfila = 0 
vpm = np.zeros((height))  # vector con los puntos tras hacer la media de cada fila
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
    
#print vpm
        

### Reconstruccion 3D

# Parametros
centerx = width/2
centery = height/2
f = 3.04e-3   # Distancia focal [mm]
tampixel = (1.12e-6)*2592/width  # um
beta = 30.0 # grados
D = 19.8e-2 # Cm

# Calculo de parametros del algoritmo
vx = math.sin((90-beta)*math.pi/180)
vz = math.cos((90-beta)*math.pi/180)

# Se recorren todos los puntos que deben ser reconstruidos y se calcula
# su posicion XYZ respecto al sistema de referencia de la camara
vp = np.zeros((height,3))  # Vector de puntos calculados repecto al sistema 
                           # de referencia de la camara
vpg = np.zeros((height,3))
for i in range(height):
    if vpm[i] > 0:
        vp[i,2] = D/(1+vx*(tampixel*(vpm[i] - centerx))/(f*vz)) # coord z
        z = vp[i,2]
        vp[i,1] = -(tampixel*(i - centery))*z/f # coord y
        vp[i,0] = (tampixel*(vpm[i] - centerx))*z/f # coord x
        
        vpg[i,2] = (vp[i,2] - D)
        vpg[i,1] = vp[i,1]
        vpg[i,0] = vp[i,0]

### Visualizacion de resultados
# Visualizacion 3D


# Imagenes        
plt.subplot(2,2,1)
plt.imshow(image)
plt.title("Imagen Original")

plt.subplot(2,2,2)
plt.imshow(gray, 'gray')
plt.title("Escala de grises")

plt.subplot(2,2,3)
plt.imshow(imabin, 'gray')
plt.title("Imagen umbralizada")
plt.show()

fig = plt.figure()
plt.hold(True)
ax = fig.gca(projection='3d')

NPASOS = 1
vpc = np.zeros((height*NPASOS,3))   # Vector de puntos completo respecto al centro de giro
angPaso = -(2*math.pi)/NPASOS # Cambiar el signo segun el sentido de giro

k = 0
for k in range(NPASOS):
    # Se trata de un giro 2D (ejes Z y X, la Y permanece intacta)
    lowlim = k*height
    uplim = (k+1)*height
    
    vpc[lowlim:uplim,0] = vpg[:,0]*math.cos(angPaso*k) - vpg[:,2]*math.sin(angPaso*k)   # x girada
    vpc[lowlim:uplim,1] = vpg[:,1]                                                  # y intacta
    vpc[lowlim:uplim,2] = vpg[:,0]*math.sin(angPaso*k) + vpg[:,2]*math.cos(angPaso*k)   # z girada


ax.scatter(vpc[:,0],vpc[:,1],vpc[:,2])

max_range = np.array([vpc[:,0].max()-vpc[:,0].min(),vpc[:,1].max()-vpc[:,1].min(),vpc[:,2].max()-vpc[:,2].min()]).max()/2.0

mid_x = (vpc[:,0].max()+vpc[:,0].min())*0.5
mid_y = (vpc[:,1].max()+vpc[:,1].min())*0.5
mid_z = (vpc[:,2].max()+vpc[:,2].min())*0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)


plt.show()



### Se espera la pulscion de una tecla antes de salir
key = cv2.waitKey(0)

### Liberar recursos antes de cerrar
camera.close()
