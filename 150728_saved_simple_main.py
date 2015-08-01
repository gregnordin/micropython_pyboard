# To get a REPL in Terminal:
screen /dev/tty.usbmodem*

# To open a serial connection to the pyboard on my macbook pro retina:
ser = serial.Serial('/dev/tty.usbmodem1452',9600)

---------------------------------------
# Cool effect with all of the LEDs

import pyb

leds = [pyb.LED(i) for i in range(1,5)]

n = 0
while True:
    n = (n + 1) % 4
    leds[n].toggle()
    pyb.delay(50)

---------------------------------------
# Just changes blue LED intensity
import pyb
led = pyb.LED(4)
intensity = 0
while True:
    intensity = (intensity + 1) % 255
    led.intensity(intensity)
    pyb.delay(1)
    
---------------------------------------
# Add an analog read and write value to serial port
import pyb

adc = pyb.ADC(pyb.Pin.board.X19)
leds = [pyb.LED(i) for i in range(1,5)]

n = 0
while True:
    n = (n + 1) % 4
    temp =  adc.read()
    print(n, temp)
    leds[n].toggle()
    pyb.delay(50)

