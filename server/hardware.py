#!/usr/bin/python
import subprocess

import wiringpi as wpi
import neopixel
import time


class Servo(object):
    MAX = 250
    MIN = 60
    OFFSET = 0
   
    @classmethod
    def init(cls):
        subprocess.call(("killall","servod"))
        time.sleep(0.05)
        subprocess.call(("servod","--p1pins=13","--pcm"))
        time.sleep(0.2)
        cls.set_pos(0)

    @classmethod
    def set_pos(cls,value):
        """Set the servo to point to angle value (-90 -> 90)"""
        value -= cls.OFFSET
        if value > 360:
            value  = value % 360
        if value > 180:
            value -= 360
        value = max(-90,value)
        value = min(90,value)
        cls.value = value
        pos = cls.MIN+((value+90)*(cls.MAX-cls.MIN))/180
        with open("/dev/servoblaster","w") as f:
            f.write("0=%d\n" % int(pos))
            f.close()    
        return value
        
    def reset_pos(cls):
        cls.OFFSET = cls.value

class Drive(object):
    #pin numbers
    L1 = 7
    L2 = 8
    R1 = 10
    R2 = 9

    @classmethod
    def init(cls):
        #use pwm on inputs so motors don't go too fast
        wpi.wiringPiSetupGpio()
        for pin in (cls.L1, cls.L2, cls.R1, cls.R2):
            wpi.pinMode(pin, wpi.OUTPUT)
            wpi.softPwmCreate(pin,0,100)

    @classmethod
    def set_motors(cls,left,right):
        for value,pins in ((left, (cls.L1, cls.L2)), (right, (cls.R1, cls.R2))):
            if value>=0:
                wpi.softPwmWrite(pins[1],0)
                wpi.softPwmWrite(pins[0],int(value))
            else: 
                wpi.softPwmWrite(pins[0],0)
                wpi.softPwmWrite(pins[1],int(-value))
            

    # stop(): Stops both motors
    @classmethod
    def stop(cls):
        cls.set_motors(0,0)
        
    # forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
    @classmethod
    def forward(cls,speed):
        cls.set_motors(speed,speed)
        
    # reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
    @classmethod
    def reverse(cls,speed):
        cls.set_motors(-speed,-speed)

    # spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
    @classmethod
    def spinLeft(cls,speed):
        cls.set_motors(-speed,speed)
        
    # spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
    @classmethod
    def spinRight(cls,speed):
        cls.set_motors(speed,-speed)
        
    # turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
    @classmethod
    def turnForward(cls,leftSpeed, rightSpeed):
        cls.set_motors(leftSpeed,rightSpeed)
        
    # turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
    @classmethod
    def turnReverse(cls,leftSpeed, rightSpeed):
        cls.set_motors(-leftSpeed,-rightSpeed)


class Led(object):
    LED_COUNT   = 2      # Number of LED pixels.
    LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
    LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
    
    @classmethod
    def init(cls):
        # Create NeoPixel object with appropriate configuration.
        cls.strip = neopixel.Adafruit_NeoPixel(cls.LED_COUNT, cls.LED_PIN, cls.LED_FREQ_HZ, cls.LED_DMA, cls.LED_INVERT)
        # Intialize the library (must be called once before other functions).
        cls.strip.begin()
        
    @classmethod    
    def setColours(cls,col1,col2):
        """set LED1 to col1 (a 3-tuple) and LED2 to col2"""
        time.sleep(0.01)
        cls.strip.setPixelColor(0,neopixel.Color(*col1))
        cls.strip.setPixelColor(1,neopixel.Color(*col2))
        cls.strip.show()


def init():
    Servo.init()
    Drive.init()
    Led.init()

if __name__=="__main__":
    import sys
    import time
    init()
    time.sleep(3)
    Servo.set_pos(80)
    time.sleep(3)
    Led.setColours([0,0,255],[255,0,0])
    Drive.forward(15)
    time.sleep(3)
    Servo.set_pos(-80)
    Drive.reverse(15)    
    Led.setColours([255,0,0],[0,0,255])
    time.sleep(3)
    Drive.stop()
    Servo.set_pos(0)
    Led.setColours([0,0,0],[0,0,0])

