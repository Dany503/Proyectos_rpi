from sense_hat import SenseHat
from picamera import PiCamera
import datetime
import os

class sens_TempHumdd:
    sense = SenseHat()
    calefactor_encendido = int
    def _init_(self):          
        calefactor_encendido = 0
        temperatura = 0
        TempStr = "0.0"
     
    def tomar_medida(self):
        self.temperatura = self.sense.get_temperature_from_humidity()
        self.TempStr=str(round(self.temperatura,2))
        print(self.temperatura)

        self.sense.show_message(("T1:"+self.TempStr),text_colour=[255,000,000])

##    def chequeo_temperatura(self):
##        if (self.temperatura < 22):
##            self.calefactor_encendido = 1
##            #añadir pin a encender
##        else:
##            self.calefactor_encendido = 0
##            #añadir pin a apagar
            
    def guardar_medida(self):
        file = open(os.getcwd() + "/TempHumedad.txt", 'w')
        file.write("@ordenesmierapi")
        today=datetime.date.today()
        now=datetime.datetime.now().strftime("%H:%M")
        file.write("\n"+str(today)+"\n"+str(now)+"\nTemperatura = "+self.TempStr +" ºC")
        file.close()

class sens_TempPres:
    sense = SenseHat()
    calefactor_encendido = int
    def _init_(self):          
        calefactor_encendido = 0
        temperatura = 0
        TempStr = "0.0"
    
    def tomar_medida(self):
        self.temperatura=self.sense.get_temperature_from_pressure()
        self.TempStr=str(round(self.temperatura,2))
        self.sense.show_message("T2:"+self.TempStr,text_colour=[000,255,000])

##    def chequeo_temperatura(self):
##        if (self.temperatura < 22):
##            self.calefactor_encendido = 1
##            #añadir pin a encender
##        else:
##            self.calefactor_encendido = 0
##            #añadir pin a apagar
            
    def guardar_medida(self):
        file = open(os.getcwd() +"/TempPresion.txt", "w")
        file.write("@ordenesmierapi")
        today=datetime.date.today()
        now=datetime.datetime.now().strftime("%H:%M")
        file.write("\n"+str(today)+"\n"+str(now)+"\nTemperatura = "+self.TempStr +" ºC")
        file.close()

class sens_Humedad:
    sense = SenseHat()
    def _init_(self):          
        Humedad = 0
        HumStr = "0.0" 
    
    def tomar_medida(self):
        self.Humedad=self.sense.get_humidity()
        self.HumStr=str(round(self.Humedad,2))
        self.sense.show_message("H:"+self.HumStr,text_colour=[000,000,255])
        
    def guardar_medida(self):
        file = open(os.getcwd() +"/Humedad.txt", "w")
        file.write("@ordenesmierapi")
        today=datetime.date.today()
        now=datetime.datetime.now().strftime("%H:%M")
        file.write("\n"+str(today)+"\n"+str(now)+"\nHumedad = "+self.HumStr +" %")
        file.close()

class sens_Presion:
    sense = SenseHat()
    def _init_(self):          
        Presion = 0
        PresStr = "0.0" 
    
    def tomar_medida(self):
        self.Presion=self.sense.get_pressure()
        self.PresStr=str(round(self.Presion,2))
        self.sense.show_message("P:"+self.PresStr,text_colour=[255,255,255])
        
    def guardar_medida(self):
        file = open(os.getcwd() +"/Presion.txt", "w")
        file.write("@ordenesmierapi")
        today=datetime.date.today()
        now=datetime.datetime.now().strftime("%H:%M")
        file.write("\n"+str(today)+"\n"+str(now)+"\nPresion = "+self.PresStr +" Bar")
        file.close()

class ctrl_Camara:
      
      camera = PiCamera()
      
      def tomar_foto(self):         
          Image = os.getcwd() +"/image.jpg"        
          self.camera.capture(Image)                            

        
      

