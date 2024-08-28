from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if not city:
        return "City name is required", 400
    api_key = '871da2a6732da40a3868e0d7a5a0348f'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    print(f"API Response: {data}")  # Debugging statement
    
    if data.get('cod') != 200:
        return "City not found", 404

    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    
    return render_template('weather.html', weather=weather_info)

@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form.get('city')
    api_key = '871da2a6732da40a3868e0d7a5a0348f'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != '200':
        return "City not found", 404

    forecast_info = []
    for item in data['list']:
        forecast_info.append({
            'date': item['dt_txt'],
            'temperature': item['main']['temp'],
            'description': item['weather'][0]['description']
        })
    
    return render_template('forecast.html', forecast=forecast_info)

@app.route('/location', methods=['POST'])
def location():
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    if not lat or not lon:
        return "Location coordinates are required", 400
    
    api_key = '871da2a6732da40a3868e0d7a5a0348f'
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
@app.route('/test', methods=['GET', 'POST'])
def test():
    return "Test route is working!"

if __name__ == '__main__':
    app.run(debug=True)

