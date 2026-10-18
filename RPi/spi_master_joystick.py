#!/usr/bin/env python3
import spidev
import time
import pygame

# SPI configuration
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0
spi.bits_per_word = 8

# Controller setup (Pygame)
pygame.init()
pygame.joystick.init()

print("RPi SPI master started (mixed-logic controller)...")

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")
except Exception:
    print("No controller found!")
    raise SystemExit

# --- LOGIC DEFINITIONS ---

# Buttons that must send the command continuously (states)
tasti_movimento = {
    0: 2,  # Y -> forward
    1: 5,  # B -> right
    2: 3,  # A -> backward
    3: 4,  # X -> left
    4: 6,  # LB -> counterclockwise rotation
    5: 7   # RB -> clockwise rotation
}

# Buttons that send a command only once (events/pulses)
tasti_funzione = {
    8: 0,  # select -> motors off
    9: 1   # start -> motors locked
}

# Register for function buttons to detect whether they were already pressed in the previous cycle
stato_precedente_funzione = {tasto: False for tasto in tasti_funzione.keys()}
# Current movement state: active movement button or None if none is pressed
movimento_attivo_precedente = None

try:
    while True:
        # Update the internal Pygame states
        pygame.event.pump()

        # 1. MOVEMENT BUTTON HANDLING (single trigger on press / stop on release)
        tasto_movimento_attuale = None
        cmd_movimento_attuale = None
        for tasto, cmd in tasti_movimento.items():
            if joystick.get_button(tasto):
                tasto_movimento_attuale = tasto
                cmd_movimento_attuale = cmd
                break  # Priority to the first pressed button

        if tasto_movimento_attuale is not None:
            if movimento_attivo_precedente != tasto_movimento_attuale:
                print(f"MOVEMENT: button {tasto_movimento_attuale} activated -> SPI {cmd_movimento_attuale}")
                spi.xfer2([0x01, cmd_movimento_attuale, 0])
                movimento_attivo_precedente = tasto_movimento_attuale
        else:
            if movimento_attivo_precedente is not None:
                print("MOVEMENT: button released -> SPI 0 (stop)")
                spi.xfer2([0x01, 0, 0])
                movimento_attivo_precedente = None

        # 2. FUNCTION BUTTON HANDLING (single event)
        for tasto, cmd in tasti_funzione.items():
            stato_attuale = joystick.get_button(tasto)

            # If it is pressed NOW but was not pressed in the PREVIOUS cycle (rising edge)
            if stato_attuale and not stato_precedente_funzione[tasto]:
                print(f"SINGLE EVENT: button {tasto} activated -> SPI {cmd}")
                spi.xfer2([0x01, cmd, 0])

            # Update the register for the next cycle
            stato_precedente_funzione[tasto] = stato_attuale

        # Small delay to avoid overloading the CPU and SPI bus
        # 0.05s = 20Hz, enough for the robot's responsiveness
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nShutdown in progress...")
    spi.close()
