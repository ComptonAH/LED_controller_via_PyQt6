#define blue_LED 2
#define green_LED_1 4
#define green_LED_2 6

String data;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  digitalWrite(13, 0);
  pinMode(blue_LED, OUTPUT);
  pinMode(green_LED_1, OUTPUT);
  pinMode(green_LED_2, OUTPUT);
}

void  loop() {
  while (Serial.available() == 0) {}
  
  if (Serial.available() > 0)
    data = Serial.readStringUntil(';');
    int pin = parse_pin(data).toInt();
    int on_off = parse_voltage(data).toInt();
    digitalWrite(pin, on_off);

}


String parse_pin(String data){
  String pin = "";
  for (int i = 0; i < data.indexOf(','); i++) {
    pin += data[i];
  }
  return pin;
}

String parse_voltage(String data){
  String voltage;
  voltage = data[data.indexOf(',') + 1];
  return voltage;
}