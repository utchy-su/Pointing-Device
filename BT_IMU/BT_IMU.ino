#include <SoftwareSerial.h>
#include <Wire.h>

#define RAD_TO_DEG 180/PI
#define DEG_TO_RAD PI/180

#define tx 7
#define rx 6

#define LED 13

int xRaw, yRaw, zRaw;
int xAcc, yAcc, zAcc;
int roll, pitch;

SoftwareSerial btSerial(rx, tx);

void setup() {
  // put your setup code here, to run once:
  /*
  Wire.begin();

  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission();
  
  Wire.beginTransmission(0x68);
  Wire.write(0x1C);
  Wire.write(0x10);
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x1B);
  Wire.write(0x08);
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x1A);
  Wire.write(0x05);
  Wire.endTransmission();
  */
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
  
  btSerial.begin(9600);
  //Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 14);

  digitalWrite(LED, HIGH);
  while (Wire.available() < 14);
  digitalWrite(LED, LOW);

  xRaw = Wire.read() << 8 | Wire.read();
  yRaw = Wire.read() << 8 | Wire.read();
  zRaw = Wire.read() << 8 | Wire.read();

  roll = atan2(yRaw, xRaw) * RAD_TO_DEG;
  pitch = atan2(zRaw, xRaw) * RAD_TO_DEG;

  int xMove = convertToRange(roll);
  int yMove = convertToRange(pitch);
  */
  btSerial.write((byte)0xFD);
  btSerial.write((byte)0x05);
  btSerial.write((byte)0x02);
  //Serial.print(xMove); Serial.print("\t"); Serial.println(yMove);
  btSerial.write((byte)0x00);
  btSerial.write((byte)0x0A);
  btSerial.write((byte)0x0A);
  btSerial.write((byte)0x00);

  //digitalWrite(LED, HIGH);
  delay(50);
  //digitalWrite(LED, LOW);
}

int convertToRange(int angle) {
  int res;
  if (0 <= angle && angle <= 40) {
    res = (angle/40) * 127;
  }
  else if (-40 <= angle && angle < 0) {
    res = 255 - (angle/40) * 127;
  }
  else {
    res = 0;
  }
  return res;
}
