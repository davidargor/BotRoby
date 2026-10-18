#include <Arduino.h>
#include "cmdParser.h"

extern "C" {
  #include "stm32l0xx_hal.h"
}

SPI_HandleTypeDef hspi1_slave; // Renamed to avoid conflicts

#define BUFFER_SIZE 3
volatile uint8_t spiRxBuffer[BUFFER_SIZE]; // An array instead of a single byte
volatile bool dataReady = false;

// 1. Connect the hardware to the HAL code
extern "C" void SPI1_IRQHandler(void) {
  HAL_SPI_IRQHandler(&hspi1_slave);
}

void MX_SPI1_Init(void) {
  __HAL_RCC_SPI1_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  // PA5 = SCK, PA6 = MISO, PA7 = MOSI, PA4 = NSS (D10)
  GPIO_InitStruct.Pin       = GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7 | GPIO_PIN_4;
  GPIO_InitStruct.Mode      = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull      = GPIO_NOPULL;
  GPIO_InitStruct.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF0_SPI1;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  hspi1_slave.Instance               = SPI1;
  hspi1_slave.Init.Mode              = SPI_MODE_SLAVE;
  hspi1_slave.Init.Direction         = SPI_DIRECTION_2LINES;
  hspi1_slave.Init.DataSize          = SPI_DATASIZE_8BIT;
  hspi1_slave.Init.CLKPolarity       = SPI_POLARITY_LOW;   // MODE0
  hspi1_slave.Init.CLKPhase          = SPI_PHASE_1EDGE;    // MODE0
  hspi1_slave.Init.NSS               = SPI_NSS_HARD_INPUT; // NSS managed by hardware (PA4)
  hspi1_slave.Init.FirstBit          = SPI_FIRSTBIT_MSB;
  hspi1_slave.Init.TIMode            = SPI_TIMODE_DISABLE;
  hspi1_slave.Init.CRCCalculation    = SPI_CRCCALCULATION_DISABLE;

  if (HAL_SPI_Init(&hspi1_slave) != HAL_OK) {
    while (1); // Critical error
  }

  // 2. ENABLE INTERRUPTS IN NVIC
  HAL_NVIC_SetPriority(SPI1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(SPI1_IRQn);

  // Start the first receive
  HAL_SPI_Receive_IT(&hspi1_slave, (uint8_t *)spiRxBuffer, BUFFER_SIZE);
}

// Callback called by the interrupt when data arrives
extern "C" void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi) {
  if (hspi->Instance == SPI1) {
    dataReady = true;
    // Re-arm for the next bytes
    HAL_SPI_Receive_IT(&hspi1_slave, (uint8_t *)spiRxBuffer, BUFFER_SIZE);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000); // Brief delay for stability
  Serial.println("--- SPI SLAVE TEST ---");
  MX_SPI1_Init();
  
  // initialize the motor control pins as outputs
  pinMode(MOTOR_A_PIN_1, OUTPUT);
  pinMode(MOTOR_A_PIN_2, OUTPUT);
  pinMode(MOTOR_B_PIN_1, OUTPUT);
  pinMode(MOTOR_B_PIN_2, OUTPUT);
  pinMode(MOTOR_C_PIN_1, OUTPUT);
  pinMode(MOTOR_C_PIN_2, OUTPUT);
  pinMode(MOTOR_D_PIN_1, OUTPUT);
  pinMode(MOTOR_D_PIN_2, OUTPUT);
  
  // Initialize PWM pins to 0 (off)
  analogWrite(MOTOR_A_PIN_1, 0);
  analogWrite(MOTOR_A_PIN_2, 0);
  analogWrite(MOTOR_B_PIN_1, 0);
  analogWrite(MOTOR_B_PIN_2, 0);
  analogWrite(MOTOR_C_PIN_1, 0);
  analogWrite(MOTOR_C_PIN_2, 0);
  analogWrite(MOTOR_D_PIN_1, 0);
  analogWrite(MOTOR_D_PIN_2, 0);
}

void loop() {
  if (dataReady) {
    dataReady = false;
    Serial.print("Received packet: ");
    for(int i=0; i < BUFFER_SIZE; i++) {
      Serial.print("0x");
      Serial.print(spiRxBuffer[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    // Call the command parsing function once:
    executeCommand(spiRxBuffer[0], spiRxBuffer[1], 100);//spiRxBuffer[2]);
  }
}