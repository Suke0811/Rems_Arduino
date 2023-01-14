// Relay pin is controlled with D8. The active wire is connected to Normally Closed and common



const byte numChars = 32;
char receivedChars[numChars];

int pin = 2;
int data = 0;

char value = 0;


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(50);
}

void loop() {
  if ( recvWithEndMarker()) {
    if (receivedChars[0] == 'w') {
    pin = letter2int(receivedChars[1]);
    value = receivedChars[2];
    writePin(pin, value);
    }
  

  if (receivedChars[0] == 'p') {
    pin = letter2int(receivedChars[1]);
    value = receivedChars[2];
    setPinMode(pin, value);
    
  }
  }
digitalWrite(LED_BUILTIN, LOW);                                                                                                                                                     
}


//set pin 
void setPinMode(int pin, char mode) {
  if (mode == 'i') {
    pinMode(pin, INPUT);
  } else {
    pinMode(pin, OUTPUT);
  }

}

//digital write
void writePin(int pin, char value) {
  if (value == 'h') {
    digitalWrite(pin, HIGH);
  } else if (value == 'l') {
    digitalWrite(pin, LOW);
  }
}




bool recvWithEndMarker() {
  // get line of serial data
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  while (Serial.available() > 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    rc = Serial.read();
    delay(1);

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0';  // terminate the string
      ndx = 0;
      return true;
    }
  }
  return false;
}




// to represent a pin number with a single char
int letter2int(char letter){
  int ret = 0;
  switch(letter){
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
      ret = letter - '0';
      break;
    case 'a':
      ret = 10;
      break;
    case 'b':
    ret = 11;
      break;
    case 'c':
    ret = 12;
      break;
    case 'd':
    ret = 13;
      break;
    case 'l':
    ret = LED_BUILTIN;
      break;

  }
  return ret;
}