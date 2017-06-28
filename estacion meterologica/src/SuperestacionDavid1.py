#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib2
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from sense_hat import SenseHat

# Oauth JSON File. Archivo JSON
GDOCS_OAUTH_JSON       = 'Raspberry pi-abdbfa45e6bf.json'

# Google Docs spreadsheet nombre del archivo.
GDOCS_SPREADSHEET_NAME = 'raspberry'

# Tiempo entre medidas en segundos.
FREQUENCY_SECONDS      = 30


def login_open_sheet(oauth_key_file, spreadsheet):
        """Conecta con Google Docs spreadsheet y devuelve el primer worksheet."""
        try:
                json_key = json.load(open(oauth_key_file))
                credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                json_key['private_key'],
                ['https://spreadsheets.google.com/feeds'])
                gc = gspread.authorize(credentials)
                worksheet = gc.open(spreadsheet).sheet1
                return worksheet
        except Exception as ex:
                print 'No se ha podido loguear. Revisa las OAuth credentials, el nombre del archivo, y asegurate de que esta compartido con la direccion de client_email en el archivo OAuth .json !'
                print 'Google sheet fallo con error en el login:', ex
                sys.exit(1)


sense = SenseHat()
sense.clear()           
print 'Guardando las medidas de los sensores en {0} cada {1} segundos.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Pulse Ctrl-C para parar el programa.'
worksheet = None
while True:
        # Si es necesario pedira login.
        if worksheet is None:
                worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

        # Recogemos los valores de los sensores.
        temp = sense.get_temperature()
        temp = round(temp, 1)
        humidity = sense.get_humidity()
        humidity = round(humidity, 1)
        pressure = sense.get_pressure()
        pressure = round(pressure, 1)

        # Joystick
        joyst = sense.stick.get_events()
        direccionjoy = joyst.event.direction
        if direccionjoy == up:
                info4 = 'Temperatura up (C): ' + str(temp)
                sense.show_message(info4, text_colour=[255, 0, 255]) # Rojo

        # Pantalla 8x8 RGB
        sense.clear()
        info = 'Temperatura (C): ' + str(temp) 
        sense.show_message(info, text_colour=[255, 0, 0]) # Rojo
        info2 = 'Humedad: ' + str(humidity) 
        sense.show_message(info2, text_colour=[255, 255, 0]) # Amarillo
        info3 =  'Presion: ' + str(pressure)
        sense.show_message(info3, text_colour=[0, 255, 255]) # Azul
        # Print en el SHELL de la Raspberry
        print "La Temperatura ambiente (C) es de: ", temp
        print "La Humedad es de: ", humidity
        print "La Presión es de: ", pressure, "\n"

        # Append the data in the spreadsheet, including a timestamp
        try:
                worksheet.append_row((datetime.datetime.now(), temp,humidity,pressure))
        except:
                # Error appending data, most likely because credentials are stale.
                # Null out the worksheet so a login is performed at the top of the loop.
                print 'Append error, logging in again'
                worksheet = None
                time.sleep(FREQUENCY_SECONDS)
                continue

        # Espera 30 segundos antes de continuar
        print 'Se introdujo una nueva fila con los datos en el archivo {0}'.format(GDOCS_SPREADSHEET_NAME)
        time.sleep(FREQUENCY_SECONDS)
