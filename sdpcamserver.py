from flask import Flask, render_template, Response
from flask import request
import cv2
import time
from threading import Thread



class myserver:
	def openCap(self):
		self.cap = cv2.VideoCapture(0)

app = Flask(__name__)
ServerCam = myserver()
ServerCam.openCap()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

'''
def gen():
    """Video streaming generator function."""
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1
'''
def get_frame():
	while True:
		ret , frame = ServerCam.cap.read()
		ret2, frame2 = cv2.imencode('.jpg',frame)
		stringData2=frame2.tostring()
		yield (b'--frame\r\n'
		b'Content-Type: image/jpeg\r\n\r\n'+stringData2+b'\r\n')
		
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
	shutdown_server()
	ServerCam.cap.release()
	return 'Server shutting down...'
	
def startServerCam():
	try:
		app.run(host='0.0.0.0',port ='8080',threaded= True)
	except KeyboardInterrupt:
		shutdown_server()	
def startServer():
	Thread(target=startServerCam, name='SERVER').start()

