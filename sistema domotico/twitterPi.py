from twython import Twython
import os
from auth import(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

orden = { "temp_humedad" : 1,
          "temp_pres" : 2,
          "humedad" : 3,
          "presion" : 4,
          "foto" : 5,
          "todo" : 6,
          "encender_calefactor":7,
          "apagar_calefactor":8
         }

class manejo_twitter:
   
    """Clase que maneja twitter"""
    authTwitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
      )
    tweet_anterior = str()
    #constructor de la clase
    def __init__(self): 
          self.tweet_anterior = "sin leer"
          
        
    def update_status(self):
        print("entra")
        a = self.authTwitter.get_user_timeline(screen_name = "@ordenesmierapi", count = 10)
        print("sigue")
        for tweet in a:
            if (tweet['text'].find("@MieraPi1617") != -1):
                
                if self.tweet_anterior != tweet['text']:
                    print(tweet['text'])
                    nueva_orden = open(os.getcwd() + "/leido.txt",'w')
                    nueva_orden.write(tweet['text'])
                    nueva_orden.close()
                    self.tweet_anterior = tweet['text']
                    return 1
                else:
                    print("else")
                    return 0
            else:
                return 0
            print("no entra if")
    

    def escribir_resultado(self,orden = 0):

        if (orden == 6): #Mandamos datos e imagenes
            sensPres = open( os.getcwd()  +"/Presion.txt", 'r')
            self.authTwitter.update_status(status = sensPres.read())
            sensPres.close()
            sensHum = open(os.getcwd() +"/Humedad.txt", 'r')
            self.authTwitter.update_status(status = sensHum.read())
            sensHum.close()
            sensTempPres = open(os.getcwd() +"/TempPresion.txt", 'r')
            self.authTwitter.update_status(status = sensTempPres.read())
            sensTempPres.close()            
            sensTempHum = open(os.getcwd() +"/TempHumedad.txt", 'r')
            self.authTwitter.update_status(status=sensTempHum.read())
            sensTempHum.close()
            photo = open(os.getcwd() +"/image.jpg", 'rb')
            self.authTwitter.update_status_with_media(status="@ordenesmierapi", media=photo)
            photo.close()
                
        elif (orden == 5):#Mandamos solo imagenes
                photo = open(os.getcwd() +"/image.jpg", 'rb')
                self.authTwitter.update_status_with_media(status="@ordenesmierapi", media=photo)
                photo.close()
        elif (orden == 4):#Sensor de Presión
                 sensPres = open( os.getcwd()  +"/Presion.txt", 'r')
                 self.authTwitter.update_status(status = sensPres.read())
                 sensPres.close()
        elif (orden == 3):#Sensor de Humedad
                 sensHum = open(os.getcwd() +"/Humedad.txt", 'r')
                 self.authTwitter.update_status(status = sensHum.read())
                 sensHum.close()
        elif (orden == 2):#Sensor de Temperatura a partir de la Presion
                 sensTempPres = open(os.getcwd() +"/TempPresion.txt", 'r')
                 self.authTwitter.update_status(status = sensTempPres.read())
                 sensTempPres.close()
        elif (orden == 1):#Sensor de Temperatura a partir de la Humedad              
                 sensTempHum = open(os.getcwd() +"/TempHumedad.txt", 'r')
                 self.authTwitter.update_status(status=sensTempHum.read())
                 sensTempHum.close()

    def leer_ordenes(self):
        ordenes_leidas = open(os.getcwd() +"/leido.txt",'r')
        #Dividimos el tweet en todas las palabras que lo componen
        ordenes = ordenes_leidas.read().split()
        print(ordenes)
        count = 0
        sumatorio = 0

        for i in ordenes:
            #Buscamos la palabra en nuestro diccionario. Si no está saltará una excepción
            #pero la ignoramos y seguimos buscando.
            #Al final tendremos un sumatorio de las órdenes y el número de encuentros.
            try:
                if orden[i]:
                    count = count +1
                    sumatorio = sumatorio + orden[i]
            except:
                continue

        #Éste será el valor devuelto
        if count > 0:
            if (sumatorio % count): #Si es distinto de 0 el resto nos están pidiendo información de ambos dispositivos.
                print(sumatorio % count)
                return (6)
            else:   #Nos están pidiendo solo un dato
                print (sumatorio / count)
                return(sumatorio / count)       
