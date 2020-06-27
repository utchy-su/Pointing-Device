#include <Mouse.h>
#include <Wire.h>

#define RAD_TO_DEG 180/PI
#define DEG_TO_RAD PI/180

#define IndicateSensitivity 9

#define IndicateOff 10
#define IndicateLinear 11
#define IndicateNonLinear 12

int16_t axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw, temperature; //raw data given by the sensor
unsigned long t; //the time since the beginning of the loop() function
float kx = 0.2; //gain for x
float ky = 0.2; //gain for y
char mode = 0; //mode of control type
int move_x; //relative distance to move in X-axis
int move_y; //relative distance to move in Y-axis
float acc_x, acc_y, acc_z; //raw data from the sensor
float acc_angX, acc_angY, acc_angZ; //calculated angles
unsigned long dt; //duration for a single loop
int sensitivity; // number of times the user pushed the switch 1
int function; // number of times the user pushed the switch 2
float Xoffset, Yoffset;
float Xmax = (29 + 29)/2;
float Ymax = (30 + 17)/2;
const float Cx = abs(1 - sin(Xmax*DEG_TO_RAD)/(Xmax*DEG_TO_RAD));
const float Cy = abs(1 - sin(Ymax*DEG_TO_RAD)/(Ymax*DEG_TO_RAD));
