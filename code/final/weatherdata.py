import requests
import config

#Gets wind direction at specified coordinates
class WeatherData:
    def __init__(self,lat,lon):

        #API key
        self.key = config.api_key

        #
        self.lat = lat
        self.lon = lon

        self.url = "https://api.darksky.net/forecast/{}/{},{}?exclude=minutely,hourly,daily,alerts,flags&units=si".format(self.key,self.lat,self.lon)
        self.weather = requests.get(self.url)

    def getWindDirection(self,lat,lon):

        self.lat = lat
        self.lon = lon

        #url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(self.lat,self.lon,self.key)
        #weather = requests.get(url)

        #print("Wind dir = ", weather.json()["wind"]["deg"])
        return self.weather.json()["currently"]["windBearing"]

    def getWindSpeed(self,lat,lon):
        self.lat = lat
        self.lon = lon

        #url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(self.lat,self.lon,self.key)
        #weather = requests.get(url)

        #print("WindSp =",weather.json()["wind"]["speed"])
        return self.weather.json()["currently"]["windSpeed"]


#Testing
'''
weather = WeatherData(57.1497,2.0943)
print(weather.getWindDirection(57.1497,-2.0943))
print(weather.getWindSpeed(57.1497,-2.0943))
'''
