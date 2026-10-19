# SPI slave firmware

[Italiano](README_it.md)

This folder contains the firmware that receives SPI commands and translates them
into PWM outputs for the four motors. The guide describes the behavior of the
current code and the points to modify in order to add commands or new features.

The development environment used to write the code for the microcontroller is
[Arduino IDE](https://www.arduino.cc/en/software/) with the
[STM32duino](https://github.com/stm32duino) library.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| `spi_slave.ino` | Initializes SPI, receives packets, and starts processing in the main Arduino loop. |
| `cmdParser.h` | Defines command IDs, motor pins, and function declarations. |
| `cmdParser.cpp` | Maps IDs to handler functions and generates PWM signals for the motors. |

## Packet flow

The expected command format is a three-byte frame:

| Index | Field | Expected meaning |
| --- | --- | --- |
| 0 | `grpID` | Destination group or subsystem; `0x01` is indicated as the mobility group. |
| 1 | `cmdID` | Action identifier. |
| 2 | `param` | Action parameter; for movement commands it is the speed. |

The firmware flow is:

1. `MX_SPI1_Init()` configures SPI1 as a slave and starts an interrupt-driven
   receive of `BUFFER_SIZE` bytes (currently 3).
2. After the reception completes, `HAL_SPI_RxCpltCallback()` sets `dataReady` and
   restarts reception.
3. `loop()` detects `dataReady`, prints the received bytes, and calls
   `executeCommand()`.
4. `executeCommand()` selects a handler based on the command.
5. The handlers set the motor outputs through `setMotorPWM()`,
   `setMotorOff()`, or `setMotorBrake()`.

The interrupt only signals reception; command processing happens in the main loop,
not in the callback.

## SPI configuration and connections

The configuration in `MX_SPI1_Init()` is:

- SPI1 in slave mode, full duplex, two-wire;
- 8-bit words, most significant bit first (MSB first);
- polarity and phase `LOW` / `1EDGE` (SPI mode 0);
- hardware NSS, connected to PA4;
- hardware CRC disabled;
- SPI pins: PA5 = SCK, PA6 = MISO, PA7 = MOSI, PA4 = NSS.

The master must therefore use compatible settings and keep NSS active during frame
transmission. The SPI frequency is not specified in this file.

## Current behavior and known limitations

The three-byte format is the expected one, but the current code does not fully
implement this semantics:

- `loop()` calls `executeCommand(spiRxBuffer[0], spiRxBuffer[1], 100)`. The
  third received byte (`spiRxBuffer[2]`) is commented out and therefore ignored;
  movement commands always receive speed `100`.
- `executeCommand()` does not use `grpID`; the `switch` selects the command based
  only on `cmdID`. Group `0x01` is documented as mobility, but it is neither
  validated nor routed by the parser.
- Reception is fixed at three bytes. There is no length field, delimiter,
  sequence number, or application-level checksum/CRC.
- `HAL_SPI_RxCpltCallback()` restarts reception using the same buffer shared with
  `loop()`. A subsequent packet received before the main loop has processed the
  previous one may overwrite the data. If traffic is expected to be frequent,
  a design with separate buffers or a queue should be used.
- If `HAL_SPI_Init()` fails, the firmware remains in the infinite loop defined by
  the code; no recovery procedure is defined.

These are implementation details to keep in mind during extensions; they should
not be confused with features planned by the protocol format.

## Mobility commands

The IDs are defined in `cmdParser.h`:

| ID | Macro | Action | Parameter |
| --- | --- | --- | --- |
| `0x00` | `CMD_MOTORS_OFF` | Turns the motors off: PWM to zero on both outputs of each motor. | Ignored by the handler. |
| `0x01` | `CMD_MOTORS_BRAKE` | Applies PWM `255` to both outputs of each motor. | Ignored by the handler. |
| `0x02` | `CMD_MOTORS_FRONT` | Forward motion. | Speed. |
| `0x03` | `CMD_MOTORS_BACK` | Reverse motion. | Speed. |
| `0x04` | `CMD_MOTORS_LEFT` | Lateral motion to the left. | Speed. |
| `0x05` | `CMD_MOTORS_RIGHT` | Lateral motion to the right. | Speed. |
| `0x06` | `CMD_MOTORS_RLEFT` | Counterclockwise rotation. | Speed. |
| `0x07` | `CMD_MOTORS_RRIGHT` | Clockwise rotation. | Speed. |

The handlers pass speed and direction to `setMotorPWM(pinA, pinB, speed,
forward)`. If `speed` is zero, both outputs are set to zero; otherwise,
`forward == true` activates A and `forward == false` activates B.

The direction mapping implemented by the handlers is:

| Handler | Motor A | Motor B | Motor C | Motor D |
| --- | --- | --- | --- | --- |
| `handleMotorsFront` | A | A | A | A |
| `handleMotorsBack` | B | B | B | B |
| `handleMotorsLeft` | B | A | A | B |
| `handleMotorsRight` | A | B | B | A |
| `handleMotorsRLeft` | B | B | A | A |
| `handleMotorsRRight` | A | A | B | B |

Here A/B indicate which output of the motor pair receives the PWM, not a
physical left/right position. The mapping depends on wiring and drivers.

## Motor outputs

The pins are defined in `cmdParser.h` and configured as outputs in `setup()`:

| Motor | Pin 1 | Pin 2 |
| --- | --- | --- |
| A | PA0 | PB10 |
| B | PA1 | PB11 |
| C | PB13 | PB14 |
| D | PB4 | PB5 |

The primitives in `cmdParser.cpp` are the lowest level of control:

- `setMotorPWM()` selects direction and duty cycle;
- `setMotorOff()` sets both outputs to zero;
- `setMotorBrake()` sets both outputs to `255`.

Always verify that the pins, PWM channels, driver, and electrical meaning of
shutdown/braking match the hardware before modifying these primitives.

## How to add a mobility command

To add a command that belongs to the motor group:

1. Choose a free ID and define the macro `CMD_MOTORS_...` in `cmdParser.h`,
   avoiding collisions with existing IDs.
2. Declare the handler in `cmdParser.h` with the appropriate parameter (for
   example `uint8_t speed` if speed is needed).
3. Add a `case` in `executeCommand()` in `cmdParser.cpp`. The `case` must call
   the handler and end with `break`.
4. Implement the handler in `cmdParser.cpp`. For four-motor motion, reuse
   `setMotorPWM()` by specifying the pins and direction for each motor.
5. Verify the frame generation on the master side and reception on the slave
   side. Before testing movement with motors connected, check the outputs with
   the robot lifted or the motors disconnected.

Schematic example:

```cpp
// cmdParser.h
#define CMD_MOTORS_EXAMPLE 0x08
void handleMotorsExample(uint8_t speed);

// cmdParser.cpp: inside executeCommand()
case CMD_MOTORS_EXAMPLE:
  handleMotorsExample(param);
  break;

// cmdParser.cpp: implementation
void handleMotorsExample(uint8_t speed) {
  // Set direction and speed for each motor here.
}
```

To make the frame parameter effective, also update `loop()` in `spi_slave.ino`
so it passes `spiRxBuffer[2]` instead of the fixed value `100`. The master must
send the same ID and encode the speed in the same byte.

## How to add a group or a peripheral

For now, `grpID` is received and passed to `executeCommand()`, but ignored. To
introduce distinct groups, modify `executeCommand()` so it routes based on both
`grpID` and `cmdID`; add the definitions and handlers of the new group in the
appropriate files. Update the master firmware and protocol documentation at the
same time.

If the new peripheral requires more data or a different frame length, adding a
`case` alone is not enough: `BUFFER_SIZE`, HAL reception, byte interpretation,
and the master-side protocol must all be updated together.
