import telepot
import numpy as np
import datetime
import os
import subprocess as sp
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id,per_chat_id_except, per_chat_id_in, create_open, pave_event_space
import time
import configparser

from sdpcam import waktu
#------------------------------#
import sdpcamserver
#------------------------------#

config = configparser.SafeConfigParser()
config1 = configparser.SafeConfigParser()
x = waktu()

class SmartRoomChat(telepot.helper.ChatHandler):
	global config
	global x
	def __init__(self, *args, **kwargs):
		super(SmartRoomChat, self).__init__(*args, **kwargs)
		self.mn = True
		self.cam = 0
		
		
		self.konfigjam = ""
		self.konfigmenit = ""
		self.konfigdurasi = ""
		self.hasil = ""
		
		self.belljam = ""
		self.bellmenit = ""
		self.bellajam = ""
		self.bellamenit = ""
		self.bellhasil = ""
		self.bellahasil = ""
		
		self.statuskam = 0
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		command = msg['text']
		print ('Got command: %s' % command)
		print (chat_id)
		
		def papanmenu():
			keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				['Bel01','Bel02','Bel03','Bel04',],
				['Kamera01','Kamera02','Kamera03','Kamera04'],['Panduan']]			
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
			self.sender.sendMessage('[Panduan] untuk informasi lebih lanjut',reply_markup = replyKeyboardMakeup)
		
		def bellconfig(jam, alarm):
			a0 = ['BATAL']
			
			a1 =['00','01','02','03']
			a2 =['04','05','06','07']
			a3 =['08','09','10','11']
			a4 =['12','13','14','15']
			a5 =['16','17','18','19']
			a6 =['20','21','22','23']
			keyboardLayout = [a0,a1,a2,a3,a4,a5,a6]
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			b1 = ['00','05','10','15']
			b2 = ['20','25','30','35']
			b3 = ['40','45','50','55']
			keyboardLayout1 = [a0,b1,b2,b3]
			replyKeyboardMakeup1 = {'keyboard': keyboardLayout1, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			
			if jam == 'BATAL':
				self.close()
				
			if self.statuskam == 0:
				self.sender.sendMessage('Pada Jam Berapa?', reply_markup = replyKeyboardMakeup)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 1:
				self.belljam = jam
				self.sender.sendMessage('Pada Menit Berapa ?', reply_markup = replyKeyboardMakeup1)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 2:
				self.bellmenit = jam
				self.sender.sendMessage('Berakhir pada Jam ?', reply_markup = replyKeyboardMakeup)
				self.statuskam = self.statuskam + 1
			
			elif self.statuskam == 3:
				self.bellajam = jam
				self.sender.sendMessage('Berakhir pada Menit ?', reply_markup = replyKeyboardMakeup1)
				self.statuskam = self.statuskam + 1
			
			elif self.statuskam == 4:
				self.bellamenit = jam
				self.bellhasil = self.belljam+':'+self.bellmenit
				self.bellahasil = self.bellajam+':'+self.bellamenit
				config.read('SMADHARMAPUTRA.ini')
				config.set(alarm,'time_on',self.bellhasil+':00')
				config.set(alarm,'time_off',self.bellahasil+':00')
				with open('SMADHARMAPUTRA.ini','w+') as configfile:
					config.write(configfile)
				testjam = config.get(alarm,'time_on')
				testdurasi = config.get(alarm,'time_off')
				self.sender.sendMessage(alarm+' telah disetel setiap pukul '+testjam+' dan berakhir pada pukul '+testdurasi)
				self.close()
			elif self.statuskam == 5:
				print('Done.')
		
		def papankonfigurasi(jam, alarm):
			a0 = ['BATAL']
			a1 =['00','01','02','03']
			a2 =['04','05','06','07']
			a3 =['08','09','10','11']
			a4 =['12','13','14','15']
			a5 =['16','17','18','19']
			a6 =['20','21','22','23']
			keyboardLayout = [a0,a1,a2,a3,a4,a5,a6]
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			b1 = ['00','05','10','15']
			b2 = ['20','25','30','35']
			b3 = ['40','45','50','55']
			keyboardLayout1 = [a0,b1,b2,b3]
			replyKeyboardMakeup1 = {'keyboard': keyboardLayout1, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			c1 = ['05','10','15','20']
			c2 = ['25','30','35','40']
			c3 = ['45','50','55','60']
			keyboardLayout2 = [a0,c1,c2,c3]
			replyKeyboardMakeup2 = {'keyboard': keyboardLayout2, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			if jam == 'BATAL':
				papanmenu()
				self.statuskam = 4
				self.mn = True
				self.cam = 0
				menuutama(command)
				
			if self.statuskam == 0:
				self.sender.sendMessage('Pada Jam Berapa?', reply_markup = replyKeyboardMakeup)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 1:
				self.konfigjam = jam
				self.sender.sendMessage('Pada Menit Berapa ??', reply_markup = replyKeyboardMakeup1)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 2:
				self.konfigmenit = jam
				self.sender.sendMessage('Berapa Lama', reply_markup = replyKeyboardMakeup2)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 3:
				self.konfigdurasi = jam
				self.hasil = self.konfigjam+':'+self.konfigmenit
				config.read('SMADHARMAPUTRA.ini')
				config.set(alarm,'hour',self.hasil+':00')
				config.set(alarm,'durasi','00:'+self.konfigdurasi+':00')
				with open('SMADHARMAPUTRA.ini','w+') as configfile:
					config.write(configfile)
				testjam = config.get(alarm,'hour')
				testdurasi = config.get(alarm,'durasi')
				self.sender.sendMessage(alarm+' telah disetel setiap pukul '+testjam+' selama '+testdurasi+' Menit')
				self.mn = True
				self.statuskam = self.statuskam + 1
				self.cam = 0
				papanmenu()
				menuutama(command)
				
			elif self.statuskam == 4:
				print('Done.')
				
		
		
		def menuutama(commands):
			if commands == 'AMBIL GAMBAR':
				self.sender.sendMessage('AMBIL GAMBAR')
			elif commands == 'AMBIL VIDEO':
				self.sender.sendMessage('AMBIL VIDEO')
			elif commands == 'Panduan':
				self.bot.sendMessage(chat_id, text = 'AMBIL GAMBAR - Mengambil gambar pada CCTV \nAMBIL VIDEO - Merekam video selama 10 detik \nKamera01-04 - Mengoperasikan kamera pada waktu dan durasi yang telah ditentukan \nBel01-04 - Mengoperasikan Bell pada waktu yang telah ditentukan\n\nSMA Dharma Putra')
			elif commands == '/run':
				x.loadConfig()
				x.setStart()
				x.start()
				self.sender.sendMessage('AMBIL GAMBAR')
			elif commands == '/stop':
				x.stop()
				self.sender.sendMessage('AMBIL GAMBAR')
			elif commands == 'Kamera01':
				self.cam = 1
			elif commands == 'Kamera02':
				self.cam = 2
			elif commands == 'Kamera03':
				self.cam = 3
			elif commands == 'Kamera04':
				self.cam = 4
			elif commands == 'Bell01':
				self.cam = 5
			elif commands == 'Bell02':
				self.cam = 6
			elif commands == 'Bell03':
				self.cam = 7
			elif commands == 'Bell04':
				self.cam = 8
		
		if command == '/start':
			papanmenu()
		if self.mn == True:
			menuutama(command)
		
		if self.cam == 0:
			self.mn == True
			
		elif self.cam == 1:
			papankonfigurasi(command,'alarmcam1')
		elif self.cam == 2:
			papankonfigurasi(command,'alarmcam2')
		elif self.cam == 3:
			papankonfigurasi(command,'alarmcam3')
		elif self.cam == 4:
			papankonfigurasi(command,'alarmcam4')
			
		elif self.cam == 5:
			bellconfig(command,'alarmrelay1')
		elif self.cam == 6:
			bellconfig(command,'alarmrelay2')
		elif self.cam == 7:
			bellconfig(command,'alarmrelay3')
		elif self.cam == 8:
			bellconfig(command,'alarmrelay4')
			
		
	def on__idle(self, event):
		self.close()
		
	def on_close(self, ex):
		keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				['Bel01','Bel02','Bel03','Bel04',],
				['Kamera01','Kamera02','Kamera03','Kamera04'],['Panduan']]			
		replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
		self.sender.sendMessage('[Panduan] untuk informasi lebih lanjut',reply_markup = replyKeyboardMakeup)
		print('Timeout Excedded')
				
class ChatBox(telepot.DelegatorBot):
	global config
	global config1
	def __init__(self,token):
		self.adminconfig()
		self.timeconfig()
		super(ChatBox, self).__init__(token, [
			pave_event_space()(per_chat_id(), create_open, SmartRoomChat, timeout=60),
				])
	def adminconfig(self):
		try:
			config1.read(open('telebot.ini'))
		except:
			try:
				config1.add_section('admin')
				config1.set('admin','chatid','000000000')
				config1.set('admin','password','000000000')
				with open('telebot.ini', 'w') as fp:
					config1.write(fp)
			except:
				print('[info] failed')
			else:
				chatid = config1.get('admin','chatid')
				print(chatid)
		else:
			print('[info] reading success (admin)')
			config1.read('telebot.ini')
			chatid = config1.get('admin','chatid')
			print(chatid)
	def timeconfig(self):
		try:
			config.read(open('SMADHARMAPUTRA.ini'))
		except:
			try:
				config.add_section('alarmcam1')
				config.add_section('alarmcam2')
				config.add_section('alarmcam3')
				config.add_section('alarmcam4')
				config.add_section('alarmrelay1')
				config.add_section('alarmrelay2')
				config.add_section('alarmrelay3')
				config.add_section('alarmrelay4')
				config.add_section('status')
				config.set('status','status','0')
				config.set('alarmcam1','hour','00:00:00')
				config.set('alarmcam2','hour','00:00:00')
				config.set('alarmcam3','hour','00:00:00')
				config.set('alarmcam4','hour','00:00:00')
				config.set('alarmrelay1','time_on','00:00:00')
				config.set('alarmrelay2','time_on','00:00:00')
				config.set('alarmrelay3','time_on','00:00:00')
				config.set('alarmrelay4','time_on','00:00:00')
				config.set('alarmcam1','durasi','00:00:00')
				config.set('alarmcam2','durasi','00:00:00')
				config.set('alarmcam3','durasi','00:00:00')
				config.set('alarmcam4','durasi','00:00:00')
				config.set('alarmrelay1','time_off','00:00:00')
				config.set('alarmrelay2','time_off','00:00:00')
				config.set('alarmrelay3','time_off','00:00:00')
				config.set('alarmrelay4','time_off','00:00:00')
				with open('SMADHARMAPUTRA.ini','w') as configfile:
					config.write(configfile)
					#config.readfp(configfile)
				print('Membuat Konfigurasi....')
			except:
				print('cannot Create File')
		else:
			print('[info] reading success (time)')
			
				
TOKEN = '333574709:AAH6JLNwXwYgExVxfFQ0rSGfBd-Ofq4eI4U'

bot = ChatBox(TOKEN)
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)