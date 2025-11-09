#include <Arduino.h>

// --- Program variables ---
volatile bool data_toggle = false;
volatile int sensor_choice = 0;

// --- Sensor pins ---
const int Ultrasonic_trig = 14;
const int Ultrasonic_echo = 27;
const int IR_read = 26;

// --- LEDs ---
const int data_led = 2;
const int sensor_selectLED0 = 32; // Ultrasonic
const int sensor_selectLED1 = 33; // IR

// --- Buttons ---
const int data_toggle_bttn = 34;
const int sensor_select_bttn = 35;

// --- Enum for active sensor ---
enum {
  Ultrasonic,
  IR
};

// --- Function declarations ---
void Ultrasonic_sensor_read();
void IR_sensor_read();
void update_sensor_leds();

// --- Interrupt functions ---
void IRAM_ATTR datastreamer_toggle();
void IRAM_ATTR sensor_select();

// --- Setup ---
void setup() {
  Serial.begin(9600);

  pinMode(data_toggle_bttn, INPUT_PULLUP);
  pinMode(sensor_select_bttn, INPUT_PULLUP);

  pinMode(data_led, OUTPUT);
  pinMode(sensor_selectLED0, OUTPUT);
  pinMode(sensor_selectLED1, OUTPUT);

  pinMode(Ultrasonic_trig, OUTPUT);
  pinMode(Ultrasonic_echo, INPUT);
  pinMode(IR_read, INPUT);

  attachInterrupt(digitalPinToInterrupt(sensor_select_bttn), sensor_select, FALLING);
  attachInterrupt(digitalPinToInterrupt(data_toggle_bttn), datastreamer_toggle, FALLING);

  update_sensor_leds();
}

// --- Main loop ---
void loop() {
  if (data_toggle) {
    switch (sensor_choice) {
      case Ultrasonic:
        Ultrasonic_sensor_read();
        break;

      case IR:
        IR_sensor_read();
        break;

      default:
        sensor_choice = Ultrasonic;
        break;
    }
  }

  delay(200); // control data rate
}

// --- Ultrasonic sensor function ---
void Ultrasonic_sensor_read() {
  long duration;
  float distance_cm;

  digitalWrite(Ultrasonic_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(Ultrasonic_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Ultrasonic_trig, LOW);

  duration = pulseIn(Ultrasonic_echo, HIGH);
  distance_cm = (duration * 0.0343) / 2.0; // cm = (time * speed_of_sound) / 2

  //Serial.print("Ultrasonic (cm): ");
  Serial.println(distance_cm, 2);
}

// --- IR sensor function ---
void IR_sensor_read() {
  int rawValue = analogRead(IR_read);
  float voltage = rawValue * (3.3 / 4095.0);

  // Example empirical conversion (calibrate for your sensor!)
  float distance_cm = 0.0;
  if (voltage > 0.42) {
    distance_cm = 27.86 / (voltage - 0.42);
  }

  //Serial.print("IR sensor (V): ");
  Serial.print(voltage, 2);
  //Serial.print("  |  Distance (cm): ");
  Serial.println(distance_cm, 1);
}

// --- Interrupt handlers ---
void IRAM_ATTR datastreamer_toggle() {
  data_toggle = !data_toggle;
  digitalWrite(data_led, data_toggle ? HIGH : LOW);
}

void IRAM_ATTR sensor_select() {
  sensor_choice++;
  if (sensor_choice > IR) sensor_choice = Ultrasonic;
  update_sensor_leds();
}

// --- Helper function ---
void update_sensor_leds() {
  digitalWrite(sensor_selectLED0, sensor_choice == Ultrasonic);
  digitalWrite(sensor_selectLED1, sensor_choice == IR);
}
