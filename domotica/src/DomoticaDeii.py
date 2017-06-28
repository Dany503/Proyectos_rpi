import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)

servo = GPIO.PWM(29,50)
servo.start(2) # Centrado es 7.5, menos de este valor gira hacia la derecha y al contrario

ser = serial.Serial("/dev/ttyAMA0")

try:
    while 1:
        read = ser.read()
        if read == '1':
            print("Apagando bombilla")
            GPIO.output(11,GPIO.HIGH)
        if read == '0':
            print("Encendiendo bombilla")
            GPIO.output(11,GPIO.LOW)
        if read == '3':
            print("Apagando enchufe")
            GPIO.output(18,GPIO.HIGH)
        if read == '2':
            print("Encendiendo enchufe")
            GPIO.output(18,GPIO.LOW)
        if read == '4':
            print("Abriendo puerta")
            servo.ChangeDutyCycle(8)
        if read == '5':
            print("Cerrando puerta")
            servo.ChangeDutyCycle(2)
            
except KeyboardInterrupt:
    print("Saliendo")
except:
    print("error")
finally:
    ser.close()
    servo.stop()
    GPIO.cleanup()
    
    
