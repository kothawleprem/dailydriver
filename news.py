# pip install geopy
# pip install requests

from functools import partial
import requests
from geopy.geocoders import Nominatim





city = str(input("Enter City:"))
myapi = f"https://nominatim.openstreetmap.org/search?city=<{city}>&format=json"
# From the api we get data.
json_data = requests.get(myapi).json()
part = json_data[0]
display_name = part["display_name"]
c_list = list(map(str,display_name.split(",")))
country = c_list[-1].strip()





# Firstly we take the required city from the user.



# Currently testing for 4 countries can do for 50 more.
# Now checking the received country and converting it to the country code.
code = ""
mylist = [["United Arab Emirates", "ae"], ["India", "in"], ["United Kingdom", "gb"], ["United States", "us"], ["Australia", "au"]]
for i in range(len(mylist)+1):
    # print(mylist[i][0])
    if country == mylist[i][0]:
        code = mylist[i][1]
        # print(code)
        break

# mylist = [["United Arab Emirates","ae"],[] ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za]
# Getting category from user.
# business, entertainment, general, health, science, sports, technology
category = input("Enter Category")

contents = []
# If entered city gives correct country and then code we move to newsapi.
if len(code) == 2:
    myapi = f"https://newsapi.org/v2/top-headlines?country={code}&category={category}&apiKey=3b898b7e09c04eed9bb2be0e3dba2f07"
    # From the api we get data.
    json_data = requests.get(myapi).json()
    # We choose the articles section
    articles = json_data["articles"]
    for article in articles:
        # We iterate over each part in articles,get required information and store in a list.
        content = []
        title = article['title']
        description = article['description']
        url = article['url']
        content.append(title)
        content.append(description)
        content.append(url)
        # Finally we add this list to another list
        contents.append(content)
else:
    print("Country not found")

# content = [title,description,url]
# contents = [[content],[content],[content]]
for c in contents:
    print("Heading:",c[0])
    print("Description:",c[1])
    print("URL:",c[2])
