#include <SoftwareSerial.h>

#define tx 1
#define rx 0
#define led 13

int i = 0;

SoftwareSerial btSerial(rx, tx);

void setup() {
  // put your setup code here, to run once:

  btSerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  btSerial.write((byte)0xFD);
  btSerial.write((byte)0x05);
  btSerial.write((byte)0x02);

  btSerial.write((byte)0x00);
  btSerial.write((byte)i);
  btSerial.write((byte)0x00);
  btSerial.write((byte)0x00);
  i++;
  delay(100);
}


boolean readMageSensor(int port, float limit){
  int mageValue = analogRead(port);
  float voltage = mageValue * (5.0 / 1023.0);
  //Serial.print(voltage);
  return voltage > limit;
}

void sendKeyModifier(byte key, byte modifier){
  sendKeyCode(key, modifier);
  delay(100);
  sendKeyCode((byte)0x00, (byte)0x00);
}

void sendKey(byte key){
  sendKeyModifier(key, (byte)0x00);
}
void sendKeyCode(byte key, byte modifier){
    btSerial.write(0xFD); // Raw Report Mode
    btSerial.write(0x09); // Length
    btSerial.write(0x01); // Descriptor 0x01=Keyboard

    btSerial.write(modifier);
    btSerial.write((byte)0x00);
    btSerial.write(key);
    btSerial.write((byte)0x00);
    btSerial.write((byte)0x00);
    btSerial.write((byte)0x00);
    btSerial.write((byte)0x00);
    btSerial.write((byte)0x00);
}

void ledFlash(){
  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(10);              // wait for a second
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  delay(10);              // wait for a second
}
