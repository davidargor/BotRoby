#include <Arduino.h>
#include <stdint.h>
#include "cmdParser.h"

void executeCommand(uint8_t grpID, uint8_t cmdID, uint8_t param) {
  switch (cmdID) {
    
    // Meccanum wheel motor group
    case CMD_MOTORS_OFF:
      handleMotorsOff();
      break;
      
    case CMD_MOTORS_BRAKE:
      handleMotorsBrake();
      break;

    case CMD_MOTORS_FRONT:
      handleMotorsFront(param); // param indicates speed
      break;

    case CMD_MOTORS_BACK:
      handleMotorsBack(param);
      break;

    case CMD_MOTORS_LEFT:
      handleMotorsLeft(param);
      break;

    case CMD_MOTORS_RIGHT:
      handleMotorsRight(param);
      break;

    case CMD_MOTORS_RLEFT:
      handleMotorsRLeft(param);
      break;

    case CMD_MOTORS_RRIGHT:
      handleMotorsRRight(param);
      break;
    
    // ...


    // Default: unknown command
    default:
      Serial.print("Error: command ID not recognized 0x");
      Serial.println(cmdID, HEX);
      break;
  }
}

void setMotorPWM(uint16_t pinA, uint16_t pinB, uint8_t speed, bool forward) {
  if (speed == 0) {
    analogWrite(pinA, 0);
    analogWrite(pinB, 0);
    return;
  }

  if (forward) {
    analogWrite(pinA, speed);
    analogWrite(pinB, 0);
  } else {
    analogWrite(pinA, 0);
    analogWrite(pinB, speed);
  }
}

void setMotorBrake(uint16_t pinA, uint16_t pinB) {
  analogWrite(pinA, 255);
  analogWrite(pinB, 255);
}

void setMotorOff(uint16_t pinA, uint16_t pinB) {
  analogWrite(pinA, 0);
  analogWrite(pinB, 0);
}

void handleMotorsOff() {
  Serial.println("Motors off");
  setMotorOff(MOTOR_A_PIN_1, MOTOR_A_PIN_2);
  setMotorOff(MOTOR_B_PIN_1, MOTOR_B_PIN_2);
  setMotorOff(MOTOR_C_PIN_1, MOTOR_C_PIN_2);
  setMotorOff(MOTOR_D_PIN_1, MOTOR_D_PIN_2);
}

void handleMotorsBrake() {
  Serial.println("Motors braked");
  setMotorBrake(MOTOR_A_PIN_1, MOTOR_A_PIN_2);
  setMotorBrake(MOTOR_B_PIN_1, MOTOR_B_PIN_2);
  setMotorBrake(MOTOR_C_PIN_1, MOTOR_C_PIN_2);
  setMotorBrake(MOTOR_D_PIN_1, MOTOR_D_PIN_2);
}

void handleMotorsFront(uint8_t speed) {
  Serial.print("Motors forward at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, true);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, true);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, true);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, true);
}

void handleMotorsBack(uint8_t speed) {
  Serial.print("Motors reverse at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, false);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, false);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, false);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, false);
}

void handleMotorsLeft(uint8_t speed) {
  Serial.print("Left motors at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, false);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, true);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, true);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, false);
}

void handleMotorsRight(uint8_t speed) {
  Serial.print("Right motors at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, true);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, false);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, false);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, true);
}

void handleMotorsRLeft(uint8_t speed) {
  Serial.print("Counterclockwise rotation at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, false);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, false);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, true);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, true);
}

void handleMotorsRRight(uint8_t speed) {
  Serial.print("Clockwise rotation at speed: ");
  Serial.println(speed);
  setMotorPWM(MOTOR_A_PIN_1, MOTOR_A_PIN_2, speed, true);
  setMotorPWM(MOTOR_B_PIN_1, MOTOR_B_PIN_2, speed, true);
  setMotorPWM(MOTOR_C_PIN_1, MOTOR_C_PIN_2, speed, false);
  setMotorPWM(MOTOR_D_PIN_1, MOTOR_D_PIN_2, speed, false);
}


