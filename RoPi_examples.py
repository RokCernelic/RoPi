#!/usr/bin/env python
# UL PeF, Rok Cernelic, 2014
from RoPi_lib import *



# ===========================================================================
# PORTA (ANALOG INPUT)
# ===========================================================================
PORTA(pin)                      # 0-7 pins on PORTA are analog input pins

# Example 1
while True:
    print PORTA(1)




# ===========================================================================
# PORTB (DIGITAL INPUT, OUTPUT)
# ===========================================================================
PORTB.setup(pin, PORTB.IN)      # Ignore. Allerady set in the library for pins 0-7
PORTB.pullup(pin, 1)            # Ignore. Allerady set in the library for pins 0-7
PORTB.input(pin)                # Call input pin 0-7

PORTB.setup(pin, PORTB.OUT)     # Set pin as output (overrides library setup)
PORTB.output(pin, value)        # Set output pin 0-7 as High/Low

# Example 2
# Checkinh buttons 0-7
while True:
    if PORTB.input(7) == 0:
        print "7"
    if PORTB.input(6) == 0:
        print "6"
    if PORTB.input(5) == 0:
        print "5"
    if PORTB.input(4) == 0:
        print "4"
    if PORTB.input(3) == 0:
        print "3"
    if PORTB.input(2) == 0:
        print "2"
    if PORTB.input(1) == 0:
        print "1"
    if PORTB.input(0) == 0:
        print "0"

# Example 3:
# Blink pin7
while True:
    PORTB.output(7, 1)
    sleep(1)
    PORTB.output(7, 0)
    sleep(1)




# ===========================================================================
# PORTC (DIGITAL OUTPUT, MOTOR DRIVER, MAX. 0.6A)
# ===========================================================================
PORTC.output(pin, value)        # Set output pin 0-7 as High/Low
PORTE.pwm(0, DC)                # Set PWM to motor1 - PORTC(0-1), DC 0-4095
PORTE.pwm(1, DC)                # Set PWM to motor2 - PORTC(2-3), DC 0-4095 
PORTE.pwm(2, DC)                # Set PWM to motor3 - PORTC(4-5), DC 0-4095 
PORTE.pwm(3, DC)                # Set PWM to motor4 - PORTC(6-7), DC 0-4095

# Example 4
# Disconnect PWM jumpers for max motor speed. No PORTE.pwm lines needed
try:
    while True:
        PORTC.output(4, 0)
        PORTC.output(5, 1)
except KeyboardInterrupt:
    # stop
    PORTC.output(4, 0)
    PORTC.output(5, 0)

# Example 5 
# Cycle motor3 speed from 0 to 4095 an back
PORTC.output(4, 0)
PORTC.output(5, 1)
def speed():
        for DC in range(0, 4095, 10):
            PORTE.pwm(2, DC)
            sleep(0.01)
        for DC in range(4095, -1, -10):
            PORTE.pwm(2, DC)
            sleep(0.01)

try:
    while True:
        speed()
except KeyboardInterrupt:
    # stop
    PORTC.output(4, 0)
    PORTC.output(5, 0)
    

    
    
# ===========================================================================
# PORTD (GPIO PINS: GPIO4, GPIO17, GPI18, GPIO22, GPIO23, GPIO24, GPIO25, GPIO27)
# ===========================================================================
PORTD.setmode(PORTD.BCM)        # Set pin numbering                                

PORTD.setup(pin, PORTD.IN)      # Set pin as input
PORTD.input(pin)                # Call input pin

PORTD.setup(pin, PORTD.OUT)     # Set pin as output
PORTD.output(pin, value)        # Set output pin as High/Low
    
# Use PORTD in examples 2-4




# ===========================================================================
# PORTE (SERVO PWM DRIVER)
# ===========================================================================
PORTE.pwm(pin, DC)                # Pin 0-15, DC = DutyCycle, must be integer
                                  # Frequency set to 50Hz, modify in library


# DCmin is pre-set in RoPi_lib
# DCmax is pre-set in RoPi_lib

# Example 6
while True:
    # PORTE.pwm(channel, position-DC)
    PORTE.pwm(8, DCmin)
    sleep(2)
    PORTE.pwm(8, DCmax)
    sleep(2)

# Example 7
# Control servo position with potentiometer connected to 10bit ADC input (PORTA)
while True:
    ADC = PORTA(0)
    DC = DCmin + ((DCmax - DCmin) * (ADC / 1023.0))
    PORTE.pwm(8, int(DC))

# examples of manual servo position input
DC = DCmin + ((DCmax - DCmin) * (percent / 100))      # percent 1 - 100
DC = DCmin + ((DCmax - DCmin) * (input / rangeMax))   # input is a number in rangeMax, could use servo angle




# ===========================================================================
# LCD as GPIO on MCP23008
# ===========================================================================
# LCD functions
LCD.begin(self, cols, lines)
LCD.home(self)              # set cursor position to zero
LCD.clear(self)             # command to clear display
LCD.setCursor(self, col, row) # Set kursos position
LCD.noDisplay(self)         # Turn the display off (quickly)
LCD.display(self)           # Turn the display on (quickly)
LCD.noCursor(self)          # Turns the underline cursor off
LCD.cursor(self)            # Turns the underline cursor on
LCD.noBlink(self)           # Turn the blinking cursor off
LCD.blink(self)             # Turn the blinking cursor on
LCD.DisplayLeft(self)       # These commands scroll the display without changing the RAM
LCD.scrollDisplayRight(self)# These commands scroll the display without changing the RAM
LCD.leftToRight(self)       # This is for text that flows Left to Right
LCD.rightToLeft(self)       # This is for text that flows Right to Left
LCD.autoscroll(self)        # This will 'right justify' text from the cursor
LCD.noAutoscroll(self)      # This will 'left justify' text from the cursor

# Example 8
# Print to two line (max 16 char)
message = raw_input("Vnos: ")
while 1:
    LCD.clear()
    LCD.message("%s\n%s" % ((message[0:8]), (message[8:16])))
    sleep(2)
