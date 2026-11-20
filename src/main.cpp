// W204 OBD reader — entry point (scaffold; see docs/PLAN.md)
#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial.println("W204 OBD reader: scaffold");
}

void loop() {
  delay(1000);
}
