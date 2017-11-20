import datetime
import time

from threading import Thread
from sdpcamserver import myserver

import sdpcamserver
import cv2
import configparser

import subprocess as sp
#import RPi.GPIO as GPIO
import os
from urllib.request import urlopen

class waktu:
	#def __init__(self):
		#self.stopped = False
	def loadConfig(self):
		self.config = configparser.SafeConfigParser()
		self.config.read('SMADHARMAPUTRA.ini')
		self.state = self.config.get('status','status')
		self.jam1 = self.config.get('alarmcam1','hour')
		self.jam2 = self.config.get('alarmcam2','hour')
		self.jam3 = self.config.get('alarmcam3','hour')
		self.jam4 = self.config.get('alarmcam4','hour')
		self.durasi1 = self.config.get('alarmcam1','durasi')
		self.durasi2 = self.config.get('alarmcam2','durasi')
		self.durasi3 = self.config.get('alarmcam3','durasi')
		self.durasi4 = self.config.get('alarmcam4','durasi')
		self.bell_on1 = self.config.get('alarmrelay1','time_on')
		self.bell_on2 = self.config.get('alarmrelay2','time_on')
		self.bell_on3 = self.config.get('alarmrelay3','time_on')
		self.bell_on4 = self.config.get('alarmrelay4','time_on')
		self.bell_off1 = self.config.get('alarmrelay1','time_off')
		self.bell_off2 = self.config.get('alarmrelay2','time_off')
		self.bell_off3 = self.config.get('alarmrelay3','time_off')
		self.bell_off4 = self.config.get('alarmrelay4','time_off')
	def start(self):
		x = Thread(target=self.update)
		x.start()
	def update(self):
		while True:
			self.clock = datetime.datetime.now().strftime('%H:%M:%S')
			time.sleep(1)
			if self.stopped:
				break
				print('[INFO]-Alarm Has Been Disabled')
			#if self.state == '1':
			#if self.stopped == False:
			if self.clock == self.jam1:
				print('[INFO]-Alarm Trigerred..')
				Thread(target=self.cam, args=[self.durasi1]).start()
			if self.clock == self.jam2:
				print('[INFO]-Alarm Trigerred..')
				Thread(target=self.cam, args=[self.durasi2]).start()
			if self.clock == self.jam3:
				print('[INFO]-Alarm Trigerred..')
				Thread(target=self.cam, args=[self.durasi3]).start()
			if self.clock == self.jam4:
				print('[INFO]-Alarm Trigerred..')
				Thread(target=self.cam, args=[self.durasi4]).start()
				
			#if self.state == '0':
			
			print('[TIME] - '+self.clock)
			
	def startCaptureCam(self, name):
		url = 'http://localhost:8080/video_feed'
		try:
			print("[INFO] opening stream..")
			urlopen(url)
			
		except:
			print("[FAIL] failed opening cam from stream")
			try:
				print("[INFO] recording now livecam")
			except:
				print("[FAIL] failed opening cam from webcam")
			else:
				self.CaptureCam(name,0)
				
		else:
			print("[INFO] recording now")
			self.CaptureCam(name,'http://localhost:8080/video_feed')
			
		finally:
			print("[INFO] done.")
			
	def CaptureCam(self, name, source):
		cap = cv2.VideoCapture(source)
		time.sleep(2)
		(grab, frame) = cap.read()
		for i in range(100):
			(grab, frame) = cap.read()
		cv2.imwrite(name, frame)
	def startRecordCam(self, name):
		url = 'http://localhost:8080/video_feed'
		try:
			print("[INFO] opening stream..")
			urlopen(url)
			
		except:
			print("[FAIL] failed opening cam from stream")
			try:
				print("[INFO] recording now livecam")
			except:
				print("[FAIL] failed opening cam from webcam")
			else:
				self.liveRecordCam(name)
				
		else:
			print("[INFO] recording now")
			self.httpRecordCam()
			
		finally:
			print("[INFO] done.")
	
	def httpRecordCam(self,name):
		sp.call(["ffmpeg",
			"-f","mjpeg",
			"-video_size", "640x480" ,
			#"-rtbufsize", "702000k",
			"-framerate","7.5",
			"-i", "http://localhost:8080/video_feed",
			"-f", "lavfi",
			"-i", "anullsrc=channel_layout=stereo:sample_rate=40000",
			"-vcodec", "libx264",
			"-minrate", "256k",
			"-b:v", "256k",
			"-maxrate", "512k",
			"-t", "00:00:10",
			#"-r", "10",
			"-crf","28",
			"-preset","slow",
			"-pix_fmt","yuv420p",
			"-c:a", "aac",
			"-f","mp4",
			name])
	def liveRecordCam(self,name):
		sp.call(["ffmpeg",
			"-f","v4l2",
			"-video_size", "640x480" ,
			"-rtbufsize", "702000k",
			"-framerate","10",
			"-i", "/dev/video0",
			"-f", "lavfi",
			"-i", "anullsrc=channel_layout=stereo:sample_rate=40000",
			"-vcodec", "libx264",
			"-minrate", "256k",
			"-b:v", "256k",
			"-maxrate", "512k",
			"-t", "00:00:10",
			"-r", "10",
			"-crf","28",
			"-preset","slow",
			"-pix_fmt","yuv420p",
			"-c:a", "aac",
			"-f","mp4",
			name])
	def cam(self,duration):
		filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
		sdpcamserver.startServer()
		time.sleep(1)
		sp.call(["ffmpeg",
			"-f","mjpeg",
			#"-video_size", "640x480" ,
			"-framerate","7.5",
			"-i", "http://localhost:8080/video_feed",
			"-f", "lavfi",
			"-i", "anullsrc=channel_layout=stereo:sample_rate=40000",
			"-vcodec", "libx264",
			"-t", duration,
			"-c:a", "aac",
			"-f","mp4","temp"+filenamevid])

		"""sp.call(["ffmpeg",
			"-f","v4l2",
			"-framerate", "10",
			"-rtbufsize", "702000k",
			"-i", "/dev/video0",
			"-f", "lavfi",
			"-i", "anullsrc=channel_layout=stereo:sample_rate=10",
			"-c:v", "libx264",
			"-minrate", "128k",
			"-b:v", "192k",
			"-maxrate", "256k",
			"-t", duration,
			"-c:a", "aac", "temp"+filenamevid])"""
		sp.call(["ffmpeg",
			"-i","temp"+filenamevid,
			"-video_size", "640x480",
			"-vcodec","libx264",
			"-acodec","copy",
			"-minrate", "192k",
			"-b:v", "192k",
			"-maxrate", "256k",
			"-preset","slow",
			"-pix_fmt","yuv420p",
			"-crf","27",
			"-f","mp4",
			filenamevid])
		os.remove("temp"+filenamevid)
		urlopen('http://localhost:8080/shutdown')
	def stop(self):
		self.stopped = True
	def setStart(self):
		self.stopped = False