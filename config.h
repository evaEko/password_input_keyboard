// config.h
#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h> 

enum SpecialKey {
  PASS_KEY_NONE,
  PASS_KEY_ENTER,
  PASS_KEY_TAB
};

struct PasswordElement {
  String text;
  SpecialKey specialKey;

  PasswordElement(String t) : text(t), specialKey(PASS_KEY_NONE) {}
  PasswordElement(SpecialKey sk) : text(""), specialKey(sk) {}
};

#include "passwords_def.h"

#endif // CONFIG_H

