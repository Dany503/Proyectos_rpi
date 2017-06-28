/*

------modifical los topics MQTT en el proyecto final, aqui hay chapuzas-----------

D0 ROJO, D1 AZUL y D2 VERDE se usan para el control del LED RGB
D3 se usara para el control del DIMMER
D4 se usará para el control del SERVO

Servo min 40
servo max 117

*/
#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#define SERVOMAX 117
#define SERVOMIN 50

const char* ssid = "CLAU07";                 //red a la que nos conectamos
const char* password = "Claudio91.";       //clave de la red
char* server = "192.168.1.3";              //direccion del servidor MQTT (no de OpenHAB)
char message_buff[20];                      //string donde guardar los mensajes

unsigned long previousMillis = 0;           //ultima vez que se actualizaron los datos
unsigned long previousMillis2 = 0;           //ultima vez que se actualizaron los datos de energia

const long intervalo = 100;                //refresco de la temp, presion, corriente, tension, potencia y energia consumida

char msgServo = 0;
int pos=117;


char buff[6];                             //Cadena donde almacenaremos el valor convertido

void callback(char* topic, byte* payload, unsigned int length) {    //funcion para el manejo de los mensajes MQTT

  int i = 0;

  for (i = 0; i < length; i++) {
    message_buff[i] = payload[i];     //almacenar el mensaje
  }

  message_buff[i] = '\0';             //finalizar el vector

  String msgString = String(message_buff);    
  String stopic = String(topic); 

    //escribir los valores PWM al RGB  

  if (stopic == "dev/RED") analogWrite(D2, msgString.toInt() * 10); 
  if (stopic == "dev/GREEN") analogWrite(D1, msgString.toInt() * 10);
  if (stopic == "dev/BLUE") analogWrite(D0, msgString.toInt() * 10);
  
  //recepcion de la orden del servo
  
  if (stopic == "dev/servo" && msgString == "UP")  msgServo = 1;
  else if (stopic == "dev/servo" && msgString == "DOWN")  msgServo = 2;
  else if (stopic == "dev/servo" && msgString == "STOP")  msgServo = 0;
    
  if (stopic == "dev/slid") analogWrite(D3, msgString.toInt() * 10);

}

WiFiClient wifiClient;        //crear un cliente wifi
PubSubClient client(server, 1883, callback, wifiClient);      //conexion al servidor


void setup() {

  Serial.begin(115200);
  delay(10);
    
  analogWriteFreq(60);
  analogWrite(D4, pos);

  pinMode(D0, OUTPUT);
  digitalWrite(D0, 0);
  pinMode(D1, OUTPUT);
  digitalWrite(D1, 0);
  pinMode(D2, OUTPUT);
  digitalWrite(D2, 0);
  pinMode(D3, OUTPUT);
  digitalWrite(D3, 0);
  pinMode(D4, OUTPUT);
  digitalWrite(D4, 0);


  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {         //espera a que el dispositivo se conecte a la red
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());


  if (client.connect("arduinoClient2")) {                   //nos conectamos al servidor MQTT como "arduinoClient2"

    client.subscribe("dev/slid");   //nos suscribimos a dev/D
    client.subscribe("dev/RED");   // nos suscribimos a dev/D
    client.subscribe("dev/GREEN");   //nos suscribimos a dev/D
    client.subscribe("dev/BLUE");   //nos suscribimos a dev/D
    client.subscribe("dev/servo");   //nos suscribimos a dev/D

  }
}

void loop() {

  client.loop();      //hay que ejecutarlo continuamente para recibir mensajes

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalo && msgServo == 2) {  //actualiza el valor del servo
    previousMillis = currentMillis;
    
    pos++;
    if(pos > SERVOMAX) pos=SERVOMAX;
    
    analogWrite(D4, pos);
    Serial.println(pos, DEC);

  }
  
    if (currentMillis - previousMillis >= intervalo && msgServo ==1) {  //actualiza el valor del servo
    previousMillis = currentMillis;
    
    pos--;
    if(pos < SERVOMIN) pos=SERVOMIN;
    
    analogWrite(D4, pos);
    Serial.println(pos, DEC);

  }

}


