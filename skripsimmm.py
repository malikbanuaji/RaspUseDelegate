import telepot
import numpy as np
import datetime
import os
import subprocess as sp
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
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
		print ('Got command: %s \r' % command)
		print (chat_id)
		
		def papanmenu():
			keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				#['Bel01','Bel02','Bel03','Bel04',],
				['Alarm 1','Alarm 2','Alarm 3','Alarm 4'],['Panduan','Status']]			
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
					configfile.close()
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
				self.close()
				#papanmenu()
				#self.statuskam = 4
				#self.mn = True
				#self.cam = 0
				#menuutama(command)
				
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
					configfile.close()
				testjam = config.get(alarm,'hour')
				testdurasi = config.get(alarm,'durasi')
				self.sender.sendMessage(alarm+' telah disetel setiap pukul '+testjam+' selama '+testdurasi+' Menit')
				x.loadConfig()
				self.close()
				
			elif self.statuskam == 4:
				print('Done.')
				
		
		
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
				self.bot.sendMessage(chat_id, text = 'AMBIL GAMBAR - Mengambil gambar pada CCTV \nAMBIL VIDEO - Merekam video selama 10 detik \nAlarm (1-4) - Mengoperasikan kamera pada waktu dan durasi yang telah ditentukan \n/setelpabrik - mengatur ulang Admin ID dan Semua pengatura\n/reset - Mengatur pengaturan seperti awal (ID Admin Tidak Termasuk)\n\nSMA Dharma Putra')

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
				if stat == '0':
					s = 'Tidak Aktif'
					keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
				elif stat == '1':
					s = 'Aktif'
					keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
				chatkam = self.sender.sendMessage('SSID      :%sPassword : %s(admin)\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s' %(ssidstr, pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s),reply_markup=keyboard)
				self._alarm = telepot.helper.Editor(self.bot, chatkam)

			elif commands == 'Alarm 1':
				self.cam = 1
			elif commands == 'Alarm 2':
				self.cam = 2
			elif commands == 'Alarm 3':
				self.cam = 3
			elif commands == 'Alarm 4':
				self.cam = 4
			elif commands == 'Bel01':
				self.cam = 5
			elif commands == 'Bel02':
				self.cam = 6
			elif commands == 'Bel03':
				self.cam = 7
			elif commands == 'Bel04':
				self.cam = 8
		
		if command == '/start':
			papanmenu()
		elif command == '/setelpabrik':
			self._delete_confirmation()
		elif command == '/reset':
			self._reset_confirmation()
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
			if stat == '0':
				s = 'Tidak Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
			elif stat == '1':
				s = 'Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
			if self._alarm:
				self._alarm.editMessageText('Password : %s\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s' %(pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s),reply_markup=keyboard)
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
			if stat == '0':
				s = 'Tidak Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Mulai Alarm', callback_data='alyes')]])
			elif stat == '1':
				s = 'Aktif'
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Matikan Alarm', callback_data='alno')]])
			if self._alarm:
				self._alarm.editMessageText('Password : %s\n------------------\nAlarm 1  : %s Durasi(%s)\nAlarm 2  : %s Durasi(%s)\nAlarm 3  : %s Durasi(%s)\nAlarm 4  : %s Durasi(%s)\nAlarm     : %s' %(pwd, kam1, dkam1, kam2, dkam2, kam3, dkam3, kam4, dkam4, s),reply_markup=keyboard)
	def on__idle(self, event):
		self.close()
		
	def on_close(self, ex):
		keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				['Alarm 1','Alarm 2','Alarm 3','Alarm 4'],['Panduan','Status']]			
		replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
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
			TOKEN = ''
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

