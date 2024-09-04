from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = '5f7069317f456bba3ba98f99573719fd'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ua&APPID=' + appid
    # https: // api.openweathermap.org / data / 2.5 / weather?q = Kyiv & lang = uk & APPID = 5
    # f7069317f456bba3ba98f99573719fd

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        response = requests.get(url.format(city.name)).json()

        city_info = {
            'city': city.name,
            'description': response['weather'][0]['description'].title(),
            'temp': response['main']['temp'],
            'wind': response['wind']['speed'],
            'humidity': response['main']['humidity'],
            'icon': response['weather'][0]['icon'],
        }

        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
    }

    return render(request, 'weather/index.html', context)
