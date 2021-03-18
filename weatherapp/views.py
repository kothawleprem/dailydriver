from django.shortcuts import render
from ipstack import GeoLookup
import requests

from .models import Location
from django.views.decorators.http import require_POST
from . forms import LocationForm
import os

from bs4 import BeautifulSoup
#############################################
# from apiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# import pickle
# import pickle
# import datetime
# import os
# from google_auth_oauthlib.flow import Flow, InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.auth.transport.requests import Request
# import json

##############################################################
# Create your views here.

#############################################################
# news_heading =[]
# news_brief = []
# news_link = []
news_final = []
html_text = requests.get('https://www.ndtv.com/india').text
soup = BeautifulSoup(html_text,'lxml')
articles = soup.find_all('div',class_='news_Itm')
for article in articles:
    try:
        news_initial = []
        content = article.find('div',class_='news_Itm-cont')
        heading = content.find('h2',class_='newsHdng').text
        link = content.find('h2',class_='newsHdng').a['href']
        brief = content.find('p',class_='newsCont').text
        news_initial.append(heading)
        news_initial.append(brief)
        news_initial.append(link)
        news_final.append(news_initial)
        print(f" Heading : {heading}")
        print(f" Link    : {link}")
        print(f" Brief   : {brief}")
        print("")
    except:
        print("")    
#############################################################
def home(request):
    if 'city' in request.GET:
        city = request.GET.get('city')
        api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5bc57ba9bc106c9844915b5178ee10ad"
    else:
        geo_lookup = GeoLookup("582179b24ab7f5f07d71c6fb0be3fc7c")
        ulocation = geo_lookup.get_own_location()
        print(ulocation)
        city = ulocation["city"]
        # zip = ulocation["zip"]
        # ip = ulocation["ip"]
        api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5bc57ba9bc106c9844915b5178ee10ad"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    feels_like = int(json_data['main']['feels_like'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']

 

    # try:
    #     if len(data)>0:
    #         city=data
    # except:
    #         pass
    # print(data)
   
    
   # print(city,zip,ip)
  
    
#     ###################################################################
#     CLIENT_SECRETE_FILE = open('web_client_secret.json')
#     API_NAME = 'calendar'
#     API_VERSION = 'v3'
#     SCOPES = ['https://www.googleapis.com/auth/calendar']
# # # To create a calender
#     def Create_Service(client_secret_file, api_name, api_version, *scopes):
#         print(client_secret_file, api_name, api_version, scopes, sep='-')
#         CLIENT_SECRET_FILE = client_secret_file
#         API_SERVICE_NAME = api_name
#         API_VERSION = api_version
#         SCOPES = [scope for scope in scopes[0]]
#         print(SCOPES)
    
#         cred = None

#         pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
#     # print(pickle_file)
    
#         if os.path.exists(pickle_file):
#             with open(pickle_file, 'rb') as token:
#                 cred = pickle.load(token)

#         if not cred or not cred.valid:
#             if cred and cred.expired and cred.refresh_token:
#                 cred.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
#                 cred = flow.run_local_server()

#             with open(pickle_file, 'wb') as token:
#                 pickle.dump(cred, token)

#         try:
#             service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
#             print(API_SERVICE_NAME, 'service created successfully')
#             return service
#         except Exception as e:
#             print(e)
#             return None


#     def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
#         dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
#         return dt

#     ######################################################################
    


#     service = Create_Service(CLIENT_SECRETE_FILE,API_NAME,API_VERSION,SCOPES)
#     result = service.calendarList().list().execute()
#     calendar_id = result['items'][0]['id']
#     result = service.events().list(calendarId=calendar_id, timeZone="Asia/Kolkata").execute()
    
#     rlen = len(result['items'])
#     ourlist = []
#     for i in range(rlen):
#         mylist = []
#         summary = result['items'][i]['summary']
#         mylist.append(summary)
#         start_time = result['items'][i]['start']
#         mylist.append(start_time)
#         end_time = result['items'][i]['end']
#         mylist.append(end_time)
#         link = result['items'][i]['hangoutLink']
#         mylist.append(link)
#         ourlist.append(mylist)
    
#     print(ourlist)
#     print(imp_s)
#     summary = result['items'][0]['summary']
#     start_time = result['items'][0]['start']
#     end_time = result['items'][0]['end']
#     link = result['items'][0]['hangoutLink']
#     print(summary,start_time,end_time,link)
#     print(imp)
 
    


##################################################################

    context = {
        'city' : city,
        # 'zip' : zip,
        'temp' : temp,
        'min_temp' : min_temp,
        'max_temp' : max_temp,
        'feels_like' : feels_like,
        'pressure' : pressure,
        'humidity' : humidity,
        # 'ourlist' : ourlist,
        # 'news_heading' : news_heading,
        # 'news_brief' : news_brief,
        # 'news_link' : news_link,
        'news_final' : news_final,
    }
    return render(request,'home.html',context)

    
