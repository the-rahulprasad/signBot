import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import smtplib
import urllib.request
import os
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def wikiResult(query):
	query = query.replace('wikipedia','')
	query = query.replace('search','')
	if len(query.split())==0: query = "wikipedia"
	try:
		return wikipedia.summary(query, sentences=2)
	except Exception as e:
		return "Desired Result Not Found"

class WEATHER:
	def __init__(self):
		#Currently in Lucknow, its 26 with Haze
		self.tempValue = ''
		self.city = ''
		self.currCondition = ''
		self.speakResult = ''

	def updateWeather(self):
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		#URL = 'https://weather.com/en-IN/weather/today/l/'+data['loc']
		URL = 'https://weather.com/en-IN/weather/today/'
		result = requests.get(URL)
		src = result.content

		soup = BeautifulSoup(src, 'html.parser')

		city = ""
		for h in soup.find_all('h1'):
			cty = h.text
			cty = cty.replace('Weather','')
			self.city = cty[:cty.find(',')]
			break

		spans = soup.find_all('span')
		for span in spans:
			try:
				if span['data-testid']=="TemperatureValue":
					self.tempValue = span.text[:-1]
					break
			except Exception as e:
				pass

		divs = soup.find_all('div', class_='CurrentConditions--phraseValue--2xXSr')
		for div in divs:
			self.currCondition = div.text
			break

	def weather(self):
		from datetime import datetime
		today = datetime.today().strftime('%A')
		self.speakResult = "Currently in " + self.city + ", its " + self.tempValue + " degree, with a " + self.currCondition 
		return [self.tempValue, self.currCondition, today, self.city, self.speakResult]

w = WEATHER()

def dataUpdate():
	w.updateWeather()

##### WEATHER #####
def weather():
	w.updateWeather()
	return w.weather()



def latestNews(news=5):
	URL = 'https://indianexpress.com/latest-news/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	headlineLinks = []
	headlines = []

	divs = soup.find_all('div', {'class':'title'})

	count=0
	for div in divs:
		count += 1
		if count>news:
			break
		a_tag = div.find('a')
		headlineLinks.append(a_tag.attrs['href'])
		headlines.append(a_tag.text)

	return headlines,headlineLinks

def maps(text):
	text = text.replace('maps', '')
	text = text.replace('map', '')
	text = text.replace('google', '')
	openWebsite('https://www.google.com/maps/place/'+text)

def giveDirections(startingPoint, destinationPoint):

	geolocator = Nominatim(user_agent='assistant')
	if 'current' in startingPoint:
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		startinglocation = geolocator.reverse(data['loc'])
	else:
		startinglocation = geolocator.geocode(startingPoint)

	destinationlocation = geolocator.geocode(destinationPoint)
	startingPoint = startinglocation.address.replace(' ', '+')
	destinationPoint = destinationlocation.address.replace(' ', '+')

	openWebsite('https://www.google.co.in/maps/dir/'+startingPoint+'/'+destinationPoint+'/')

	startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
	destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
	total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km #.mile
	return str(round(total_distance, 2)) + 'KM'

def openWebsite(url='https://www.google.com/'):
	webbrowser.open(url)



def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."



def downloadImage(query, n=4):
	print(query)
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	query = query.replace('who', '')
	query = query.replace('is', '')
	query = query.replace(' ', '')
	URL = "https://www.google.com/search?q=" + query + "&tbm=isch"
	print(URL)
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')
	imgTags = soup.find_all('img')

	if os.path.exists('Downloads')==False:
		os.mkdir('Downloads')

	count=0
	for i in imgTags:
		if count==n: break
		try:
			image_url = i['src']
			if '.gif' in image_url:
				continue
			else:
				urllib.request.urlretrieve(image_url, 'Downloads/' + str(count) + '.jpg')
				count += 1
				print('Downloaded', count)
		except Exception as e:
			raise e
