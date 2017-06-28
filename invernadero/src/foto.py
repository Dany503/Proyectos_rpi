from picamera import PiCamera
from time import sleep
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

camera = PiCamera()
camera.resolution = (640,480)
camera.rotation = 180
camera.start_preview(fullscreen=False, window=(30,30,320,240))
for i in range(0,5):
    print 5-i
    sleep(1)

camera.capture('/home/pi/imagen.jpg')
camera.stop_preview()
camera.close()

direccion_fuente = "proyectoberrypi1617@gmail.com"
direccion_destino = "manuel.jimenez.93@gmail.com"

 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(direccion_fuente, "disman44")


msg = MIMEMultipart()
msg['From'] = direccion_fuente
msg['To'] = direccion_destino
msg['Subject'] = "FOTOGRAFIA INVERNADERO"

cuerpo_mensaje = "INVERNADERO"
msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

 
archivo = "/home/pi/imagen.jpg"
adjunto = open(archivo, "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((adjunto).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % archivo)
msg.attach(part)

texto = msg.as_string()
print texto

try:
    print "Enviando email"
    print server.sendmail(direccion_fuente, direccion_destino, texto)
except:
    print "Error al enviar el email"
    server.quit()
    
server.quit()

