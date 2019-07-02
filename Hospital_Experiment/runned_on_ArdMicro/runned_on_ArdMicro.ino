#include "Header.h"

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  TWBR = 12;

  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0X00);
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

  Mouse.begin();
  Serial.begin(19200);
  calibrate();

  //Initialize the all LED
  pinMode(IndicateMode, OUTPUT);
  pinMode(IndicateLow, OUTPUT);
  pinMode(IndicateMid, OUTPUT);
  pinMode(IndicateHigh, OUTPUT);
  digitalWrite(IndicateMode, HIGH);
  digitalWrite(IndicateLow, HIGH);
  digitalWrite(IndicateMid, HIGH);
  digitalWrite(IndicateHigh, HIGH);
  delay(1000);
  digitalWrite(IndicateMode, LOW);
  digitalWrite(IndicateLow, LOW);
  digitalWrite(IndicateMid, LOW);
  digitalWrite(IndicateHigh, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  t = millis();
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 14);
  while (Wire.available() < 14);
  axRaw = Wire.read() << 8 | Wire.read();
  ayRaw = Wire.read() << 8 | Wire.read();
  azRaw = Wire.read() << 8 | Wire.read();

  acc_x = axRaw / 16384.0; //convert raw data into m/s^2
  acc_y = ayRaw / 16384.0;
  acc_z = azRaw / 16384.0;

  acc_angX = atan2(acc_y, acc_x) * 360 / 2.0 / PI; //calculatete the tilt angle about X-axis
  //Serial.print(acc_angX); Serial.print(",");
  acc_angY = atan2(acc_z, acc_x) * 360 / 2.0 / PI; //calculate the tilt angle about Y-axis
  //Serial.println(acc_angY);

  if (digitalRead(4) == LOW) { //if the left switch is pushed then s+=1
    s += 1;
    if (s > 3) s = 0;
    delay(100);
    while (digitalRead(4) == LOW) {}
    twinkle(1);
  }

  if (digitalRead(5) == LOW) { //if the right switch is pushed then f+=1
    f += 1;
    if (f > 3) f = 0;
    delay(100);
    while (digitalRead(5) == LOW) {}
    twinkle(2);
    calibrate();
  }
  distinguisher();
  sensitivity_changer();
  Mouse.move(move_x, move_y, 0); // Move the cursor according to the tilt angles
  dt = (double) (millis() - t);

  if (dt < 20) delay(20 - dt);
}

//1: distinguisher
//2: sensitivity_changer
void twinkle(int func_name) {
  if (func_name == 1) {
    int n = IndicateMode; //light LED1 on
    int rep_num =  s;
    Serial.println(n);
    for (int i = 0; i <= s; i++) {
      digitalWrite(n, HIGH);
      delay(100);
      digitalWrite(n, LOW);
      delay(100);
    }
  }

  if (func_name == 2) {
    int rep_num = f;
    if (f == 0) {
      digitalWrite(IndicateLow, HIGH);
      delay(1000);
      digitalWrite(IndicateLow, LOW);
    }
    if (f == 1) {
      digitalWrite(IndicateMid, HIGH);
      delay(1000);
      digitalWrite(IndicateMid, LOW);
    }
    if (f == 2) {
      digitalWrite(IndicateHigh, HIGH);
      delay(1000);
      digitalWrite(IndicateHigh, LOW);
    }
    if (f == 3) {
      digitalWrite(IndicateLow, HIGH);
      digitalWrite(IndicateMid, HIGH);
      digitalWrite(IndicateHigh, HIGH);
      delay(1000);
      digitalWrite(IndicateLow, LOW);
      digitalWrite(IndicateMid, LOW);
      digitalWrite(IndicateHigh, LOW);
    }
  }

  if (func_name == 3){
    digitalWrite(IndicateLow, HIGH);
    delay(1000);
    digitalWrite(IndicateLow, LOW);

    if (f == 0){
      digitalWrite(IndicateMid, HIGH);
      delay(1000);
      digitalWrite(IndicateMid, LOW);
    }
  }
}

void distinguisher() {
  float X = acc_angY - Yoffset;
  float Y = acc_angX - Xoffset;
  //this is reversed because the sensor is on its side
  if (f == 0) { //Linear Mode
    move_x = (int) (kx *  X / Xmax);
    move_y = (int) (ky * -Y / Ymax);
  }

  if (f == 1) { //model derived Mode
    if (0 <= X && X < Xmax) {
      move_x = (int) (kx * (1 - sin(X * DEG_TO_RAD) / (X * DEG_TO_RAD)) / Cx);
    } else if (-Xmax < X && X < 0) {
      move_x = (int) (-kx * (1 - sin(X * DEG_TO_RAD) / (X * DEG_TO_RAD)) / Cx);
    } else if (X < -Xmax){
      move_x = -kx;
    } else if (X > Xmax){
      move_x = kx;
    }

    if (0 <= Y && Y < Ymax) {
      move_y = (int) (-ky * (1 - sin(Y * DEG_TO_RAD) / (Y * DEG_TO_RAD)) / Cy);
    } else if (-Ymax< Y && Y< 0) {
      move_y = (int) (ky * (1 - sin(Y * DEG_TO_RAD) / (Y * DEG_TO_RAD)) / Cy);
    } else if (Y < -Ymax){
      move_y = ky;
    } else if (Ymax < Y){
      move_y = -ky;
    }
  }

  if (f == 2) { //tanh mode
    if (0 <= X && X < Xmax) {
      move_x = (int) (kx * tanh(X/Xmax*2));
    } else if (-Xmax < X && X < 0) {
      move_x = (int) (kx * tanh(X/Xmax*2));
    } else if (X < -Xmax){
      move_x = (int) (kx * tanh(-2));
    } else if (X > Xmax){
      move_x = (int) (kx * tanh(2));
    }

    if (0 <= Y && Y < Ymax) {
      move_y = (int) (ky * tanh(-Y/Ymax*2));
    } else if (-Ymax< Y && Y< 0) {
      move_y = (int) (ky * tanh(-Y/Ymax*2));
    } else if (Y < -Ymax){
      move_y = (int) (ky * tanh(2));
    } else if (Ymax < Y){
      move_y = (int) (ky * tanh(-2));
    }
  }

  if (f == 3){ // deactivated mode
    move_x = 0;
    move_y = 0;
  }
  Serial.print(X); Serial.print(';'); Serial.print(-Y); Serial.print(';'); Serial.println(kx);
 }

void calibrate() {
  float Xcalib, Ycalib;
  for (int i = 0; i < 100; i++) {
    Wire.beginTransmission(0x68);
    Wire.write(0x3B);
    Wire.endTransmission();
    Wire.requestFrom(0x68, 14);
    while (Wire.available() < 14);
    axRaw = Wire.read() << 8 | Wire.read();
    ayRaw = Wire.read() << 8 | Wire.read();
    azRaw = Wire.read() << 8 | Wire.read();

    acc_x = axRaw / 16384.0; //convert raw data into m/s^2
    acc_y = ayRaw / 16384.0;
    acc_z = azRaw / 16384.0;

    Xcalib += atan2(acc_y, acc_x) * 360 / 2.0 / PI; //calculatete the tilt angle about X-axis
    //Serial.print(acc_angX); Serial.print(",");
    Ycalib += atan2(acc_z, acc_x) * 360 / 2.0 / PI; //calculate the tilt angle about Y-axis
  }
  Xoffset = Xcalib/100;
  Yoffset = Ycalib/100; //an average value for 100 iteration
  
}

void sensitivity_changer() {
  kx = (s + 1) * 10;
  ky = (s + 1) * 10;
  delay(5);
}
