# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO, time

from time import sleep

from picamera import PiCamera

GPIO.setmode(GPIO.BOARD)
exit = False

def timer (pin):
	cont = 0
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.setup(pin, GPIO.IN)
	while (GPIO.input(pin) == GPIO.LOW):
		cont += 1
        return cont

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 180
camera.start_preview(fullscreen=False, window=(30,30,320,240))

while not exit:
	LDR = timer(10)
        
	if LDR<300:

		sleep(3)
		camera.capture('/home/pi/imagen.jpg')
		camera.stop_preview() 
		camera.close()
                import pexpect
                
                contacto = "Agustín_Ramos_Hurtado"
                img = "/home/pi/imagen.jpg"                      #Imagen a enviar
                telegram = pexpect.spawn('./bin/telegram-cli -k tg-server.pub') #Inicia Telegram
                telegram.expect('\r\n>',timeout=2)                            #Espera a que termine de iniciar
                telegram.sendline('contact_list')
                time.sleep(2)                
                telegram.sendline("send_photo Agustín_Ramos_Hurtado /home/pi/imagen.jpg")#Ejecuta el comando send_photo
                telegram.sendline("msg Agustín_Ramos_Hurtado Atracador robando caja fuerte")                 
                telegram.expect('100',timeout = 1200)
                telegram.expect('photo')
                print ('Imagen enviada a '+contacto)            #Notifica que ya se ha mandado el mensaje
                telegram.expect('\r\n>',timeout=2) 
                telegram.sendline('quit')                        #Cierra el programa

		exit = True
            
	print (LDR)

