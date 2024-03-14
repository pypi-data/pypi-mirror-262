#import requests, pprint
import requests

# url = "https://api.openweathermap.org/data/2.5/forecast?lat=40&lon=70&appid=fe36175ac9d40f540a6d015267c6359d"
# r = requests.get(url)
# print(r.text)
# print(type(r.text))
# print(r.json())

class Weather:
    """Creates a weather object getting an apikey as input
    and either a city name or lat and lon coordinates.

    Package use example:
    # Create a weather object using a city name:
    # The api key below is not guarantees to work.
    # Get your own apikey from https://openweathermap.org
    # and wait a couple of hours for the apikey to be activated
    >>> weather1 = Weather(apikey = "fe36175ac9d40f540a6d015267c6359d", city = "Madrid")

    # Using latitude and longitude coordinates
    >>> weather2 = Weather(apikey = "fe36175ac9d40f540a6d015267c6359d", lat = 41.1, lon=-4.1)

    #Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    #Simplified data for the next 12 hours:
    >>> weather1.next_12h_simplified()
    """

    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={apikey}&units=metri"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            #url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units=imperial"
            #url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units=standard"
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units=metri"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city or lat and lon arguments")

        if self.data["cod"] != "200":
            return ValueError(self.data["message"])


    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict
        """
        # print(self.data)
        return self.data['list'][:4]  # up to that fourth item of that's a list

    def next_12h_simplified(self):
        """Returns date, temperature, and sky condition every 3 hours
           for the next 12 hours as a tuple of tuples.
        """
        simple_data = []
        for dicty in self.data['list'][:4]:
            # print(dicty)
            #print(dicty['dt_txt'],dicty['main']['temp'],dicty['weather'][0]['description'])   # get only first item of the list
            #celcius = round(dicty['main']['temp']-273, 2)
            #simple_data.append((dicty['dt_txt'],celcius,dicty['weather'][0]['description']))   # get only first item of the list
            simple_data.append((dicty['dt_txt'],round(dicty['main']['temp']-273, 2),dicty['weather'][0]['description']))   # get only first item of the list
             # return(self.data['list'][0]['dt_txt'],
            #        self.data['list'][0]['main']['temp'],
            #        self.data['list'][0]['weather'][0]['description'])   # get only first item of the list
        return simple_data

# weather1 = Weather(apikey= "fe36175ac9d40f540a6d015267c6359d", city="Santiago")
# weather2 = Weather(apikey= "fe36175ac9d40f540a6d015267c6359d", lat=4.1, lon = 4.5)
#
# print("Parte 1 ...............")
# # print(weather1.data)
# print(weather1.next_12h())
#
# print("Parte 2 ...............")
# print(weather2.data)
# print(weather2.next_12h())


#print(weather.next_12h())
#pprint.pprint(weather.data['list'][:1])
#pprint.pprint(weather.next_12h())

"""Remove this code - you might also want to remove the pprint, we don't need it now,
 and also check to remove every possible print function that we were using here for troubleshooting things.
weather = Weather(apikey= "fe36175ac9d40f540a6d015267c6359d", city="Calgary", lat=4.1, lon=4.5)
pprint.pprint(weather.next_12h_simplified())
"""
