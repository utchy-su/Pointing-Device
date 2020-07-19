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
  pinMode(IndicateSensitivity, OUTPUT); //9番ピンを初期化
  pinMode(IndicateOff, OUTPUT);  //10番ピンを初期化
  pinMode(IndicateLinear, OUTPUT);  //11番ピンを初期化
  pinMode(IndicateNonLinear, OUTPUT);  //12番ピンを初期化
  digitalWrite(IndicateSensitivity, HIGH);
  digitalWrite(IndicateOff, HIGH);
  digitalWrite(IndicateLinear, HIGH);
  digitalWrite(IndicateNonLinear, HIGH);
  delay(1000);
  digitalWrite(IndicateSensitivity, LOW);
  digitalWrite(IndicateOff, LOW);
  digitalWrite(IndicateLinear, LOW);
  digitalWrite(IndicateNonLinear, LOW);
  //起動時にすべてのLEDが一瞬点灯する
}

void loop() {
  // put your main code here, to run repeatedly:

  t = millis();  //get the current time at the beggining of the loop

  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 14);
  while (Wire.available() < 14);
  axRaw = Wire.read() << 8 | Wire.read();  //get the acceleration on x-axis
  ayRaw = Wire.read() << 8 | Wire.read();  //get the acceleration on y-axis
  azRaw = Wire.read() << 8 | Wire.read();  //get the acceleration on z-axis

  acc_x = axRaw / 16384.0; //convert raw data into m/s^2
  acc_y = ayRaw / 16384.0;
  acc_z = azRaw / 16384.0;

  acc_angX = atan2(acc_y, acc_x) * 360 / 2.0 / PI; //calculatete the tilt angle about X-axis
  //Serial.print(acc_angX); Serial.print(",");
  acc_angY = atan2(acc_z, acc_x) * 360 / 2.0 / PI; //calculate the tilt angle about Y-axis
  //Serial.println(acc_angY);

  Serial.print(acc_angX); Serial.print(" ; "); Serial.println("acc_angY");

  if (digitalRead(4) == LOW) { //if the left switch is pushed then sensitiity+=1
    sensitivity++;
    if (sensitivity > 5) sensitivity = 0;
    delay(100);
    while (digitalRead(4) == LOW) {}
    indicateCurrentSensitivity();
  }

  if (digitalRead(5) == LOW) { //if the right switch is pushed then function+=1
    function += 1;
    if (function > 2) function = 0;
    delay(100);
    while (digitalRead(5) == LOW) {}
    indicateCurrentFunction();
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
void indicateCurrentFunction() {
  if (function == 0) {
      digitalWrite(IndicateOff, HIGH);
      delay(1000);
      digitalWrite(IndicateOff, LOW);
    }
   else if (function == 1) {
      digitalWrite(IndicateLinear, HIGH);
      delay(1000);
      digitalWrite(IndicateLinear, LOW);
    }
   else {
      digitalWrite(IndicateNonLinear, HIGH);
      delay(1000);
      digitalWrite(IndicateNonLinear, LOW);
    }
  }

void indicateCurrentSensitivity() {
    for (int i = 0; i < sensitivity; i++) {
        digitalWrite(IndicateSensitivity, HIGH);
        delay(100);
        digitalWrite(IndicateSensitivity, LOW);
        delay(100);
      }
  }

/*
void twinkle(int func_name) {
  if (func_name == 1) {
    int n = IndicateMode; //light LED1 on
    int rep_num =  sensitivity;
    Serial.println(n);
    for (int i = 0; i <= s; i++) {
      digitalWrite(n, HIGH);
      delay(100);
      digitalWrite(n, LOW);
      delay(100);
    }
  }

  if (func_name == 2) {
    int rep_num = s;
    if (s == 0) {
      digitalWrite(IndicateLow, HIGH);
      delay(1000);
      digitalWrite(IndicateLow, LOW);
    }
    if (s == 1) {
      digitalWrite(IndicateMid, HIGH);
      delay(1000);
      digitalWrite(IndicateMid, LOW);
    }
    if (s == 2) {
      digitalWrite(IndicateHigh, HIGH);
      delay(1000);
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
*/

void distinguisher() {
  float X = acc_angY - Yoffset;
  float Y = acc_angX - Xoffset;
  //this is reversed because the sensor is on its side
  if (function == 0) { //OFF MODE
    move_x = 0;
    move_y = 0;
  }

  if (function == 1) { //Linear Mode
    move_x = (int) (kx *  X / Xmax);
    move_y = (int) (ky * -Y / Ymax);
  }

  if (function == 2) { //non-linear mode
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
  kx = (sensitivity + 1) * 10;
  ky = (sensitivity + 1) * 10;
  delay(5);
}
