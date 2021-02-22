from django.shortcuts import render
from geopy.geocoders import Nominatim
from .utils import get_geo
from requests import get


def for_location(request):
    geolocator = Nominatim(user_agent="location")

    #ip = '192.168.0.105'
    ip = get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    
    
    country,city,lat,lon = get_geo(ip)
   
    print('location country',country)
    print('location city',city)

    ulocation = geolocator.geocode(city)
    print('###',ulocation)
    context = {
        'ulocation' : ulocation,
    }
    return render(request, 'location/main.html',context)
# Create your views here.
