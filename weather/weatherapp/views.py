from django.shortcuts import render
from ipstack import GeoLookup
import requests
# Create your views here.
def home(request):
    geo_lookup = GeoLookup("APIKEY")
    # Replace APIKEY with Our API
    ulocation = geo_lookup.get_own_location()
    city = ulocation["city"]
    zip = ulocation["zip"]
    ip = ulocation["ip"]
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=APIKEY"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    feels_like = int(json_data['main']['feels_like'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    context = {
        'city' : city,
        'zip' : zip,
        'temp' : temp,
        'min_temp' : min_temp,
        'max_temp' : max_temp,
        'feels_like' : feels_like,
        'pressure' : pressure,
        'humidity' : humidity,
    }
   # print(city,zip,ip)
    return render(request,'home.html',context)
