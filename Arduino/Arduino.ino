#include "Header.h"

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  TWBR = 12;

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

  Mouse.begin();
  Serial.begin(19200);
  calibrate();

  //Initialize the all LED
  pinMode(IndicateSensitivity, OUTPUT); //9番ピンを初期化
  pinMode(IndicateLinear, OUTPUT);  //10番ピンを初期化
  pinMode(IndicateSqrt, OUTPUT);  //11番ピンを初期化
  pinMode(IndicateQuad, OUTPUT);  //12番ピンを初期化
  digitalWrite(IndicateSensitivity, HIGH);
  digitalWrite(IndicateLinear, HIGH);
  digitalWrite(IndicateSqrt, HIGH);
  digitalWrite(IndicateQuad, HIGH);
  delay(1000);
  digitalWrite(IndicateSensitivity, LOW);
  digitalWrite(IndicateLinear, LOW);
  digitalWrite(IndicateSqrt, LOW);
  digitalWrite(IndicateQuad, LOW);
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
  
  pitch = -atan2(acc_y, acc_x) * 360 / 2.0 / PI; //calculatete the pitch angle
  //Serial.print(pitch); Serial.print(",");
  roll = atan2(acc_z, acc_x) * 360 / 2.0 / PI; //calculate the roll angle
  //Serial.println(roll);

  if (digitalRead(4) == LOW) { //if the left switch is pushed then sensitiity+=1
    sensitivity++;
    if (sensitivity > 5) sensitivity = 0;
    delay(100);
    while (digitalRead(4) == LOW) {}
    indicateCurrentSensitivity();
  }

  if (digitalRead(5) == LOW) { //if the right switch is pushed then function+=1
    function += 1;
    if (function > 3) function = 0;
    delay(100);
    while (digitalRead(5) == LOW) {}
    indicateCurrentFunction();
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
      digitalWrite(IndicateLinear, HIGH);
      delay(1000);
      digitalWrite(IndicateLinear, LOW);
    }
   else if (function == 1) {
      digitalWrite(IndicateSqrt, HIGH);
      delay(1000);
      digitalWrite(IndicateSqrt, LOW);
    }
   else if (function == 2) {
      digitalWrite(IndicateQuad, HIGH);
      delay(1000);
      digitalWrite(IndicateQuad, LOW);
    }
   else {
      digitalWrite(IndicateLinear, HIGH);
      digitalWrite(IndicateSqrt, HIGH);
      digitalWrite(IndicateQuad, HIGH);
      delay(1000);
      digitalWrite(IndicateLinear, LOW);
      digitalWrite(IndicateSqrt, LOW);
      digitalWrite(IndicateQuad, LOW);
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

void distinguisher() {
  float netPitch = roll - rollOffset;
  float netRoll = pitch - pitchOffset;
  //this is reversed because the sensor is on its side
  if (function == 0) { //linear mode
    move_x = (int) kx * (netPitch/pitchMax);
    move_y = (int) ky * (netRoll/rollMax);
  }

  if (function == 1) { //sqrt mode
    move_x = (int) kx * sign(netPitch) * sqrt(abs(netPitch)/pitchMax);
    move_y = (int) ky * sign(netRoll) * sqrt(abs(netRoll)/rollMax);
  }

  if (function == 2) { //non-linear mode
    move_x = (int) kx * sign(netPitch) * (netPitch/pitchMax)*(netPitch/pitchMax);
    move_y = (int) ky * sign(netRoll) * (netRoll/rollMax)*(netRoll/rollMax);
  }

  if (function == 3) { //off mode
    move_x = 0;
    move_y = 0;
  }
  Serial.print(netPitch); Serial.print(';'); Serial.print(-netRoll); Serial.print(';'); Serial.println(kx);
 }

void calibrate() {
  float pitchCalib, rollCalib;
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

    pitchCalib += -atan2(acc_y, acc_x) * 360 / 2.0 / PI; //calculatete the tilt angle about netPitch-axis
    //Serial.print(pitch); Serial.print(",");
    rollCalib += atan2(acc_z, acc_x) * 360 / 2.0 / PI; //calculate the tilt angle about netRoll-axis
  }
  pitchOffset = pitchCalib/100;
  rollOffset = rollCalib/100; //an average value for 100 iteration
  
}

void sensitivity_changer() {
  kx = (sensitivity + 1) * 10;
  ky = (sensitivity + 1) * 10;
  delay(5);
}
