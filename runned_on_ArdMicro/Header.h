#include <Mouse.h>
#include <Wire.h>

#define RAD_TO_DEG 180/PI
#define DEG_TO_RAD PI/180

#define IndicateSensitivity 9

#define IndicateLinear 10
#define IndicateSqrt 11
#define IndicateQuad 12

int16_t axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw, temperature; //raw data given by the sensor
unsigned long t; //the time since the beginning of the loop() function
float kx = 0.2; //gain for x
float ky = 0.2; //gain for y
char mode = 0; //mode of control type
int move_x; //relative distance to move in X-axis
int move_y; //relative distance to move in Y-axis
float acc_x, acc_y, acc_z; //raw data from the sensor
float pitch, roll;
unsigned long dt; //duration for a single loop
int sensitivity; // number of times the user pushed the switch 1
int function; // number of times the user pushed the switch 2
float pitchOffset, rollOffset;
float pitchMax = 40;
float rollMax = 40;

int sign(float num) {
  if (num < 0) return -1;
  return 1;
}

int sign(int num) {
  if (num < 0) return -1;
  return 1;
}
