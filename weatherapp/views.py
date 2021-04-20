from django.shortcuts import render
from ipstack import GeoLookup
import requests
from functools import partial

from .models import Location
from django.views.decorators.http import require_POST
from . forms import CategoryForm
import os

from bs4 import BeautifulSoup

from functools import partial
import requests
from geopy.geocoders import Nominatim

def home(request):
    city = ""
    if 'city' in request.GET:
        # if city == "":
        #     geo_lookup = GeoLookup("582179b24ab7f5f07d71c6fb0be3fc7c")
        #     ulocation = geo_lookup.get_own_location()
        #     # print(ulocation)
        #     city = ulocation["city"]
        #     api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=5bc57ba9bc106c9844915b5178ee10ad"
        # else:
        #     city = request.GET.get('city')
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

    myapi = f"https://nominatim.openstreetmap.org/search?city=<{city}>&format=json"
    # From the api we get data.
    json_data = requests.get(myapi).json()
    part = json_data[0]
    display_name = part["display_name"]
    c_list = list(map(str,display_name.split(",")))
    country = c_list[-1].strip()

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


    if category == "":
        mycategory = "General"
    else:
        mycategory = category.capitalize()
   
    if category == "":
        mycategory = "General"
    else:
        mycategory = category.capitalize()
    
    if country == "United Kingdom":
        country = "uk"
    if country == "United States":
        country = 'us'
    html_text = requests.get(f'https://www.worldometers.info/coronavirus/country/{country}').text
    soup = BeautifulSoup(html_text,'lxml')
    main_counter = soup.find_all('div',id='maincounter-wrap')
    cases_counter = main_counter[0]  # to get first 'maincounter-wrap' out of 3
    cases_number = cases_counter.find('div',class_='maincounter-number')
    cases = cases_number.find('span').text
    deaths_counter = main_counter[1] # to get second 'maincounter-wrap' out of 3
    deaths_number = deaths_counter.find('div',class_='maincounter-number')
    deaths = deaths_number.find('span').text
    recovered_counter = main_counter[2] # to get third 'maincounter-wrap' out of 3
    recovered_number = recovered_counter.find('div',class_='maincounter-number')
    recovered = recovered_number.find('span').text

    description = ''
    location = ''
    time = ''
    link = ''
    html_text = requests.get('https://sports.ndtv.com/cricket/live-scores').text
    soup = BeautifulSoup(html_text, "html.parser")
    sect = soup.find_all('div',class_='sp-scr_wrp')
    section = sect[0]
    description = section.find('span',class_='description').text
    location = section.find('span',class_='location').text
    time = section.find('div',class_='scr_dt-red').text
    link = "https://sports.ndtv.com/" + section.find('a',class_='scr_ful-sbr-txt').get('href')
    toss = ''
    team1_name = ''
    team1_score = ''
    team2_name = ''
    team2_score = ''
    try:
        toss = section.find('div',class_="scr_dt-red @*scr-inf_tx*@").text
        block = section.find_all('div',class_='scr_tm-wrp')
        team1_block = block[0]
        team1_name = team1_block.find('div',class_='scr_tm-nm').text
        team1_score = team1_block.find('span',class_='scr_tm-run').text
        team2_block = block[1]
        team2_name = team2_block.find('div',class_='scr_tm-nm').text
        team2_score = team2_block.find('span',class_='scr_tm-run').text
    except:
        print("Some Error Found")
    url = "https://www.affirmations.dev/"
    myjson= requests.get(url).json()
    affirmation = myjson['affirmation']
    context = {
        'city' : city,
        'temp' : temp,
        'min_temp' : min_temp,
        'max_temp' : max_temp,
        'feels_like' : feels_like,
        'pressure' : pressure,
        'humidity' : humidity,

        'contents' : contents,
        'category' : mycategory,
        'cases' : cases,
        'deaths' : deaths,
        'recovered' : recovered,
        'country' : country.upper(),
        'description' : description,
        'location' : location,
        'time' : time,
        'toss' : toss,
        'team1_name' : team1_name,
        'team1_score' : team1_score,
        'team2_name' : team2_name,
        'team2_score' : team2_score,
        'link' : link,
        'affirmation' : affirmation,
    }
    return render(request,'home.html',context)

    
