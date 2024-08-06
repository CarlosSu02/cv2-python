

int pinLed = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(pinLed, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  py();

}

void py () {


  if (Serial.available() > 0) {

    char option = Serial.read();

    if (option >= '1' && option <= '9') {
   
      option -= '0';
    
      // for (int i = 0; i < option; i++) {
   
        digitalWrite(pinLed, HIGH);
        delay(100);
   
        // digitalWrite(pinLed, LOW);
        // delay(100);
   
      // }
   
    }

  }

  digitalWrite(pinLed, LOW);
  // delay(100);

}


