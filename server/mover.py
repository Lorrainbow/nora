#!/usr/bin/env python

import subprocess
import cwiid
import time
import re
from twisted.internet import threads
from twisted.web.resource import Resource


from hardware import Drive, Led, Servo
import hardware

BLUE = (0,0,255)
LIGHT_OFF = (0,0,0)
LIGHT_ON = (255,255,255)

BLUETOOTH_TIMEOUT = 1000

SPEED = 70
TURN_MULTIPLIER = 2.5

class Wii(object):
    def __init__(self):
        subprocess.call(("hciconfig","hci0","piscan"))
        Led.init()
        Drive.init()
        time.sleep(0.1)
        self.lights = False
        Led.setColours(LIGHT_OFF,LIGHT_OFF)
        self.y_offset = 0
        self.wm = None
        self.connect()
        from twisted.internet import reactor
        reactor.addSystemEventTrigger('before', 'shutdown', self.finish)
       
    
    def poll(self):
        # this will be called repeatedly by twisted
        if self.wm=="PENDING":
            if self.lights:
                Led.setColours(BLUE,LIGHT_OFF)
            else:
                Led.setColours(LIGHT_OFF,BLUE)
            self.lights = not self.lights
            return
        try:
            y = self.wm.state['acc'][1]
            btns = self.wm.state['buttons']
            d = threads.deferToThread(self.wm.request_status)
            d.addErrback(self.connect)
        except (ValueError, IOError, AttributeError) as e:
            # problem receiving data from wiimote (or not connected yet...)
            print "connection lost, shouldn't really get here very often..."
            print e.message
            self.connect()
            return
        y = y - self.y_offset
        if abs(y)<4:
            y = 0
        y = y * TURN_MULTIPLIER
        accel = btns & (cwiid.BTN_1 | cwiid.BTN_2)
        if accel == cwiid.BTN_1:
            Drive.turnForward(SPEED+y,30-y)
        elif accel == cwiid.BTN_2:
            Drive.turnReverse(SPEED+y,30-y)
        else:
            if y < 0:
                Drive.spinRight(-y)
            elif y > 0:
                Drive.spinLeft(y)
            else:
                Drive.stop()
        if btns & cwiid.BTN_A:
            if self.lights:
                Led.setColours(LIGHT_OFF,LIGHT_OFF)
                self.lights=False
            else:
                Led.setColours(LIGHT_ON,LIGHT_ON)
                self.lights=True
                
    def _connect(self):
        wm = cwiid.Wiimote()
        #get bt address
        connected_devices = subprocess.check_output(("hcitool","con"))
        addresses = re.findall(r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))",connected_devices)
        for i in addresses:
            name = subprocess.check_output(("hcitool","name",i[0]))
            if name.strip()=="Nintendo RVL-CNT-01":
                subprocess.call(("hcitool","lst",i[0],str(BLUETOOTH_TIMEOUT*16/10)))
        wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        time.sleep(0.1)
        return wm
     
    def connect(self, failure=None):
        print "connecting..."
        if failure:
            print "previous failure:"
            print failure.getErrorMessage()
        if isinstance(self.wm,cwiid.Wiimote):
            self.wm.close()
        self.wm = "PENDING"
        Drive.stop()
        d = threads.deferToThread(self._connect)
        d.addCallbacks(self.connected,self.connect)
            
    def connected(self,wm):
        try:
            self.y_offset = wm.state['acc'][1]
        except (ValueError, IOError, AttributeError, RuntimeError) as e:
            self.connect()
            return
        self.wm = wm
        print "connection complete"
        self.lights = False
        Led.setColours(LIGHT_OFF,LIGHT_OFF)
        
    def monitor(self):
        self.wm.request_status()
        
    def finish(self):
        Drive.stop()
        Led.setColours(LIGHT_OFF,LIGHT_OFF)
        
        
class Pan(Resource):
    isLeaf = True
    def __init__(self):
        Servo.init()
        
    def render_GET(self, request):
        if 'value' in request.args:
            value = float(request.args['value'][0])
            pos = Servo.set_pos(value)
            response = "Set camera position to %g" % pos
        else:
            response = "No position specified"
        return "<html><body>%s</body></html>" % response
        
        
if __name__=="__main__":
    from twisted.internet import reactor, task
    mover = Wii()
    l = task.LoopingCall(mover.poll)
    l.start(0.3)
    reactor.run()
