#################################### Practical 5B ######################################
#include <LiquidCrystal.h>
LiquidCrystal lcd(1, 2, 4, 5, 6, 7);
int celsius = 0;
void setup() {
    lcd.begin(16,2);
}
void loop() {
    celsius = map(((analogRead(A0) - 20) * 3.04), 0, 1023, -40, 125);
    lcd.print("");
    lcd.setCursor(0,1);
    lcd.print(celsius);
    delay(4000);
    lcd.clear();
}