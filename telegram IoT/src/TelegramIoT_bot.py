# ----------------------------------------------------------------------------------
# -- Company: UNIVERSIDAD DE SEVILLA
# -- Engineer: TERESA ARAUZ PISON & JAVIER NUNEZ SANCHEZ
# --
# -- Create Date:    30/01/2017
# -- Design Name:
# -- Module Name:    TelegramIoT_bot
# -- Project Name:	 Proyecto DEII MII
# -- Description:
# -- Dependencies:
# --
# -- Revision:
# -- Revision 0.01 - File Created
# -- Additional Comments:
# --
# ----------------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
from picamera import PiCamera
from sense_hat import SenseHat
from time import sleep
import RPi.GPIO as GPIO
import threading

import string
string.punctuation 

sense=SenseHat()

bot = telebot.TeleBot("xxxxxxx")
knownUsers = []  # todo: save these in a file,

user_dict = {}
umbral=[]
camera_flag =0
class User:
    def __init__(self, name):
        self.name = name
	self.camera = None
	self.alarma = None
	self.msg = None
        self.log = None
		
		
# userStep = {}  # so they won't reset every time the bot restarts

# ====== DEFINICION DE PINES ==========
cocina=7
check_cocina=8
entrada=11
check_entrada=12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cocina,GPIO.OUT)
GPIO.setup(check_cocina,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(entrada,GPIO.OUT)
GPIO.setup(check_entrada,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# ===========================
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
#imageSelect.add('Hola', 'Adios')
itembtn1 = types.KeyboardButton('Luces')
itembtn2 = types.KeyboardButton('Imagen')
itembtn3 = types.KeyboardButton('Sensores')
itembtn4 = types.KeyboardButton('Mensaje')
itembtn5 = types.KeyboardButton('Usuarios Conectados')
markup.row(itembtn1,itembtn2)
markup.row(itembtn3,itembtn4)
markup.row(itembtn5)

luces = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
luz_on = types.KeyboardButton('Encender una Luz')
luz_off = types.KeyboardButton('Apagar una Luz')
luz_st = types.KeyboardButton('Comprobar Luces')
luz_return = types.KeyboardButton('Inicio')
luces.row(luz_on)
luces.row(luz_off)
luces.row(luz_st)
luces.row(luz_return)

hab = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
hab_1 = types.KeyboardButton('Cocina')
hab_2 = types.KeyboardButton('Entrada')
hab.row(hab_1, hab_2)
hab.row(luz_return)

sensores = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
ver = types.KeyboardButton('Ver valores')
umb = types.KeyboardButton('Cambiar Umbral Alarma')
sensores.row(ver)
sensores.row(umb)
sensores.row(luz_return)

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

def alarma_th():
	while 1:
		sleep(5)
		comp_temp=sense.get_temperature_from_humidity()
		if comp_temp > umbral[0]:
			for n in knownUsers:
				bot.send_message(n, "Alerta Temperatura ALTA !!!!!!")

@bot.message_handler(commands=['start'])
def command_start(message):
    cid = message.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
		msg = bot.reply_to(message, "Hola !! Eres nuevo --> Password ??",reply_markup=hideBoard)
		bot.register_next_step_handler(msg, pass_step)
		
        # knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        # userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        # bot.send_message(cid, "Hello, stranger, let me scan you...")
        # bot.send_message(cid, "Scanning complete, I know you now")
        # command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "Usuario registrado")
			
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
	
	
def pass_step(message):
    try:
		cid = message.chat.id
		if message.text == 'J': 
			#userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
			# bot.send_message(cid, "Scanning complete, I know you now")
			print ('new user')
			name= str(message.chat.first_name) #  #
			print (name)
			user = User(name)
			print ('estructura para el usuario creada')
			user_dict[cid] = user
			print ('step2')
			user.log = 'ok'
			user.camara = 0;
			user.alarma = 0;
			user.msg = 0;
			bot.send_message(cid, name + ' login ok')
			print ('step3')
			knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
			for k in knownUsers:
				if k != cid:
					bot.send_message(k, name + ' SE HA CONECTADO')
				
			bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
			bot.register_next_step_handler(message, select_state)
			
		else:
			msg = bot.reply_to(message, "Password Incorrecto. Intentalo de nuevo")
			bot.register_next_step_handler(msg, pass_step)
		
		user_dict[cid].alarma = 1
		aux=0
		for n in knownUsers:
			if n!=cid :
				aux=aux+user_dict[n].camara
		
		if aux > 0 :
			user_dict[cid].alarma = 0
			bot.reply_to(message, 'Alarma ya atendida')
			bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
			bot.register_next_step_handler(message, select_state)	
		else :
			t = threading.Thread(target=alarma_th)
			umbral.append(30)
			t.start()
			# while 1:
				# sleep(5)
				# comp_temp=sense.get_temperature_from_humidity()
				# if comp_temp > umbral :
					# bot.send_message(cid, "Alerta Temperatura ALTA !!!!!!")
		
    except Exception as e:
        if message.text == 'J':
		#bot.reply_to(message, 'error')
			msg = bot.reply_to(message, "Nombre de usuario invalido")
			bot.register_next_step_handler(msg, pass_step)

		
def select_state(message):
	cid = message.chat.id
	if message.text == 'Luces': 
		bot.send_message(cid, "Que desea hacer", reply_markup=luces) 
		bot.register_next_step_handler(message, luz_select)
    	elif message.text == 'Imagen':
		user_dict[cid].camara = 1
		aux=0
		for n in knownUsers:
			print (n)
			if n!=cid :
				print (n)
				aux=aux+user_dict[n].camara
				
		
		if aux > 0 :
			user_dict[cid].camara = 0
			bot.reply_to(message, 'Camara ocupada')
			bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
			bot.register_next_step_handler(message, select_state)	
		else :
			#bot.reply_to(message, 'Abriendo Camara')
			camera = PiCamera()
			camera.resolution = (640,480)
			camera.rotation = 180
			#bot.reply_to(message, 'Tomando foto')
			camera.capture('/home/pi/imagen.jpg')
			camera.close()
			#bot.reply_to(message, 'Cargando la foto')
			photo = open('/home/pi/imagen.jpg', 'rb')
			#bot.reply_to(message, 'Foto Cargada')
			bot.send_photo(message.chat.id, photo)
			bot.reply_to(message, 'Aqui tienes la foto')
			user_dict[cid].camara = 0
			bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
			bot.register_next_step_handler(message, select_state)	
    	elif message.text == 'Sensores':
		bot.send_message(cid, "Que desea hacer", reply_markup=sensores) 
		bot.register_next_step_handler(message, sensor_select)
    	elif message.text == 'Mensaje':
		aux=0
		for n in knownUsers:
			aux=aux+user_dict[n].msg
		
		if aux > 0 :
			user_dict[cid].msg = 0
			bot.reply_to(message, 'Pantalla ocupada')
			bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
			bot.register_next_step_handler(message, select_state)
		else :
			user_dict[cid].msg = 1
			bot.send_message(cid, "Que desea esccribir ?")  # show the keyboard
			bot.register_next_step_handler(message, wait_msg)
    	elif message.text == 'Usuarios Conectados':
		bot.send_message(cid, " Usuarios conectados: ")
		for n in knownUsers:
			name=user_dict[n].name
			bot.send_message(cid, name)  # show the keyboard
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
    	else :
		bot.send_message(cid, "Menu Principal", reply_markup=markup)
		bot.register_next_step_handler(message, select_state)

def luz_select(message):
	bot.reply_to(message, 'opcion selecionada ' + message.text,reply_markup=hideBoard)
	cid = message.chat.id
	if message.text == 'Encender una Luz': 
		bot.send_message(cid, "Que habitacion desea encender", reply_markup=hab) 
		bot.register_next_step_handler(message, encender)
	elif message.text == 'Apagar una Luz':
		bot.send_message(cid, "Que habitacion desea apagar", reply_markup=hab) 
		bot.register_next_step_handler(message, apagar)
    	elif message.text == 'Comprobar Luces':
		res=GPIO.input(check_cocina)
		if res == 1:
			bot.send_message(cid, "Luz Cocina Encendida")
		else :
			bot.send_message(cid, "Luz Cocina Apagada")
			
		res=GPIO.input(check_entrada)
		if res == 1:
			bot.send_message(cid, "Luz Entrada Encendida")
		else :
			bot.send_message(cid, "Luz Entrada Apagada")
			
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
    	elif message.text == 'Inicio':
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	
    	else :
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
		
def  encender(message):	
    	cid = message.chat.id
	if message.text == 'Cocina': 
		GPIO.output(cocina,GPIO.HIGH)
		bot.send_message(cid,  message.text + " Encendida")
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)

	elif message.text == 'Entrada':
		GPIO.output(entrada,GPIO.HIGH)
		bot.send_message(cid,  message.text + " Encendida")
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
		
    	elif message.text == 'Inicio':
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	
    	else :
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
		
		
def  apagar(message):
	cid = message.chat.id
	if message.text == 'Cocina': 
		GPIO.output(cocina,GPIO.LOW)
		bot.send_message(cid,  message.text + " Apagada")
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)

	elif message.text == 'Entrada':
		GPIO.output(entrada,GPIO.LOW)
		bot.send_message(cid,  message.text + " Apagada")
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
		
    	elif message.text == 'Inicio':
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	
    	else :
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)

		
def wait_msg(message):
	cid = message.chat.id
	bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
	bot.register_next_step_handler(message, select_state)
	sense.show_message(message.chat.first_name + " dice: " + message.text)
	user_dict[cid].msg = 0
	
def wait_umbral(message):
	try:
		cid = message.chat.id
		umbral[0]=int(message.text)
		bot.send_message(cid, "Umbral cambiado a: %d" %umbral[0])
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)
    	except Exception as e:
        	bot.send_message(cid, "Mete un numero")
		bot.register_next_step_handler(message, wait_umbral)

	
def sensor_select(message):
	bot.reply_to(message, 'opcion selecionada ' + message.text,reply_markup=hideBoard)
	cid = message.chat.id
	if message.text == 'Ver valores': 
		Humedad=sense.get_humidity()
		Temp=sense.get_temperature_from_humidity()
		Presion=sense.get_pressure()
		bot.send_message(cid, "Humedad:  %2.3f" %Humedad )
		bot.send_message(cid, "Temperaturas: %2.3f" % Temp )
		bot.send_message(cid, "Presion: %4.2f" %Presion )
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	
	elif message.text == 'Cambiar Umbral Alarma':
			bot.send_message(cid, "Umbral actual: %d Inserte nuevo valor" %umbral[0])  # show the keyboard
			bot.register_next_step_handler(message, wait_umbral)
    	elif message.text == 'Inicio':
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	
    	else :
		bot.send_message(cid, "Menu Principal", reply_markup=markup)  # show the keyboard
		bot.register_next_step_handler(message, select_state)	


bot.polling()
print ('Mensaje enviado a ')
