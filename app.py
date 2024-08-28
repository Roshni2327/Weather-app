from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

TIMEZONE_API_KEY = 'GC3QXYIHO0O8'  # Your TimeZoneDB API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if not city:
        return "City name is required", 400

    api_key = '871da2a6732da40a3868e0d7a5a0348f'  # OpenWeatherMap API key
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    if weather_data.get('cod') != 200:
        return "City not found", 404

    # Extract latitude and longitude for TimeZoneDB
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    
    weather_info = {
        'city': weather_data['name'],
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'icon': weather_data['weather'][0]['icon'],
    }
    
    return render_template('weather.html', weather=weather_info)

@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form.get('city')
    if not city:
        return "City name is required", 400

    api_key = '871da2a6732da40a3868e0d7a5a0348f'  # OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != '200':
        return "City not found", 404

    # Initialize an empty dictionary to store forecasts
    daily_forecast = {}
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]  # Extract the date from the timestamp
        if date not in daily_forecast:
            daily_forecast[date] = {
                'date': date,
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description']
            }
    
    # Convert the dictionary to a list for rendering
    forecast_info = list(daily_forecast.values())
    
    return render_template('forecast.html', forecast=forecast_info)

@app.route('/location', methods=['POST'])
def location():
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    if not lat or not lon:
        return "Latitude and Longitude are required", 400

    api_key = '871da2a6732da40a3868e0d7a5a0348f'  # OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != 200:
        return "Location not found", 404

    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    
    return render_template('weather.html', weather=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
