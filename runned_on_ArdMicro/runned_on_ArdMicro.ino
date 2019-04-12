#include <Mouse.h>
#include <Wire.h>
#include <LiquidCrystal.h>

#define tx 1
#define rx 0

int16_t axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw, temperature; //raw data given by the sensor
unsigned long t; //the time since the beginning of the loop() function
float kx = 0.2; //gain for x
float ky = 0.2; //gain for y
char mode = 0; //mode of control type
int move_x; //relative distance to move in X-axis
int move_y; //relative distance to move in Y-axis
float C = 80; // constant to normalize
float acc_x, acc_y, acc_z; //raw data from the sensor
float acc_angX, acc_angY, acc_angZ; //calculated angles 
unsigned long dt;
int s; // number of times the user pushed the switch 1
int f; // number of times the user pushed the switch 2
#define RAD_TO_DEG 180/PI

LiquidCrystal lcd = LiquidCrystal(6, 7, 8, 9, 10, 11, 12);

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

  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WELCOME");
  delay(3000);
  lcd.clear();
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

  acc_angX = atan2(acc_x, acc_z) * 360 / 2.0 / PI;
  acc_angY = atan2(acc_y, acc_z) * 360 / 2.0 / PI;

  if (digitalRead(4)==LOW){
    s+=1;
    if (s>2) s = 0;
    delay(100);
    while(digitalRead(4)==LOW){}
    }

  if (digitalRead(5)==LOW){
    f += 1;
    if (f>2) f=0;
    delay(100);
    while(digitalRead(5)==LOW){}
    }
  distinguisher();
  sensitivity_changer();
  lcd.clear();
  Mouse.move(move_x, move_y, 0);


  dt = (double) (millis() - t)/1000.0;
}

void distinguisher(){
  if (s==0){ //OFF MODE
    move_x = 0;
    move_y = 0;
    Serial.println("OFF");
    lcd.setCursor(0,0);
    lcd.print("MODE: OFF");
    delay(5);
    }
  if (s==1){ //Linear Mode
    move_x = (int) (kx * acc_angY);
    move_y = (int) (ky * acc_angX);
    Serial.println("linear mode");
    lcd.setCursor(0,0);
    lcd.print("MODE: LINEAR");
    delay(5);
    }
  if (s==2){ //non-linear mode
    move_x = (int) (15 * tanh(acc_angY / 40));
    move_y = (int) (15 * tanh(acc_angX / 40));
    Serial.print("tanh mode");
    lcd.setCursor(0, 0);
    lcd.print("MODE: TANH");
    }
    
}

void sensitivity_changer(){
  if (f==0){
    kx = 0.1; ky = 0.1;
    lcd.setCursor(0, 1);
    lcd.print("GAIN: LOW");
    delay(5);
  }
  if (f==1){
    kx = 0.2; ky=0.2;
    lcd.setCursor(0,1);
    lcd.print("GAIN: MID");
    delay(5);
  }
  if (f==2){
    kx = 0.3; ky = 0.3;
    lcd.setCursor(0,1);
    lcd.print("GAIN: HIGH");
    delay(5);
  }
}
