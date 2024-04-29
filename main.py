import requests
import json
import csv
import time
import os

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "f81e26bd13c25320f23c934dd8c1d74d"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    if response.status_code == 200: 
        return json.loads(response.text)   
    return None

def save_weather_to_csv(weather_data, file_name='data.csv'):
    csv_header = ["city_name", "lat", "lon", "timezone_offset", "dt", "sunrise", "sunset", "temp", "feels_like", "pressure", "humidity", "dew_point", "uvi", "clouds", "visibility", "wind_speed", "wind_deg", "wind_gust", "weather_id", "weather_main", "weather_description", "weather_icon"]
    
    file_exists = os.path.exists(file_name)
    
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(csv_header)
        
        if weather_data and weather_data["cod"] == 200:
            data_to_save = [
                weather_data['name'],
                weather_data['coord']['lat'], weather_data['coord']['lon'],
                weather_data['timezone'],
                weather_data['dt'],
                weather_data['sys']['sunrise'], weather_data['sys']['sunset'],
                weather_data['main']['temp'], weather_data['main']['feels_like'],
                weather_data['main']['pressure'], weather_data['main']['humidity'],
                weather_data['main'].get('dew_point', ""),  # Optional
                weather_data.get('uvi', ""),  # Optional
                weather_data['clouds']['all'], weather_data['visibility'],
                weather_data['wind']['speed'], weather_data['wind']['deg'],
                weather_data['wind'].get('gust', ""),  # Optional
                weather_data['weather'][0]['id'], weather_data['weather'][0]['main'],
                weather_data['weather'][0]['description'], weather_data['weather'][0]['icon']
            ]
            writer.writerow(data_to_save)
        else:
            print("City Not Found or API Error")

if __name__ == "__main__":
    city = "Los Angeles"
    file_exists = os.path.exists('data.csv')
    while True: 
        weather_data = get_weather(city)      
        if weather_data:
            save_weather_to_csv(weather_data)
            print("Weather data saved for Los Angeles.")
        else:
            print("Failed to retrieve weather data.")
        time.sleep(60) #Wait for 60 seconds before next request.