import datetime
import requests
from django.shortcuts import render

def index(request):
    API_KEY = open(r"E:\Blackcoffer\BlackcofferTraining\6_Django\weather_project\weather_app\API_KEY", "r").read()
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecase_url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    
    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2',None)
        
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecase_url)
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecase_url)
        else:
            weather_data2, daily_forecasts2 = None, None
            
        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }
        return render(request, "weather_app/index.html",context)
    else:
        return render(request, "weather_app/index.html",)
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
    }
    
    daily_forecast = []
    for i in range(0,len(forecast_response['list']),8):
        print(len(forecast_response['list']))
        print(forecast_url.format(lat,lon,api_key))
        daily_data = forecast_response['list'][i]
        daily_forecast.append({
            "day": datetime.datetime.utcfromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['main']['temp_min'] - 273.15, 2),
            "max_temp": round(daily_data['main']['temp_max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon'],
        })
    print(daily_forecast)
        
    return weather_data, daily_forecast