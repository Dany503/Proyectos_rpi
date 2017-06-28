import matplotlib.pyplot as plt
from time import sleep
from sense_hat import SenseHat
import smtplib

sense = SenseHat()

plt.ion()	

while True:
    temp_list = []
    x = []

    for a in range(20):

        temp = sense.get_temperature()
        temp_list.append(temp)

        print(temp)

        x.append(a)

        sleep(1)

    plt.clf()
    plt.plot(x,temp_list,'r')
    plt.title(u"MONITOR DE TEMPERATURA")
    plt.xlabel("Tiempo")
    plt.ylabel(u"Temperatura")
    plt.ylim(20,35)
    plt.draw()
    plt.savefig("fig1.png")

    if temp>30:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("proyectoberrypi1617@gmail.com", "disman44")
 
	msg = "ALERTA!"
	server.sendmail("proyectoberrypi1617@gmail.com", "manuel.jimenez.93@gmail.com", msg)

	server.quit()
