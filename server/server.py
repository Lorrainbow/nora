#!/usr/bin/python

import SimpleHTTPServer
import SocketServer
import re
import os.path
import os
import picamera

import servo

PORT = 80
STATIC_ROOT = '/var/www/static/'
ROOT = '/var/www/'

class ServoHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    camera = picamera.PiCamera(framerate=50, resolution=(1280,720))
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        if s.path == "/":
            s.path = "/static/index.html"
        if s.path.startswith("/pan"):
            return s.pan()
        if s.path.startswith("/html/cam_pic"):
            return s.pic()
        if s.path.startswith("/static/"):
            s.path = s.path[8:]
            return s.static()

    def pan(s): 
        m = re.search(r'value=([+-]?\d+(\.\d+)?)', s.path)
        if m:
            val = float(m.group(1))
            servo.set_pos(val)
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

    def pic(s):
        s.send_response(200)
        s.send_header("Content-type", "image/jpeg")
        s.end_headers()
        s.camera.capture(s.wfile,'jpeg',use_video_port=True)

    def static(s):
        if s.path[0] == '/':
            s.path = s.path[1:]
        path = os.path.realpath(os.path.join(os.getcwd(),s.path))
        print path
        if not path.startswith(STATIC_ROOT):
            s.send_error(403)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(s)
        
httpd = SocketServer.TCPServer(("", PORT), ServoHandler)
ServoHandler.camera.iso = 800
os.chdir(STATIC_ROOT)
servo.init()
print "serving at port", PORT
httpd.serve_forever()
