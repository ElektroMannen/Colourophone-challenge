#include <Arduino.h>


//Program variables
bool data_toggle = false;
int sensor_choice = 0;

//Sensor pins
int Ultrasonic_trig = 14;
int Ultrasonic_read = 27;
int IR_read = 26;
int TOF_SCL = 22;
int TOF_sda = 21;

//Active sensor light
int sensor_selectLED0 = 32; // Ultrasonic
int sensor_selectLED1 = 33; // IR
int sensor_selectLED2 = 25; // TOF

//Buttons
int data_toggle_bttn = 34;
int sensor_select_bttn = 35;

//Function definition
void US_sensor_read(int pin);
void IR_sensor_read(int pin);
void TOF_sensor_read(int pin);


enum{
  Ultrasonic,
  IR,
  TOF
};


//Function definition
void US_sensor_read(int pin);
void IR_sensor_read(int pin);
void TOF_sensor_read(int pin);


void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(data_led,INPUT);
  pinMode(data_sending_bttn,INPUT_PULLUP);
  pinMode(sensor_select_bttn,INPUT_PULLUP);

  attachInterrupt(sensor_select_bttn, sensor_select, FALLING);
  attachInterrupt(data_toggle_bttn, datastreamer_toggle, FALLING);  
}

void loop() {
  // put your main code here, to run repeatedly:
    switch (sensor_choice){
    case Ultrasonic:
      sensor_data = 5;
      break;

    case IR:
     sensor_data = 5;
      break;
    
    case TOF:
     sensor_data = 5;
      break;

    default: //Sets sensor back to first choice so it doesnt go out of scope.
      sensor_choice = 0;
      break;
  }
}

//Interupt functions
void IRAM_ATTR datastreamer_toggle(){
  data_toggle = !data_toggle;
  if (data_toggle == true){
    data_led = HIGH;
  }
  else
    data_led = LOW;
}

void IRAM_ATTR sensor_select(){
  sensor_choice += 1;
}