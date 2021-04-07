from django.shortcuts import render
from ipstack import GeoLookup
import requests

from .models import Location
from django.views.decorators.http import require_POST
from . forms import CategoryForm
import os

from bs4 import BeautifulSoup

from functools import partial
import requests
from geopy.geocoders import Nominatim

# news_final = []
# html_text = requests.get('https://www.ndtv.com/india').text
# soup = BeautifulSoup(html_text,'lxml')
# articles = soup.find_all('div',class_='news_Itm')
# for article in articles:
#     try:
#         news_initial = []
#         content = article.find('div',class_='news_Itm-cont')
#         heading = content.find('h2',class_='newsHdng').text
#         link = content.find('h2',class_='newsHdng').a['href']
#         brief = content.find('p',class_='newsCont').text
#         news_initial.append(heading)
#         news_initial.append(brief)
#         news_initial.append(link)
#         news_final.append(news_initial)
#         # print(f" Heading : {heading}")
#         # print(f" Link    : {link}")
#         # print(f" Brief   : {brief}")
#         # print("")
#     except:
#         print("")    
#############################################################
def home(request):
    city = ""
    if 'city' in request.GET:
        city = request.GET.get('city')
        api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5bc57ba9bc106c9844915b5178ee10ad"
    else:
        geo_lookup = GeoLookup("582179b24ab7f5f07d71c6fb0be3fc7c")
        ulocation = geo_lookup.get_own_location()
        # print(ulocation)
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

    # geolocator = Nominatim(user_agent="techbayindia@gmail.com")
    # geocode = partial(geolocator.geocode, language="en")
    # location = str(geocode(city))
    # c = list(map(str, location.split(",")))
    # country = c[-1].strip()
    # print(country)
    country = "India"

    # Currently testing for 4 countries can do for 46 more.
    code = ""
    mylist = [["United Arab Emirates", "ae"], ["India", "in"], ["United Kingdom", "gb"], ["United States", "us"], ["Australia", "au"]]
    for i in range(len(mylist)+1):
        # print(mylist[i][0])
        if country == mylist[i][0]:
            code = mylist[i][1]
            # print(code)
            break

    # mylist = [["United Arab Emirates","ae"],[] ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za]
    category="general"
    if 'category' in request.GET:
        category=request.GET.get('category')
        print(category)
    contents = []
    if len(code) == 2:
        myapi = f"https://newsapi.org/v2/top-headlines?country={code}&category={category}&apiKey=147894c490b84cfaaf3b534cf5a39050"
        json_data = requests.get(myapi).json()
        articles = json_data["articles"]
        for article in articles:
            content = []
            title = "->" + article['title']
            description = article['description']
            url = article['url']
            content.append(title)
            content.append(description)
            content.append(url)
            contents.append(content)
    else:
        print("Country not found")


 


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
        'contents' : contents,
    }
    return render(request,'home.html',context)

    
