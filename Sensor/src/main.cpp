#include <Arduino.h>

//Pin asignments
int sensor_select_bttn = 2;
int data_sending_bttn = 4;
int data_led = 0;

bool data_toggle = false;
int sensor_choice = 0;
//Function definition
void US_sensor_read(int pin);
void IR_sensor_read(int pin);
void TOF_sensor_read(int pin);


void setup() {
  // put your setup code here, to run once:

  attachInterrupt(sensor_select_bttn, ISR, FALLING);
  attachInterrupt(data_sending_bttn, datastreamer_toggle, FALLING);  
}

void loop() {
  // put your main code here, to run repeatedly:
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
  
}