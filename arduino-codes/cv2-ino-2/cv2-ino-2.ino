
int pinLed = 13, relay = 4;
int pinInit = 5, pinLast = 9; // todos continuos
String data = ""; 

// fotocelda
int LDR = A0;  //Pin análogo en donde va conectada la fotocelda
int Led = 11;  //Pin PWM donde va conectado el LED
int LDR_valor = 0;

int trigPin = 13;
int echoPin = 10;
long duration;
int distance;

void setup() {

  Serial.begin(9600);

  pinMode(Led,OUTPUT); 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // pinMode(pinLed, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);

  for (int i = pinInit; i <= pinLast; i++) {
  	
    pinMode(i, OUTPUT);
    
  }

}

void loop() {

  serRead();
  fotocelda();

}

void serRead () {

  while (Serial.available())
  {
    char character = Serial.read();
    if (character != '\n') {


      if (character >= '0' && character <= '9') {
      
        if (character < '1' || character > '5')
          return onLeds(0, false);

        character -= '0';
          
        return onLeds(character, true);

      }

      data.concat(character);

    } else {

      // Serial.println("data");
      // Serial.println(data);

      if (data == "on")
        digitalWrite(relay, LOW); // envia señal baja al relay
  

      if (data == "off")
        digitalWrite(relay, HIGH); // envia señal alta al relay

      if (data == "reset")
        onLeds(0, false), digitalWrite(relay, HIGH);  // apaga todos los leds y envia señal alta al relay

      if (data == "all")
        onLeds(5, true), digitalWrite(relay, LOW);  // enciende todos los leds y envia señal baja al relay

      data = "";

    }
    
  }

  return;

}

void onLeds (int count, bool on) {
  
  if (count < 0)
    return;
    
  if (count < 5)
    for (int i = (count + 5); i <= pinLast; i++) {

      digitalWrite(i, count == 0 ? LOW : on ? LOW : HIGH);
  
    }

  for (int i = pinInit; i <= (count + 4); i++) {
  
    digitalWrite(i, on ? HIGH : LOW);
    
  }

  return;
    
}

void fotocelda () {
 
  // Enviar pulso ultrasónico
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Leer el pulso de respuesta del sensor
  duration = pulseIn(echoPin, HIGH);
  
  // Calcular la distancia en centímetros
  distance = duration * 0.034 / 2;
  
  // Mostrar la distancia en el monitor serie
  //Serial.print("Distancia: ");
  //Serial.print(distance);
  //Serial.println(" cm");
    
  LDR_valor = analogRead(LDR);
  
  //Serial.print("LDR = ");
  //Serial.println(LDR_valor);
  
  if (LDR_valor <= 150  && distance < 20){

    digitalWrite(Led, LOW);
    //delay(10000);
    for(int i = 0; i< 1000; i++){
      serRead();
      delay(10);
    }
    
    return;

  }
  else
    digitalWrite(Led, HIGH);

  return;

}
