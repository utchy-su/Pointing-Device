#include <Mouse.h>
#include <Wire.h>
#include "Header.h"

void setup() {
  // put your setup code here, to run once:
  Wire.begin();

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
}

void loop() {
  // put your main code here, to run repeatedly:
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 14);
  while (Wire.available() < 14);
  axRaw = Wire.read() << 8 | Wire.read();
  ayRaw = Wire.read() << 8 | Wire.read();
  azRaw = Wire.read() << 8 | Wire.read();

  acc_x = axRaw / 16384.0;
  acc_y = ayRaw / 16384.0;
  acc_z = azRaw / 16384.0;

  acc_angX = atan2(acc_z, -acc_x) * 360 / 2.0 / PI;
  acc_angY = atan2(acc_y, -acc_x) * 360 / 2.0 / PI;
  //ここはセンサを縦置きにしているので引数の順序が変わってます．
  //以下センサを水平において使う場合
  //acc_angX = atan2(acc_x, acc_z) * 360 / 2.0 / PI;
  //acc_angY = atan2(acc_y, acc_z) * 360 / 2.0 / PI;

  move_x = (int) (kx * acc_angX);
  move_y = (int) (ky * acc_angY);

  Serial.print(acc_angX); Serial.print(',');
  Serial.print(acc_angY); Serial.print(',');
  Serial.println(kx);

  Mouse.move(move_x, move_y, 0);
}
