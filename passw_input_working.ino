//this is the wooden box keyboard
#include <Keyboard.h>
#include <ctype.h>
#include "config.h"

const int numberOfButtons = 3;

const int pass1Length = sizeof(password1) / sizeof(password1[0]);
const int pass2Length = sizeof(password2) / sizeof(password2[0]);
const int pass3Length = sizeof(password3) / sizeof(password3[0]);

const int passwordLengths[numberOfButtons] = {pass1Length, pass2Length, pass3Length};
const PasswordElement* passMessages[numberOfButtons] = {password1, password2, password3}; 

const int led1 = 16; 
const int led2 = 15;
const int led3 = 19;  
const int button1 = 10;
const int button2 = 14;
const int button3 = 18;


int lastState1;
int lastState2;
int lastState3;

int buttonPins[numberOfButtons] = {button1, button2, button3};
int ledPins[numberOfButtons] = {led1, led2, led3};


int lastStates[numberOfButtons] = {digitalRead(button1), digitalRead(button2), digitalRead(button3)};

int currentIndex[numberOfButtons] = {0, 0, 0};

void setup() {

  setPinModes();

  turnOnAllLeds();

  Keyboard.begin(KeyboardLayout_en_US);
  Serial.begin(9600);

}

void loop() {
  for (int i = 0; i < numberOfButtons; i++) {
    int currentState = digitalRead(buttonPins[i]);
    if (currentState == LOW && lastStates[i] == HIGH) {
      blinkLed(ledPins[i]);
      Serial.print(i);
      Serial.print("pressed something");
      printPassword(passMessages[i], passwordLengths[i]);
    
    }
    lastStates[i] = currentState;
    delay(50);
  }
  
}

void blinkLed(int ledPin) {
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW);
    delay(100);
    digitalWrite(ledPin, HIGH);
    delay(100);
  }
}
void tapKey(int key){
  Keyboard.press(key);
  Keyboard.release(key);
  delay(10);  
  
}
void setPinModes(){
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
}

void turnOnAllLeds(){
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  digitalWrite(led3, HIGH);
}
bool isLetter(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

bool isSpecialCharacter(char c) {
    return !isDigit(c) && !isLetter(c);
}

void typeUnderscore() {
    Keyboard.press(KEY_LEFT_SHIFT); // Press Shift
    tapKey('-');                    // Press and release the hyphen key
    Keyboard.release(KEY_LEFT_SHIFT); // Release Shift
}

void typeBackslash() {
  //for (int i = 0x01; i <= 0xFF; i++) {
    //String keyCodeStr = String(i, HEX);
    //Keyboard.write(0x5A);
    Keyboard.release(KEY_LEFT_SHIFT);
    Keyboard.release(KEY_RIGHT_SHIFT);
    Keyboard.write(0x5C);
    delay(300); // Delay between key presses
  //}  
}
void typePeriod() {
    //String keyCodeStr = String(i, HEX);
    //Keyboard.write(0x5A);
    Keyboard.release(KEY_LEFT_SHIFT);
    Keyboard.release(KEY_RIGHT_SHIFT);
    Keyboard.write(0x2E);
    delay(300); // Delay between key presses
   
}

void printPassword(const PasswordElement* password, size_t length) {
  for (size_t i = 0; i < length; i++) {
    printPasswordElement(password[i]);
  }
}

void printPasswordElement(const PasswordElement& element) {
  if (element.specialKey == PASS_KEY_NONE) {
    // It's a text element, print the text
    printText(element.text);
  } else {
    // It's a special key, handle accordingly
    switch (element.specialKey) {
      case PASS_KEY_ENTER:
        Keyboard.write(KEY_RETURN); // Use KEY_RETURN for the Enter key
        break;
      case PASS_KEY_TAB:
        Keyboard.write(KEY_TAB);
        break;
      // Handle other special keys as needed
    }
  }
}

void printText(const String& text) {
  

    for (int j = 0; j < text.length(); j++){
      char c = text.charAt(j);  
    
      if (isUpperCase(c) || isSpecialCharacter(c) ) {
        Keyboard.press(KEY_LEFT_SHIFT);  // Press Shift for uppercase letters and special characters
      }
  
      // Check for special characters and send their key codes
      if (isSpecialCharacter(c)) {
        switch (c) {
        case '!':
          tapKey('1');
          break;
        case '@':
          tapKey('2'); 
          break;
        case '#':
          tapKey('3'); 
          break;
        case '$':
          tapKey('4'); 
          break;
        case '%':
          tapKey('5'); 
          break;
        case '^':
          tapKey('6'); 
          break;
        case '&':
          tapKey('7'); 
          break;
         case '*':
          tapKey('8'); 
          break;
         case '(':
          tapKey('9'); 
          break;
         case '.':
          typePeriod(); 
          break;
         case ')':
          tapKey('0'); 
          break;
        case '\\':
          typeBackslash();
          break;          
        case '_':
          typeUnderscore(); 
          break;
        }
      } else {  
          tapKey(tolower(c)); // Convert to lowercase because Shift is already being pressed for uppercase
        }
      
  
      if (isUpperCase(c) || isSpecialCharacter(c)) {
        Keyboard.release(KEY_LEFT_SHIFT);  // Release Shift
      }
    }
  }
