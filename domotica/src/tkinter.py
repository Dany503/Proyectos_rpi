from Tkinter import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)

servo = GPIO.PWM(29,50)
servo.start(2)

ventana = Tk()
ventana.wm_title("Domotica deii2MII")

def bombillaOnPress():
    print ("Bombilla encendida")
    GPIO.output(11,GPIO.LOW)
def bombillaOffPress():
    print ("Bombilla apagada")
    GPIO.output(11,GPIO.HIGH)

def enchufeOnPress():
    print ("Enchufe encendido")
    GPIO.output(18,GPIO.LOW)
def enchufeOffPress():
    print ("Enchufe apagado")
    GPIO.output(18,GPIO.HIGH)

def puertaOnPress():
    print ("Puerta abierta")
    servo.ChangeDutyCycle(8)
def puertaOffPress():
    print ("Puerta cerrada")
    servo.ChangeDutyCycle(2)

FramePrimario = Frame(ventana)
FramePrimario.grid(row=0,column=0,sticky=W+N,padx=20,pady=20)
FramePrimario.grid_columnconfigure(0)

label1=Label(FramePrimario,text="Domotica Deii2").grid(row=0,columnspan=2)


BombillaOn=Button(FramePrimario,text="Encender bombilla",command=bombillaOnPress,width=20)
BombillaOn.grid(row=1,column=0,padx=10,pady=2)

BombillaOff=Button(FramePrimario,text="Apagar bombilla",command=bombillaOffPress,width=20)
BombillaOff.grid(row=1,column=1,padx=10,pady=2)

EnchufeOn=Button(FramePrimario,text="Encender enchufe",command=enchufeOnPress,width=20)
EnchufeOn.grid(row=2,column=0,padx=10,pady=2)

EnchufeOff=Button(FramePrimario,text="Apagar enchufe",command=enchufeOffPress,width=20)
EnchufeOff.grid(row=2,column=1,padx=10,pady=2)

PuertaOn=Button(FramePrimario,text="Abrir puerta",command=puertaOnPress,width=20)
PuertaOn.grid(row=3,column=0,padx=10,pady=2)

PuertaOff=Button(FramePrimario,text="Cerrar puerta",command=puertaOffPress,width=20)
PuertaOff.grid(row=3,column=1,padx=10,pady=2)
    
ventana.mainloop()
