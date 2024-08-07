

int pinLed = 13;
// int pinInit = 5, pinLast = 9; // todos continuos

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(pinLed, OUTPUT);

  // for (int i = pinInit; i <= pinLast; i++) {
  	
  //   pinMode(i, OUTPUT);
    
  // }

}

void loop() {
  // put your main code here, to run repeatedly:

  py();

  // serRead();

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

void serRead () {
  
  if (Serial.available() <= 0)
    return;

  char count = Serial.read();

  if (count < '1' || count > '5')
    return onLeds(0, false);

  count -= '0';
  
  return onLeds(count, true);
  
  // Serial.println(int(count));
  
  /*
  for (int i = 0; i < count; i++) {
  
    Serial.println(i);
    
  }
  */
  
}

void onLeds (int count, bool on) {

  // Serial.println('5' - count);
  // Serial.println(count + '1');
    
  Serial.print("count: ");
  Serial.println(int(count));
  Serial.print("on: ");
  Serial.println(String(on));
  
  if (count < 0)
    return;
  
  // Serial.println(count);

  //count -= '0';
  
  //Serial.println(count);
  
  if (count < 5)
    for (int i = (count + 4); i <= pinLast; i++) {

      digitalWrite(i, count == 0 ? LOW : on ? LOW : HIGH);
      // delay(100);

    }

  for (int i = pinInit; i <= (count + 4); i++) {
  
    // Serial.println(i);
    digitalWrite(i, on ? HIGH : LOW);
    delay(50);
    
  }
  
  // onLeds(serRead(), false);
  
}
