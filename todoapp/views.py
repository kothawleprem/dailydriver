from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from todoapp.forms import TodoForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from todoapp.models import Todo, Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
#----------------------
from ipstack import GeoLookup
import requests
from functools import partial

# from .models import Location
from django.views.decorators.http import require_POST
# from . forms import CategoryForm
import os

from bs4 import BeautifulSoup

from functools import partial
import requests
from geopy.geocoders import Nominatim


@login_required(login_url='user_login')
def home(request):
#-------------------------------------------------
    if request.user.is_authenticated:
        user_category = ''
        user = request.user
        user_category = user.profile.category
        form = TodoForm()
        todos = Todo.objects.filter(user=user).order_by('priority')
        city = ""
        if 'city' in request.GET:
            city = request.GET.get('city')
            if len(city) < 2:
                geo_lookup = GeoLookup("582179b24ab7f5f07d71c6fb0be3fc7c")
                ulocation = geo_lookup.get_own_location()
                city = ulocation["city"]
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
#-------------------------------------------------------
        myapi = f"https://nominatim.openstreetmap.org/search?city=<{city}>&format=json"
        # From the api we get data.
        json_data = requests.get(myapi).json()
        part = json_data[0]
        display_name = part["display_name"]
        c_list = list(map(str,display_name.split(",")))
        co = c_list[-1].strip()
        # translator = google_translator()
        # to_lang = 'en'
        # con = translator.translate(co,lang_tgt=to_lang)
        # country = con.rstrip()
        country = co
        print(country)
        # Currently testing for 4 countries can do for 46 more.
        code = ""
        mylist = [["United Arab Emirates","ae"],["United States", "us"],["Australia", "au"],  ["India", "in"],["Argentina","ar"], ["Austria","at"],["Beligum","be"], ["Bulgaria","bg"], ["Brazil","br"], ["Canada","ca"], ["China","cn"], ["Colombia","co"], ["Cuba","cu"], ["Czechia","cz"],["Egypt","eg"], ["France","fr"],["United Kingdom", "gb"], ["Greece","gr"], ["Hong Kong","hk"], ["Hungry","hu"], ["Indonesia","id"], ["Ireland","ie"], ["Israel","il"], ["Italy","it"], ["Japan","jp"], ["Korea","kr"], ["Lithuania","lt"], ["Latvia","lv"], ["Morocco","ma"], ["Mexico","mx"], ["Malaysia","my"], ["Nigeria","ng"], ["Netherlands","nl"], ["Norway","no"], ["New Zealand","nz"], ["Philippines","ph"], ["Poland","pl"], ["Portugal","pt"], ["Romania","ro"], ["rs"],  ["Rusia","ru"], ["Saudi Arabia","sa"], ["Sweden","se"], ["Singapore","sg"], ["Slovenia","si"], ["Slovakia","sk"], ["Thailand","th"], ["Turkey","tr"], ["Taiwan","tw"], ["Ukraine","ua"], ["Venezuela","ve"], ["South Africa","za"]]

        for i in range(len(mylist)+1):
        # print(mylist[i][0])
            if country == mylist[i][0]:
                code = mylist[i][1]
                # print(code)
                break
#----------------------------------------------------
        if user_category == '':
            category = 'general'
        else:
            category=user_category
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
            'form' : form,
            'todos' : todos,
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
        return render(request,'todoapp/index.html',context)


def user_login(request):
    if request.method == 'GET':
        form =  AuthenticationForm()
        context = {
            'form' : form
        }
        return render(request,'todoapp/login.html',context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            print('Authenticate', user)
        else:
            context = {
            'form' : form
            }
            return render(request,'todoapp/login.html',context)

def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('user_login')
        else:
            return redirect('user_signup')
    else:
        form = UserRegisterForm()
        context = {'form' : form}
        return render(request,'todoapp/signup.html',context)

def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect("home")
        else:
            context = {
                'form' : form
            }
            return render(request,'todoapp/index.html',context)

def delete_todo(request,id):
    print(id)
    Todo.objects.get(pk=id).delete()
    return redirect('home')

def change_status(request,id,status):
    todo = Todo.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def emailme(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            queryset = Todo.objects.filter(user_id=user.id).values().order_by('priority')
            total_str = ""
            global status
            for q in queryset:
                if q['status'] == 'P':
                    status = 'Pending'
                if q['status'] == 'C':
                    status = 'Complete'
                total_str = total_str + f"<tr><td>{q['title']}</td><td>{status}</td><td>{q['priority']}</td></tr>"
            heading = "<html><table ><thead > <tr><th>Title</th><th>Status</th><th>Priority</th> </tr></thead> "
            # print(todo)
            uemail = request.POST.get("uemail")
            html_content = heading+total_str+"</html>"
            print(uemail)
            subject, from_email, to = 'Your Todo From Dailydriver has Arrived!!!', settings.EMAIL_HOST_USER,uemail
            text_content = 'Chart Sent Successfully'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    return redirect('home')

@login_required(login_url='user_login')
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'todoapp/profile.html',context)
