#include <Mouse.h>
#include <Wire.h>

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

void setup() {
  // put your setup code here, to run once:

  Serial.begin(19200);

}

void loop() {
  // put your main code here, to run repeatedly:

  if (digitalRead(4)==LOW){
    delay(100);
    while(digitalRead(4)==LOW){}
    Serial.print("detected");
    }

}
