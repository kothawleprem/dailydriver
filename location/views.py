from django.shortcuts import render
from geopy.geocoders import Nominatim
from .utils import get_geo
from requests import get
from ipstack import GeoLookup
import requests
import json




def for_location(request):
    geolocator = Nominatim(user_agent="location")

    geo_lookup = GeoLookup("582179b24ab7f5f07d71c6fb0be3fc7c")
    ulocation = geo_lookup.get_own_location()
    city = ulocation["city"]
    zip = ulocation["zip"]
    ip = ulocation["ip"]
    print(ulocation)
    #ip = '192.168.0.105'
    #ip = get('https://api.ipify.org').text
    #print('My public IP address is: {}'.format(ip))
    #ip = ("",publicip.get(),"")
    #ip = get('http://ip.42.pl/raw').text
    
    # country,city,lat,lon = get_geo(ip)
   
    # print('location country',country)
    # print('location city',city)

    # ulocation = geolocator.geocode(city)
    # print('###',ulocation)
    # alocation = request.remote_addr
    context = {
        'city' : city,
        'zip' : zip,
        'ip' :ip,
        #'ulocation' : ulocation,
    #   'alocation' : alocation,
    }
    return render(request, 'location/main.html',context)
# Create your views here.
