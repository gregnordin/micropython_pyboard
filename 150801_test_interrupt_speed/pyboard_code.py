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
        self.tick = (self.tick + 1) % 10000000

micropython.alloc_emergency_exception_buf(100)

micros_timer = pyb.Timer(2, prescaler=83, period=0x3ffffff)

usb = pyb.USB_VCP()
Heartbeat()
sst = serial_speed_test(2)
running_flag = False
write_flag = False

while True:
    if running_flag is False:
        if usb.any():
            input = usb.readline()
            usb.write(input+'\n')
            if input.startswith('start'):
                write_flag = True
            elif input.startswith('stop'):
                write_flag = False
            elif input.startswith('reset'):
                write_flag = False
    if write_flag:
        if sst.tick_ready:
            s = "%d,%d\n" % (sst.tick, sst.micros_timer)
            usb.write(s)
            sst.tick_ready = False
        
