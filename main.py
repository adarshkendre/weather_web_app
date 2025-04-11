from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# You'll need to replace this with your actual API key
API_KEY = "4112324bfd37b70dcae954bb3dfec32e"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9/5 + 32, 1)

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        if not city:
            error = "Please enter a city name"
        else:
            params = {
                'q': city,
                'appid': API_KEY
            }
            
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                weather_data = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temp': kelvin_to_celsius(data['main']['temp']),
                    'temp_f': kelvin_to_fahrenheit(data['main']['temp']),
                    'feels_like': kelvin_to_celsius(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'sunrise': format_timestamp(data['sys']['sunrise']),
                    'sunset': format_timestamp(data['sys']['sunset'])
                }
            else:
                error = "City not found. Please try again."
    
    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)