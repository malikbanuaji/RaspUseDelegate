import telepot
import numpy as np
import datetime
import os
import subprocess as sp
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id,per_chat_id_except, per_chat_id_in, create_open, pave_event_space, include_callback_query_chat_id
import time
import configparser
from socket import timeout
from urllib.request import urlopen, URLError

#------------------------------#
from sdpcam import waktu
#import sdpcamserver
#------------------------------#

config = configparser.SafeConfigParser()
config1 = configparser.SafeConfigParser()
x = waktu()

class NonAdmin(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(NonAdmin, self).__init__(*args, **kwargs)
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		command = msg['text']
		

		if content_type == 'text':
			self.sender.sendMessage('Tolong Masukan Password')
		config = configparser.SafeConfigParser()
		config.read('telebot.ini')
		check = config.get('admin','chatid')
		if check == '000000000':
			if command == '000000000':
				config.set('admin','chatid',str(chat_id))
				config.set('admin','password',str(chat_id))
				with open('telebot.ini','w+') as fp:
					config.write(fp)
					fp.close()
				self.sender.sendMessage('Admin ID telah di tetapkan, Restarting BOT')
				sp.call(["sudo","reboot"])
		else:
			return
	def on_idle(self, event):
		self.close
	def on_close(self, ex):
		print('Closing')

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
		
		self.statuskam = 0
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		command = msg['text']
		print ('Got command: %s \r' % command)
		print (chat_id)
		
		def papanmenu():
			keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				#['Bel01','Bel02','Bel03','Bel04',],
				['Alarm 1','Alarm 2','Alarm 3','Alarm 4'],['Panduan','Status']]			
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': True, 'one_time_keyboard': True}
			self.sender.sendMessage('[Panduan] untuk informasi lebih lanjut',reply_markup = replyKeyboardMakeup)
		
		
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
			
			self._torl = [['Bertahap'],['Langsung'],a0]
			self._torlkey = {'keyboard': self._torl, 'resize_keyboard': True, 'one_time_keyboard': True}

			
			
			if jam == 'BATAL':
				self.close()
				#papanmenu()
				#self.statuskam = 4
				#self.mn = True
				#self.cam = 0
				#menuutama(command)

			elif jam == 'Bertahap':
				self.statuskam = 1
			elif jam == 'Langsung':
				self.statuskam = 5
			
			if self.statuskam == 0:
				self.sender.sendMessage('Bertahap - Pemilihan bertahap mulai dari\nJam -- Menit -- Durasi\n\nLangsung - Mengirim pesan dengan format Jam Menit dan Durasi sesuai dengan contoh',reply_markup=self._torlkey)
				
			if self.statuskam == 1:
				self.sender.sendMessage('Pada Jam Berapa?', reply_markup = replyKeyboardMakeup)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 2:
				self.konfigjam = jam
				self.sender.sendMessage('Pada Menit Berapa ??', reply_markup = replyKeyboardMakeup1)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 3:
				self.konfigmenit = jam
				self.sender.sendMessage('Berapa Lama', reply_markup = replyKeyboardMakeup2)
				self.statuskam = self.statuskam + 1
				
			elif self.statuskam == 4:
				self.konfigdurasi = jam
				self.hasil = self.konfigjam+':'+self.konfigmenit
				config.read('SMADHARMAPUTRA.ini')
				config.set(alarm,'hour',self.hasil+':00')
				config.set(alarm,'durasi','00:'+self.konfigdurasi+':00')
				with open('SMADHARMAPUTRA.ini','w+') as configfile:
					config.write(configfile)
					configfile.close()
				testjam = config.get(alarm,'hour')
				testdurasi = config.get(alarm,'durasi')
				self.sender.sendMessage(alarm+' telah disetel setiap pukul '+testjam+' selama '+testdurasi+' Menit')
				x.loadConfig()
				self.close()
			
			elif self.statuskam == 5:
				self.sender.sendMessage('Mohon berikan jam menit dan durasi seperti contoh format berikut\n\n*1200 05*\n\n*12* - Jam(00-23)\n*00* - Menit(00-59)\n*05* - Durasi(00-60)\n\nKetik BATAL untuk membatalkan',reply_markup=ReplyKeyboardRemove(),parse_mode='Markdown')
				self.statuskam += 1
				
			elif self.statuskam == 6:
				ljam = []
				lmenit = []
				ldurasi = []
				for i in range(24):
					if len(str(i)) < 2:
						ljam.append('0%s' %i)
					else:
						ljam.append('%s' %i)
				for i in range(60):
					if len(str(i)) < 2:
						lmenit.append('0%s' %i)
					else:
						lmenit.append('%s' %i)
				for i in range(5,60):
					if len(str(i)) < 2:
						ldurasi.append('0%s' %i)
					else:
						ldurasi.append('%s' %i)
				if jam[0:2] in ljam and jam[2:4] in lmenit and jam[5:7] in ldurasi:
					#self.sender.sendMessage('yoi')
					self.hasil = jam[0:2]+':'+jam[2:4]
					config.read('SMADHARMAPUTRA.ini')
					config.set(alarm,'hour',self.hasil+':00')
					config.set(alarm,'durasi','00:'+jam[5:7]+':00')
					with open('SMADHARMAPUTRA.ini','w+') as configfile:
						config.write(configfile)
						configfile.close()
					testjam = config.get(alarm,'hour')
					testdurasi = config.get(alarm,'durasi')
					self.sender.sendMessage(alarm+' telah disetel setiap pukul '+testjam+' selama '+testdurasi+' Menit')
					self.close()
				else:
					self.sender.sendMessage('Mohon Masukan dengan format yang sesuai')				
		
		
		def menuutama(commands):
			if commands == 'AMBIL GAMBAR':
				filenameimg = datetime.datetime.now().strftime('%Y%m%d-%H%M%S.jpg')
				filenameimg_path = os.path.join(os.path.abspath('Pictures'), filenameimg)
				x.startCaptureCam(filenameimg)
				self.sender.sendChatAction('upload_photo')
				try:
					self.sender.sendPhoto(open(filenameimg_path,'rb'),caption= filenameimg)
				except:
					self.sender.sendMessage('Terjadi kesalahan silahkan ulang beberapa saat lagi')
			elif commands == 'AMBIL VIDEO':
				filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
				filenamevid_path = os.path.join(os.path.abspath('Videos'), filenamevid)
				x.startRecordCam(filenamevid)
				self.sender.sendChatAction('upload_video')
				try:
					self.sender.sendVideo(open(filenamevid_path, 'rb'),caption = filenamevid)
				except:
					self.sender.sendMessage('Terjadi kesalahan silahkan ulang beberapa saat lagi')
				
			elif commands == 'Panduan':
				self.sender.sendMessage("*AMBIL GAMBAR* - Mengambil gambar pada CCTV \n*AMBIL VIDEO* - Merekam video selama 10 detik \n*Alarm (1-4)* - Mengoperasikan kamera pada waktu dan durasi yang telah ditentukan \n\n/setelpabrik - mengatur ulang Admin ID dan Semua pengatura\n/reset - Mengatur pengaturan seperti awal (ID Admin Tidak Termasuk)\n/video - Merekam Video dengan pilihan durasi\n/backup - Melakukan backup ke Flashdisk(Pengembangan)\n\nSMA Dharma Putra",parse_mode='Markdown')
			elif commands == 'Backup':
				self._backupFile()
			elif commands == 'Status':
				config1.read('telebot.ini')
				config.read('SMADHARMAPUTRA.ini')
				pwd = config1.get('admin','password')
				kam1 = config.get('alarmcam1','hour')
				kam2 = config.get('alarmcam2','hour')
				kam3 = config.get('alarmcam3','hour')
				kam4 = config.get('alarmcam4','hour')
				dkam1 = config.get('alarmcam1','durasi')
				dkam2 = config.get('alarmcam2','durasi')
				dkam3 = config.get('alarmcam3','durasi')
				dkam4 = config.get('alarmcam4','durasi')
				stat = config.get('status','status')
				s = ''
				ssid = sp.check_output(["iwgetid","-r"])
				ssidstr = ssid.decode("utf-8")
				disk = os.statvfs('/')
				total_space = (disk.f_frsize * disk.f_blocks) / 1000000
				free_space = (disk.f_frsize * disk.f_bfree) / 1000000
				total_space_str = str(int(total_space))
				free_space_str = str(int(free_space))
				if stat == '0':
					s = 'Tidak Aktif'
					keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
				elif stat == '1':
					s = 'Aktif'
					keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
				chatkam = self.sender.sendMessage('SSID          : %sPassword : %s(admin)\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s\n\nSisa Penyimpanan :  %s/%s MB' %(ssidstr, pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s,free_space_str,total_space_str),reply_markup=keyboard)
				self._alarm = telepot.helper.Editor(self.bot, chatkam)

			elif commands == 'Alarm 1':
				self.cam = 1
			elif commands == 'Alarm 2':
				self.cam = 2
			elif commands == 'Alarm 3':
				self.cam = 3
			elif commands == 'Alarm 4':
				self.cam = 4
		
		if command == '/start':
			papanmenu()
		elif command == '/setelpabrik':
			self._delete_confirmation()
		elif command == '/reset':
			self._reset_confirmation()
		elif command == '/video':
			self._video()
		elif command == '/flashdisk':
			self._checkFlashDrive()
		elif command == '/backup':
			self._backupFile()
		elif command == '/hide':
			self.sender.sendMessage('removing',reply_markup=ReplyKeyboardRemove())
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
	def _checkFlashDrive(self):
		fd = sp.check_output(['ls','/media/pi']).strip().decode('utf-8')
		if fd == '':
			self.sender.sendMessage('Flashdisk Tidak Temukan')
		else:
			self.sender.sendMessage('Flashdisk ditemukan dengan nama %s' % fd)
	def _backupFile(self):
		pickey = InlineKeyboardMarkup(inline_keyboard=[[
					InlineKeyboardButton(text='Ya', callback_data='backy'),
					InlineKeyboardButton(text='Tidak', callback_data='backn'),]])
		sent = self.sender.sendMessage('Apakah anda yakin ingin melakukan Backup?', reply_markup=pickey)
		self._backup_file = telepot.helper.Editor(self.bot, sent)
		
	def _video(self):
		pickey = InlineKeyboardMarkup(inline_keyboard=[[
					InlineKeyboardButton(text='10 Detik', callback_data='10'),
					InlineKeyboardButton(text='15 Detik', callback_data='15'),
					InlineKeyboardButton(text='20 Detik', callback_data='20')],[
					InlineKeyboardButton(text='Batal', callback_data='vidbatal')],])
		sent = self.sender.sendMessage('Pilih durasi', reply_markup=pickey)
		self._vid = telepot.helper.Editor(self.bot, sent)

	def _delete_confirmation(self):
		keyboard = InlineKeyboardMarkup(inline_keyboard=[[
			InlineKeyboardButton(text='Ya', callback_data='delyes'),
			InlineKeyboardButton(text='Tidak', callback_data='delno'),]])
		sent = self.sender.sendMessage('Apakah Anda Yakin Ingin Setel Ulang Pabrik ?\nAdmin ID akan tereset', reply_markup=keyboard)
		self._editor = telepot.helper.Editor(self.bot, sent)
	def _reset_confirmation(self):
		keyboard = InlineKeyboardMarkup(inline_keyboard=[[
			InlineKeyboardButton(text='Ya', callback_data='resyes'),
			InlineKeyboardButton(text='Tidak', callback_data='resno'),]])
		sent = self.sender.sendMessage('Apakah anda yakin ingin melakukan reset?\nSeluruh pengaturan Alarm akan dibuat seperti semula(kecuali Admin ID)', reply_markup=keyboard)
		self._reset = telepot.helper.Editor(self.bot, sent)
	def on_callback_query(self,msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		
		if query_data == 'delyes':
			config1.read('telebot.ini')
			config1.set('admin','chatid','000000000')
			config1.set('admin','password','000000000')
			with open('telebot.ini','w+') as fp:
				config1.write(fp)
				fp.close()
			if self._editor:
				self._editor.editMessageText('Setel pabrik sukses, anda bukan admin\n\nMohon tunggu sistem sedang mengatur ulang')
				self._editor = None
			sp.call(["sudo","reboot"])
		elif query_data == 'delno':
			if self._editor:
				self._editor.editMessageText('Dibatalkan')
				self._editor = None
		elif query_data == 'backy':
			fd = sp.check_output(['ls','/media/pi']).strip().decode('utf-8')
			if not os.path.exists('/media/pi/%s/SMABACKUP' %fd):
				os.makedirs('/media/pi/%s/SMABACKUP'%fd)
			if self._backup_file:
				if fd == '':
					self._backup_file.editMessageText('Flashdisk Tidak Temukan, gagal melakukan Backup')
					self._backup_file = None
				else:
					self._backup_file.editMessageText('Flashdisk ditemukan dengan nama %s,\nMelakukan Backup....' % fd)
					sp.call(['cp','-r','Videos','/media/pi/%s/SMABACKUP/'%fd])
					sp.call(['cp','-r','Pictures','/media/pi/%s/SMABACKUP'%fd])
					sp.call(['umount','/media/pi/%s/'%fd])
					self._backup_file.editMessageText('Backup Selesai dengan nama Folder SMABACKUP\nFlashdisk dapat dilepas secara aman')
				self._backup_file = None
		elif query_data == 'backn':
			if self._backup_file:
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[
						InlineKeyboardButton(text='Ya', callback_data='ejecty'),
						InlineKeyboardButton(text='Tidak', callback_data='ejectn'),]])
				self._backup_file.editMessageText('Backup dibatalkan, apakah ingin melepas FlashDisk?',reply_markup=keyboard)
		elif query_data == 'ejecty':
			if self._backup_file:
				self._backup_file.editMessageText('Flashdisk sudah aman untuk dilepas/diambil')
				self._backup_file = None
		elif query_data == 'ejectn':
			if self._backup_file:
				self._backup_file.editMessageText('Batal, Flashdisk tidak aman untuk dilepas/ambil\n\nUntuk melepas Flashdisk dapat mengirimkan pesan /eject')
				self._backup_file = None
		elif query_data == 'resyes':
			config.read('SMADHARMAPUTRA.ini')
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
			with open('SMADHARMAPUTRA.ini','w+') as fp:
				config.write(fp)
				fp.close()
			if self._reset:
				self._reset.editMessageText('Pengaturan ulang sukses')
				self._reset = None
		elif query_data == 'resno':
			if self._reset:
				self._reset.editMessageText('Dibatalkan')
				self._reset = None		

		elif query_data == 'alyes':
			x.enableAlarm()
			x.loadConfig()
			config1.read('telebot.ini')
			config.read('SMADHARMAPUTRA.ini')
			pwd = config1.get('admin','password')
			kam1 = config.get('alarmcam1','hour')
			kam2 = config.get('alarmcam2','hour')
			kam3 = config.get('alarmcam3','hour')
			kam4 = config.get('alarmcam4','hour')
			dkam1 = config.get('alarmcam1','durasi')
			dkam2 = config.get('alarmcam2','durasi')
			dkam3 = config.get('alarmcam3','durasi')
			dkam4 = config.get('alarmcam4','durasi')
			stat = config.get('status','status')
			s = ''
			ssid = sp.check_output(["iwgetid","-r"])
			ssidstr = ssid.decode("utf-8")
			disk = os.statvfs('/')
			total_space = (disk.f_frsize * disk.f_blocks) / 1000000
			free_space = (disk.f_frsize * disk.f_bfree) / 1000000
			total_space_str = str(int(total_space))
			free_space_str = str(int(free_space))

			if stat == '0':
				s = 'Tidak Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
			elif stat == '1':
				s = 'Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
			if self._alarm:
				self._alarm.editMessageText('SSID          : %sPassword : %s(admin)\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s\n\nSisa Penyimpanan :  %s/%s MB' %(ssidstr, pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s,free_space_str,total_space_str),reply_markup=keyboard)
		elif query_data == 'alno':
			x.disableAlarm()
			x.loadConfig()
			config1.read('telebot.ini')
			config.read('SMADHARMAPUTRA.ini')
			pwd = config1.get('admin','password')
			kam1 = config.get('alarmcam1','hour')
			kam2 = config.get('alarmcam2','hour')
			kam3 = config.get('alarmcam3','hour')
			kam4 = config.get('alarmcam4','hour')
			dkam1 = config.get('alarmcam1','durasi')
			dkam2 = config.get('alarmcam2','durasi')
			dkam3 = config.get('alarmcam3','durasi')
			dkam4 = config.get('alarmcam4','durasi')
			stat = config.get('status','status')
			s = ''
			ssid = sp.check_output(["iwgetid","-r"])
			ssidstr = ssid.decode("utf-8")
			disk = os.statvfs('/')
			total_space = (disk.f_frsize * disk.f_blocks) / 1000000
			free_space = (disk.f_frsize * disk.f_bfree) / 1000000
			total_space_str = str(int(total_space))
			free_space_str = str(int(free_space))

			if stat == '0':
				s = 'Tidak Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
			elif stat == '1':
				s = 'Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
			if self._alarm:
				self._alarm.editMessageText('SSID          : %sPassword : %s(admin)\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s\n\nSisa Penyimpanan :  %s/%s MB' %(ssidstr, pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s,free_space_str,total_space_str),reply_markup=keyboard)
		elif query_data == '10':
			filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
			filenamevid_path = os.path.join(os.path.abspath('Videos'), filenamevid)
			if self._vid:
				self._vid.editMessageText('Merekam 10 detik, Mohon Tunggu')
				x.startRecordCam(filenamevid,'00:00:10')
				self._vid.deleteMessage()
				self._vid = None
			self.sender.sendChatAction('upload_video')
			with open(filenamevid_path,'rb') as v:
				self.sender.sendVideo(v)
				v.close()
			
		elif query_data == '15':
			filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
			filenamevid_path = os.path.join(os.path.abspath('Videos'), filenamevid)
			if self._vid:
				self._vid.editMessageText('Merekam 15 detik, Mohon Tunggu')
				x.startRecordCam(filenamevid,'00:00:15')
				self._vid.deleteMessage()
				self._vid = None
			self.sender.sendChatAction('upload_video')
			with open(filenamevid_path,'rb') as v:
				self.sender.sendVideo(v)
				v.close()
			
		elif query_data == '20':
			filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
			filenamevid_path = os.path.join(os.path.abspath('Videos'), filenamevid)
			if self._vid:
				self._vid.editMessageText('Merekam 20 detik, Mohon Tunggu')
				x.startRecordCam(filenamevid,'00:00:20')
				self._vid.deleteMessage()
				self._vid = None
			self.sender.sendChatAction('upload_video')
			with open(filenamevid_path,'rb') as v:
				self.sender.sendVideo(v)
				v.close()
		elif query_data == 'vidbatal':
			if self._vid:
				self._vid.editMessageText('Operasi dibatalkan')
				self._vid = None
	
	def on__idle(self, event):
		self.close()
		
	def on_close(self, ex):
		keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				['Alarm 1','Alarm 2','Alarm 3','Alarm 4'],['Panduan','Status']]			
		replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': True, 'one_time_keyboard': True}
		self.sender.sendMessage('[Panduan] untuk informasi lebih lanjut',reply_markup = replyKeyboardMakeup)
		print('Timeout Excedded')
				
class ChatBox(telepot.DelegatorBot):
	global config
	global config1
	global x
	def __init__(self,token):
		self.adminconfig()
		self.timeconfig()
		x.loadConfig()
		config1.read('telebot.ini')
		idadmin = config1.get('admin','chatid')
		x.camStart()
		super(ChatBox, self).__init__(token, [
			include_callback_query_chat_id(pave_event_space())(per_chat_id_in([int(idadmin)],types='private'), create_open, SmartRoomChat, timeout=90),
			pave_event_space()(per_chat_id_except([int(idadmin)],types='private'), create_open, NonAdmin, timeout=10),
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
					fp.close()
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
					configfile.close()
					#config.readfp(configfile)
				print('Membuat Konfigurasi....')
			except:
				print('cannot Create File')
		else:
			print('[info] reading success (time)')
			

def check_connectivity(reference):
    try:
        urlopen(reference, timeout=1)
        return True
    except URLError:
        return False


def wait_for_internet():
    while not check_connectivity("https://api.telegram.org"):
        print("Waiting for internet")
        time.sleep(1)

def path():
	filepath = ['Videos','Pictures']
	for i in filepath:
		if not os.path.exists(os.path.abspath(i)):
			os.makedirs(os.path.abspath(i))
		else:
			print('[info] Load %s' % i)
	
def main():
	try:
		wait_for_internet()
	except:
		print("[INFO] no internet connection")
		return main()
	else:
		try:
			config1.read('telebot.ini')
			chatid = config1.get('admin','chatid')
			TOKEN = '501033727:AAGTkZY5pCHy0iXdpCp7yzWf-BzaENGUoqM'
			box = telepot.Bot(TOKEN)
			bot = ChatBox(TOKEN)
			MessageLoop(bot).run_as_thread()
			print('Listening ...')

			while 1:
				box.sendMessage(int(chatid), text = 'SMA Dharma Putra')
				time.sleep(1800)
		except KeyboardInterrupt:
			x.stop()
			exit(0)
if __name__ == "__main__":
	path()
	main()

