#!/usr/bin/env python
# UL PeF, Rok Cernelic, 2014

import RPi.GPIO as PORTD
from time import sleep
import spidev
from RoPi_lib_CharLCD import Adafruit_CharLCD
from RoPi_lib_MCP230XX import Adafruit_MCP230XX
from RoPi_lib_MCP230XX import MCP230XX_GPIO
from RoPi_lib_PCA9685 import PWM



# ===========================================================================
# LIB: ADC on PORTA
# ===========================================================================
# Establish SPI Connection on Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0, 0)

def PORTA(channel):
    r = spi.xfer([1, (8 + channel) << 4, 0])
    adc = ((r[1]&3) << 8) + r[2]
    #percentage = int(round(adc/10.23))
    return adc
 
    

# ===========================================================================
# LIB: button on PORTB
# ===========================================================================
PORTB = Adafruit_MCP230XX(address = 0x20, num_gpios = 8)

# set PORTB as input
PORTB.setup(0, PORTB.IN)
PORTB.setup(1, PORTB.IN)
PORTB.setup(2, PORTB.IN)
PORTB.setup(3, PORTB.IN)
PORTB.setup(4, PORTB.IN)
PORTB.setup(5, PORTB.IN)
PORTB.setup(6, PORTB.IN)
PORTB.setup(7, PORTB.IN)

# set internal pullup resistor
PORTB.pullup(0, 1)
PORTB.pullup(1, 1)
PORTB.pullup(2, 1)
PORTB.pullup(3, 1)
PORTB.pullup(4, 1)
PORTB.pullup(5, 1)
PORTB.pullup(6, 1)
PORTB.pullup(7, 1)



# ===========================================================================
# LIB: DC MOTOR on PORTC
# ===========================================================================
PORTC = Adafruit_MCP230XX(address = 0x22, num_gpios = 8)

# for motor speed control enable PWM
PORTE = PWM(0x40, debug=True)
f = 50 # Set frequency
PORTE.frequency(f)

# motor1:
PORTC.setup(0, PORTC.OUT)
PORTC.setup(1, PORTC.OUT)

# motor2:
PORTC.setup(2, PORTC.OUT)
PORTC.setup(3, PORTC.OUT)

# motor3:
PORTC.setup(4, PORTC.OUT)
PORTC.setup(5, PORTC.OUT)

# motor4:
PORTC.setup(6, PORTC.OUT)
PORTC.setup(7, PORTC.OUT)



# ===========================================================================
# LIB: DC MOTOR on PORTD
# ===========================================================================
PORTD.setmode(PORTD.BCM)
PORTD.setwarnings(False)

# motor5:
PORTD.setup(23, PORTD.OUT)
PORTD.setup(24, PORTD.OUT)

# motor6:
PORTD.setup(25, PORTD.OUT)
PORTD.setup(27, PORTD.OUT)



# ===========================================================================
# LIB: PWM on PORTE
# ===========================================================================
'''# Initialise the PWM device using the default address
PORTE = PWM(0x40, debug=True)
f = 50 # Set frequency
PORTE.frequency(f)'''

# pulse width (refer servo datasheet and finetune for min and max servo position)
servoMin = 0.7 # tipical 0.5ms
servoMax = 2.6 # tipical 2.5ms

# Duty Cycle
DCmin = int((servoMin * 4095 * f) / 1000)
DCmax = int((servoMax * 4095 * f) / 1000)

# exapmles of manual servo position input
# DC = DCmin + ((DCmax - DCmin) * (ADC / 1023))         if ADC is 10bit ADC
# DC = DCmin + ((DCmax - DCmin) * (percent / 100))      if percent is 1 - 100
# DC = DCmin + ((DCmax - DCmin) * (input / rangeMax))   if input is a number in rangeMax, could use servo angle



# ===========================================================================
# LIB: LCD as GPIO on MCP23008
# ===========================================================================
bus = 1         # rev2 = 1, rev1 =0
address = 0x21  # I2C address of the MCP230xx chip.
gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.

# Create MCP230xx GPIO adapter.
mcp230xx = MCP230XX_GPIO(bus, address, gpio_count)
mcp230xx.setup(6, mcp230xx.OUT)
mcp230xx.output(6, 0)


# pin_rs = 25, pin_e = 24, pins_db = [23, 17, 27, 22]
#       GPIO   LCD   Adafruit  RoPi prototip
# RS    25      4       1       7
# E     24      6       2       5
# DB4   23      11      3       4
# DB5   17      12      4       3
# DB6   27      13      5       2
# DB7   22      14      6       1

# Create LCD, passing in MCP GPIO adapter.
LCD = Adafruit_CharLCD(pin_rs = 7, pin_e = 5, pins_db = [4, 3, 2, 1], GPIO = mcp230xx)
