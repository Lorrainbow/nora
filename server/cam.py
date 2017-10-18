import io
import picamera
import threading
import time

from twisted.web.resource import Resource

class SplitFrames(object):
    def __init__(self):
        self.last_frame = None
        self.stream = io.BytesIO()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            self.last_frame = self.stream.getvalue()
            #create a new stream to take the next load of data
            self.stream = io.BytesIO()
        self.stream.write(buf)

class Cam(Resource):
    isLeaf = True
    def __init__(self):
        self.output = SplitFrames()
        self.recording = True
        self.thread = threading.Thread(target=self.thread_worker)
        self.thread.start()
        from twisted.internet import reactor
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        
    def render_GET(self, request):
        request.defaultContentType = "image/jpeg"
        return self.output.last_frame
        
    def thread_worker(self):
        with picamera.PiCamera(resolution=(320,240), framerate=10) as camera:
            camera.hflip = True
            camera.vflip = True
            time.sleep(2)
            start = time.time()
            camera.start_recording(self.output, format='mjpeg')
            
            while self.recording:
                camera.wait_recording(0.2)
            camera.stop_recording()

    def stop(self):
        self.recording=False


