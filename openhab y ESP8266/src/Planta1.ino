#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#include <SPI.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK 14
#define BMP_MISO 15
#define BMP_MOSI 12
#define BMP_CS 13

Adafruit_BMP280 bme(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);      //inicio de conexion al sensor de pres/temp por SPI

const char* ssid = "CLAU07";                 //red a la que nos conectamos
const char* password = "Claudio91.";         //clave de la red
char* server = "192.168.1.3";              //direccion del servidor MQTT (no de OpenHAB)
char message_buff[20];                      //string donde guardar los mensajes 

unsigned long previousMillis = 0;           //ultima vez que se actualizaron los datos
unsigned long previousMillis2 = 0;           //ultima vez que se actualizaron los datos de energia

const long intervalo = 2000;                //refresco de la temp, presion, corriente, tension, potencia y energia consumida
const long calculoenergia = 10;             //intervalo computo energia (cuanto mas pequeño mas precisa la medida)

char buff[6];                             //Cadena donde almacenaremos el valor convertido

float presion = 0.0;
float temperatura = 0.0;
float tension = 0.0;
float corriente = 0.0;
float potencia = 0.0;
float energia = 0.0;

void callback(char* topic, byte* payload, unsigned int length) {    //funcion para el manejo de los mensajes MQTT
  
    int i = 0;
  
  for(i=0; i<length; i++) {
    message_buff[i] = payload[i];     //almacenar el mensaje
  }

  message_buff[i] = '\0';             //finalizar el vector

  String msgString = String(message_buff);    
  String stopic = String(topic);              

  if(stopic == "dev/D0" && msgString == "ON" ) digitalWrite(D0, 1);      //manejo del led 1
  if(stopic == "dev/D0" && msgString == "OFF" ) digitalWrite(D0, 0);
  if(stopic == "dev/D1" && msgString == "ON" ) digitalWrite(D1, 1);      //manejo del led 1
  if(stopic == "dev/D1" && msgString == "OFF" ) digitalWrite(D1, 0);
  if(stopic == "dev/D2" && msgString == "ON" ) digitalWrite(D2, 1);      //manejo del led 1
  if(stopic == "dev/D2" && msgString == "OFF" ) digitalWrite(D2, 0);

}
 
WiFiClient wifiClient;        //crear un cliente wifi
PubSubClient client(server, 1883, callback, wifiClient);      //conexion al servidor
 
 
void setup() {

  Wire.begin(0, 2); //pin D3 es DATA y pin D4 es CLK
  Wire.beginTransmission(0x4c);   //direccion del PAC1720

  //configuracion de registros del PAC1720
  
  writeregister(0x00,0x18);
  writeregister(0x01,0x03);
  writeregister(0x03,0x0F);
  writeregister(0x0A,0x0F);
  writeregister(0x0B,0x5A);

  
  Serial.begin(115200);
  delay(10);
 
  pinMode(D0, OUTPUT);
  digitalWrite(D0, 0);  
  pinMode(D1, OUTPUT);   
  digitalWrite(D1, 0);  
  pinMode(D2, OUTPUT); 
  digitalWrite(D2, 0); 
 
  
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  bme.begin();
  
  while (WiFi.status() != WL_CONNECTED) {         //espera a que el dispositivo se conecte a la red
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
  
  if (client.connect("arduinoClient")) {                   //nos conectamos al servidor MQTT con usuario "arduinoClient"
       
    client.subscribe("dev/D0");   //nos suscribimos a dev/D
    client.subscribe("dev/D1");   // nos suscribimos a dev/D
    client.subscribe("dev/D2");   //nos suscribimos a dev/D
    
  }
}
 
void loop() {

  client.loop();      //hay que ejecutarlo continuamente para recibir mensajes
  
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalo){     //enviamos al servidor si ha pasado el tiempo de refresco de la info
        
    previousMillis = currentMillis;

    presion=bme.readPressure()/100;
    dtostrf(presion,4,2,buff);          //hay que convertir a texto antes de enviar
    client.publish("dev/press",buff);   //publicamos la informacion en el topic indicado

    temperatura=bme.readTemperature();
    dtostrf(temperatura,4,2,buff);      //hay que convertir a texto antes de enviar
    client.publish("dev/temp",buff);    //publicamos la informacion en el topic indicado

    tension = ((float)(readregister(0x11)*8.0) + (float)(readregister(0x12)/32.0))*39.98/2048.0;  //obtencion de la tension
    dtostrf(tension,4,2,buff);      //hay que convertir a texto antes de enviar
    client.publish("dev/tension",buff);    //publicamos la informacion en el topic indicado

    corriente = ((float)(readregister(0x0D)*16.0) + (float)(readregister(0x0E)/16.0))*8.0/2048.0;   //obtencion de la corriente
    dtostrf(corriente,4,2,buff);      //hay que convertir a texto antes de enviar
    client.publish("dev/corriente",buff);    //publicamos la informacion en el topic indicado

    dtostrf(potencia,4,2,buff);      //hay que convertir a texto antes de enviar
    client.publish("dev/potencia",buff);    //publicamos la informacion en el topic indicado
    
    dtostrf(energia,4,2,buff);      //hay que convertir a texto antes de enviar
    client.publish("dev/energia",buff);    //publicamos la informacion en el topic indicado
           
  }

  
  if(millis() - previousMillis2 >= 10){  //calcula la energia consumida hasta el momento

    previousMillis2 = millis();

    float energiaperiodo = 0.0;
    
    potencia = ((float)(readregister(0x15)*256.0) + (float)readregister(0x16))*319.84/65535.0;  //obtencion de la potencia
    energiaperiodo = potencia * 10.0;      //en Wms
    energia = energiaperiodo/(3600.0 * 1000.0) + energia;   //conversion a Wh
    
  }
  
}

char readregister(char direccion){      //lectura del PAC1720

  char devolver=0;

  Wire.beginTransmission(0x4c); 
  Wire.write(direccion);
  Wire.endTransmission();
  
  Wire.requestFrom(0x4c, 1);
  devolver = Wire.read();
  Wire.endTransmission();

  return devolver;
  
}

void writeregister(char direccion, char dato){      //escritura del PAC1720

  Wire.beginTransmission(0x4c);   //write to device
  Wire.write(direccion);
  Wire.write(dato);
  Wire.endTransmission();
  
}

