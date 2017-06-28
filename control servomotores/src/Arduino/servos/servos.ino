#include <Servo.h> //librería para poder usar servos

//int LED=13;
//Variables para escribir en Servo
int AI=0; //alerón izquierto
int AD=0; //alerón derecho
int TD=0; //timón de dirección
int TP=0; //timón de profundidad

//Variables para detectar cambios
int AI_new=0; //alerón izquierto
int AD_new=0; //alerón derecho
int TD_new=0; //timón de dirección
int TP_new=0; //timón de profundidad

//Pines de comunicación con Raspberry
int TP_RPi = A0;
int TD_RPi = A1;
int AD_RPi = A2;
int AI_RPi = A3;

//Variables de lectura
int TP_read = 0;
int TD_read = 0;
int AD_read = 0;
int AI_read = 0;


//#define centro 90 //sin desplegar, posición central 90º
//#define Apos 90+21 //alerón hacia arriba
//#define Aneg 90-21//alerón hacia abajo
//#define TDpos 90+30 //Timón de dirección hacia la derecha
//#define TDneg 90-30//Timón de dirección hacia la izquierda
//#define TPpos 90-40//Timón de profundidad hacia arriba
//#define TPneg 90+20//Timón de profundidad hacia abajo

#define centro 90 //sin desplegar, posición central 90º
#define Apos 90+15 //alerón hacia arriba
#define Aneg 90-15//alerón hacia abajo
#define TDpos 90+3 //Timón de dirección hacia la derecha
#define TDneg 90-15//Timón de dirección hacia la izquierda
#define TPpos 90//Timón de profundidad hacia arriba
#define TPneg 90-12//Timón de profundidad hacia abajo

//Creación variables servos
Servo sAI; //alerón izquierdo
Servo sAD; //alerón derecho
Servo sTD; //timón de dirección
Servo sTP; //timón de profundidad

void setup() {
  // inicializar puerto serie
  Serial.begin(9600); //9600 es la velocidad de la comunicación serie en baudios
  //pinMode(LED,OUTPUT);
  
  //definición de los pines donde están conectados los servos
  sAI.attach(9);
  sAD.attach(10);
  sTD.attach(11);
  sTP.attach(12);

  pinMode(TP_RPi,INPUT);
  pinMode(TD_RPi,INPUT);
  pinMode(AD_RPi,INPUT);
  pinMode(AI_RPi,INPUT);

  sAI.write(90);
  sAD.write(90);
  sTP.write(90);
  sTD.write(90);
}

void loop() {

//Lectura de entradas analógicas  
    TP_read = analogRead(TP_RPi);
    TD_read = analogRead(TD_RPi);
    AD_read = analogRead(AD_RPi);
    AI_read = analogRead(AI_RPi);

//Lógica de decisión
    //Timón de profundidad
    if(TP_read>600){
      TP_new=TPpos;}
    else{
      TP_new=TPneg;
      }
    TP_new=constrain(TP_new,0,180); //limitamos el valor a 0-180 para proteger el servo

    //Timón de dirección
    if(TD_read>600){
      TD_new=TDpos;}
      else{
      TD_new=TDneg;
      }
    TD_new=constrain(TD_new,0,180); //limitamos el valor a 0-180 para proteger el servo

    //Alerón derecho
    if(AD_read>600){
      AD_new = Aneg;}
      else{
      AD_new = Apos;
      }
    AD_new=constrain(AD_new,0,180); //limitamos el valor a 0-180 para proteger el servo

    //Alerón izquierdo
    if(AI_read>600)
    {
      AI_new = Apos;
    }
    else
    {
      AI_new = Aneg;
    }
    AI_new=constrain(AI_new,0,180); //limitamos el valor a 0-180 para proteger el servo
    
//Escritura en los servos. Sólo en caso de que el valor cambie
  if(AI_new != AI)
  {
    sAI.write(AI_new);
    AI = AI_new;
  }

  if(AD_new != AD)
  {
    sAD.write(AD_new);
    AD = AD_new;
  }

  if(TD_new != TD)
  {
    sTD.write(TD_new);
    TD = TD_new;
  }

  if(TP_new != TP)
  {
    sTP.write(TP_new);
    TP = TP_new;
  }

  delay(20);
}
