from django.shortcuts import render
import requests
from .models import *
from .forms import *

def index(request):
    appid = '34c7d0b54458f883c5b145995200072d'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+appid
    form = CityForm()
    if request.method == 'POST':
        if requests.get(url.format(request.POST.get('name'))).json().get('message') == 'city not found':
            return render(request, 'wap/index.html', {'all_info':'not found','form':form})
        form = CityForm(request.POST)
        form.save()

    cities = City.objects.all()
    all_cities = []

    for i in cities:
        res = requests.get(url.format(i)).json()
        city_info = {
            'city' : i,
            'temp' : res['main']['temp'],
            'icon' : res['weather'][0]['icon']
        }
        all_cities.append(city_info)
    context = {'all_info':all_cities,'form':form}
    return render(request,'wap/index.html',context)

