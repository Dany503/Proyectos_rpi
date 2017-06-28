# -*- coding: utf-8 -*-


import mosquitto, os, urlparse

#Define event callbacks
def on_connect(mosq, obj, rc):
	print("rc: " + str(rc))
	
def on_message(mosq, obj, msg):
	print(msg.topic +  " " + str(msg.qos) + " " + str(msg.payload))
	
def on_publish(mosq, obj, mid):
		print("mid: " + str(mid))
		
def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))
	
def on_log(mosq, obj, level, string):
	print(string)

mqttc = mosquitto.Mosquitto()
#Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncoment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)

# Connect
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)

import smtplib
from sense_hat import SenseHat
sense=SenseHat()
sense.clear()
bucle=True
contador=1000
while bucle:
	contador=contador-1
	Temp=sense.get_temperature()
	Hum=sense.get_humidity()
	Pres=sense.get_pressure()
	PStr=str(round(Pres,2))
	HStr=str(round(Hum,2))
	TStr=str(round(Temp,2))
	events = sense.stick.get_events()
	for event in events:
		if event.direction == "up" and event.action != "released":
			sense.show_message("P: " + PStr)
		if event.direction == "down" and event.action != "released":
			sense.show_message("H: " + HStr)
		if event.direction == "right" and event.action != "released":
			sense.show_message("T: " + TStr)
		if event.direction == "middle":
			bucle=False
			
	print("Temperatura: %2.2f ºC" % (Temp))
	print("Presion: %2.2f bar" % (Pres))
	print("Humedad: %2.2f" % (Hum))
	
	if contador==0:
		mqttc.publish("dev/Presion", PStr)
		mqttc.publish("dev/Hum", HStr)
		mqttc.publish("dev/Temp", TStr)
		
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login ("practicaraspberry@gmail.com", "practicaraspberry2017")
		
		msg = TStr
		server.sendmail("practicaraspberry@gmail", "practicaraspberry@gmail", msg)
		server.quit()
		contador=1000
	
	clear()