#!/usr/bin/env python

import sys
import io
import time
import os

from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor, endpoints, task
from twisted.internet.threads import deferToThread
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.python import log
#log.startLogging(sys.stdout)

import cam
import mover

STATIC_ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"../html"))

class Root(Resource):
    def getChild(self, name, request):
        print name
        if name == '':
            return File(STATIC_ROOT +'/index.html')
        return Resource.getChild(self, name, request)


root = Root()
root.putChild("static",File(STATIC_ROOT))
root.putChild("pan",mover.Pan())
root.putChild("cam",cam.Cam())
factory = Site(root)

endpoint = endpoints.TCP4ServerEndpoint(reactor, 80)
endpoint.listen(factory)
wii = mover.Wii()
l = task.LoopingCall(wii.poll)
l.start(0.3)

reactor.run()
