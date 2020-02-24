import requests
import config

#Gets wind direction at specified coordinates
class WeatherData:
    def __init__(self):

        #API key
        self.key = config.api_key

    def getWindDirection(self,lat,lon):

        self.lat = lat
        self.lon = lon

        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(self.lat,self.lon,self.key)
        weather = requests.get(url)

        #print("Wind dir = ", weather.json()["wind"]["deg"])
        return weather.json()["wind"]["deg"]

    def getWindSpeed(self,lat,lon):
        self.lat = lat
        self.lon = lon

        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(self.lat,self.lon,self.key)
        weather = requests.get(url)

        #print("WindSp =",weather.json()["wind"]["speed"])
        return weather.json()["wind"]["speed"]


#Testing
'''
weather = WeatherData()
print(weather.getWindDirection(57.1497,-2.0943))
print(weather.getWindSpeed(57.1497,-2.0943))
'''
