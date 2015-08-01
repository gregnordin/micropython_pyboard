import micropython
micropython.alloc_emergency_exception_buf(100)

import pyb
import micropython

class Heartbeat(object):

    def __init__(self):
        self.tick = 0
        self.led = pyb.LED(4) # 4 = Blue
        tim = pyb.Timer(4)
        tim.init(freq=10)
        tim.callback(self.heartbeat_cb)

    def heartbeat_cb(self, tim):
        if self.tick <= 3:
            self.led.toggle()
        self.tick = (self.tick + 1) % 10

class serial_speed_test(object):

    def __init__(self, freq_Hz):
        self.tick = 0
        self.tick_ready = False
        self.micros_timer = micros_timer.counter()
        self.freq_Hz = freq_Hz
        tim1 = pyb.Timer(1)
        tim1.init(freq=freq_Hz)
        tim1.callback(self.serial_speed_test_cb)

    def serial_speed_test_cb(self, tim1):
        self.micros_timer = micros_timer.counter()
        self.tick_ready = True
        #print(micros_timer.counter(), ',', 40*self.tick)
        self.tick = (self.tick + 1) % 100

micropython.alloc_emergency_exception_buf(100)

micros_timer = pyb.Timer(2, prescaler=83, period=0x3ffffff)

usb = pyb.USB_VCP()
Heartbeat()
sst = serial_speed_test(2)

while True:
    if sst.tick_ready:
        s = "%d,%d\n" % (sst.tick, sst.micros_timer)
        usb.write(s)
        #usb.write("confirmed\n")
        sst.tick_ready = False
        
