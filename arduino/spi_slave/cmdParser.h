// Command definitions
// Global variables use 1520 bytes (18%) of dynamic memory, leaving 6672 bytes free for local variables. The maximum is 8192 bytes.

// Mobility commands:
#define CMD_MOTORS_OFF      0x00 // turns the motors off (0 0)
#define CMD_MOTORS_BRAKE    0x01 // brakes the motors (1 1)
#define CMD_MOTORS_FRONT    0x02 // moves forward (1 byte for speed)
#define CMD_MOTORS_BACK     0x03 // moves backward (1 byte for speed)
#define CMD_MOTORS_LEFT     0x04 // moves left (1 byte for speed)
#define CMD_MOTORS_RIGHT    0x05 // moves right (1 byte for speed)
#define CMD_MOTORS_RLEFT    0x06 // rotates counterclockwise (1 byte for speed)
#define CMD_MOTORS_RRIGHT   0x07 // rotates clockwise (1 byte for speed)


// Motor pin definitions (PWM-capable)
#define MOTOR_A_PIN_1     PA0   // TIM2_CH1
#define MOTOR_A_PIN_2     PB10  // TIM2_CH3 // -- PA1   // TIM2_CH2
#define MOTOR_B_PIN_1     PA1   // TIM2_CH2//  -- PB10  // TIM2_CH3
#define MOTOR_B_PIN_2     PB11  // TIM2_CH4
#define MOTOR_C_PIN_1     PB13  // TIM21_CH1
#define MOTOR_C_PIN_2     PB14  // TIM21_CH2
#define MOTOR_D_PIN_1     PB4   // TIM22_CH1
#define MOTOR_D_PIN_2     PB5   // TIM22_CH2

// Function declarations
void executeCommand(uint8_t grpID, uint8_t cmdID, uint8_t param);
void handleMotorsOff(void);
void handleMotorsBrake(void);
void handleMotorsFront(uint8_t speed);
void handleMotorsBack(uint8_t speed);
void handleMotorsLeft(uint8_t speed);
void handleMotorsRight(uint8_t speed);
void handleMotorsRLeft(uint8_t speed);
void handleMotorsRRight(uint8_t speed);
void setMotorPWM(uint16_t pinA, uint16_t pinB, uint8_t speed, bool forward);
void setMotorBrake(uint16_t pinA, uint16_t pinB);
void setMotorOff(uint16_t pinA, uint16_t pinB);

