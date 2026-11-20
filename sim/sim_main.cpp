// W204 ECU simulator — bench test partner for the reader (scaffold; see docs/PLAN.md)
#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial.println("W204 ECU simulator: scaffold");
}

void loop() {
  delay(1000);
}
