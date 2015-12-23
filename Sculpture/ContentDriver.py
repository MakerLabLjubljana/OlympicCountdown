from datetime import datetime, timedelta
import time
from rgbmatrix import RGBMatrix
from rgbmatrix import graphics
from threading import Thread
from twython import Twython
import requests
import os
TWITTER_APP_KEY = 'JFDLlCc8bdiS5RKExbOPI2lwb' #supply the appropriate value
TWITTER_APP_KEY_SECRET = 'WkkONPuUDArF9dIpjEC9i8ybRUJvqZ0WgE9UMVB0bR5tUWZ5QJ' 
TWITTER_ACCESS_TOKEN = '350180030-0Nq9UwhufGajuaVDPnosH6gyON81hme1VurYw3rd'
TWITTER_ACCESS_TOKEN_SECRET = 'qIkeMpeRVVa1i9kxPZkraroKLoyQtwYcUqQIGJFR482Aw'

# SETTINGS START ###############################################################################################
rows = 32                                                                                                         
chain = 12
parallel = 1
pwmbits = 3
brightness = 100
luminance = True
font_file = "/home/pi/Digital-7.bdf"
font_file_twitter = "/home/pi/twiter.bdf"
color_codeR = 255
color_codeG = 0
color_codeB = 0

OI = datetime(2016, 8, 5, 0, 0, 0) #cas zacetka olimpijskih iger yyyy, mm, dd, HH, MM, SS
dni = "DNI"
ur ="UR"
koordinate_ure  = [130,145,   160,   165,180,   195,   200,215]  #koordinate za  HH ":" MM ":" SS   
TWEET = "Cakam na tweet"
web_url = "http://maker.si/odstevalnik"
# SETTINGS STOP ################################################################################################

def thread():
    while True:
#	time.sleep(60)
	global TWEET
#	res = os.popen('vcgencmd measure_temp').readline()
#	temp=(res.replace("temp=","").replace("'C\n",""))
	
#	payload = {"presence" : "www" }#(datetime.now().strftime("%Y-%m-%d %H:%M:%S : ")+temp)}

#	requests.post(web_url, data=payload)
#	print  requests.get(web_url).text

#	requests.post(web_url, data=payload)
	print  requests.get(web_url).text

	twitter = Twython(app_key=TWITTER_APP_KEY,
                        app_secret=TWITTER_APP_KEY_SECRET,
                        oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

	try:
		search_results = twitter.search(q='#odstevalnik', count=5)
	
	except TwythonError as e:
		TWEET = "Cakam na tweet"
	TWEET = ""
	for tweet in reversed(search_results['statuses']):
#			print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at'])
		TWEET +=  tweet['text'].encode('utf-8') + "           "

	time.sleep(120)		


class Matrix():
	def __init__(self):
		matrix = RGBMatrix(rows, chain, parallel)
		matrix.pwmBits = pwmbits
		matrix.brightness = brightness
		matrix.luminanceCorrect = luminance
		self.canvas = matrix
		self.font = graphics.Font()
		self.font.LoadFont(font_file)
		self.font_twitter = graphics.Font()
		self.font_twitter.LoadFont(font_file_twitter)
		self.color = graphics.Color(color_codeR, color_codeG, color_codeB)
		self.pos = self.canvas.width
		#self.tweet = "Cakam na tweet :D"
		#self.Twitter()
		self.offscreenCanvas = self.canvas.CreateFrameCanvas()
		
	def Run(self):
		#previous_time = datetime.now().second
		while True:
			self.elapsed_time()
		#	now_time = datetime.now().second
		#	if now_time != previous_time:
			self.matrix_show()
		#		previous_time = now_time
			time.sleep(0.05)

	def elapsed_time(self):
		sedaj = datetime.now()
		razlika = OI - sedaj
		if razlika.seconds == 0: return 0
		dni = razlika.days+1
		if dni < 10 : dni=' '+' '+' '+str(dni)
		elif dni < 100 :dni=' '+' '+str(dni)
		elif dni < 1000 : dni=' '+str(dni)

		ur, remainder = divmod(razlika.seconds, 3600)
		if ur < 10 : ur=" "+str(ur)
	
		minut, sec = divmod(remainder, 60)
		if minut < 10 : minut="0"+str(minut)
		if sec < 10 : sec="0"+str(sec)
		self.days = str(dni)
		self.show=str(ur)+":"+str(minut)+":"+str(sec) #tisto kar mora prikazati
		
	
	def matrix_show(self):
		global TWEET
		self.offscreenCanvas.Clear()
		lenght = graphics.DrawText(self.offscreenCanvas, self.font_twitter, self.pos, 20, self.color, TWEET)
		self.pos -= 1
		if (self.pos + lenght < 255):
			self.pos = self.offscreenCanvas.width

		for x in range (0,256):
			for y in range (0,32):
				self.offscreenCanvas.SetPixel(x,y,0,0,0)		

		for x in range (0,len(ur)):
			graphics.DrawText(self.offscreenCanvas, self.font, 232+(10*x),28 , self.color, ur[x])

		for x in range (0,len(dni)):
			graphics.DrawText(self.offscreenCanvas, self.font, 104+(10*x) ,28 , self.color, dni[x])

		for x in range (0,len(self.days)):
			graphics.DrawText(self.offscreenCanvas, self.font, 42+(15*x) ,28 , self.color, self.days[x])

		for x in range (0,len(self.show)):
			graphics.DrawText(self.offscreenCanvas, self.font, koordinate_ure[x],28 , self.color, self.show[x])

		
		self.offscreenCanvas = self.canvas.SwapOnVSync(self.offscreenCanvas)
		

if __name__ == "__main__":
	t = Thread(target=thread, args = [])
	t.daemon = True
	t.start()
	led_panel = Matrix()
	led_panel.Run()


