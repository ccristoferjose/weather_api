# Weather Application Documentation

## Overview

This application fetches real-time weather data from the OpenWeatherMap API and stores it in a SQL database. The data includes the current weather conditions for a specific latitude and longitude.

**Installation**
Before running the application, you need to install the required Python libraries. You can do this using pip, which is a package manager for Python. Open your terminal and type the following commands:

```bash
pip install requests
pip install json
pip install sqlalchemy
```

You can set up your python enviroment if needed `python -m venv myenv`. 

**Dependencies**

1. *requests*: Used to send HTTP requests.
2. *json:* Used to parse the JSON response from the API.
3. *sqlalchemy:* Used to interact with the SQL database.
4. *API Key:* You need an API key from OpenWeatherMap to use their API. Replace {API key} with your actual OpenWeatherMap API key.

**Base URL**
The base URL for the One Call API 3.0 is https://api.openweathermap.org/data/3.0/onecall?.

**Location Coordinates**
The application fetches weather data for the coordinates specified in the latitude and longitude variables.

**API Request**
The application sends a GET request to the API with the specified latitude, longitude, and API key. The exclude parameter is used to exclude hourly and daily data from the response.

**JSON Response**
If the API request is successful (status code 200), the application parses the JSON response and prints it in a formatted way.

**SQL Database**
The application connects to a SQL server using SQLAlchemy. It defines a table WeatherData with columns for id, lat, lon, timezone, and current_weather. After creating the table in the database, it inserts the weather information into the table.

```sql
CREATE TABLE locations (
    id INT IDENTITY(1,1) PRIMARY KEY,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    timezone VARCHAR(50),
    timezone_offset INT
);

CREATE TABLE current_weather (
    id INT IDENTITY(1,1) PRIMARY KEY,
    location_id INT,
    dt BIGINT,
    sunrise BIGINT,
    sunset BIGINT,
    temp DECIMAL(5, 2),
    feels_like DECIMAL(5, 2),
    pressure INT,
    humidity INT,
    dew_point DECIMAL(5, 2),
    uvi DECIMAL(3, 2),
    clouds INT,
    visibility INT,
    wind_speed DECIMAL(5, 2),
    wind_deg INT,
    wind_gust DECIMAL(5, 2),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE rain (
    id INT IDENTITY(1,1) PRIMARY KEY,
    current_weather_id INT,
    rain_1h DECIMAL(6, 2),
    FOREIGN KEY (current_weather_id) REFERENCES current_weather(id)
);

CREATE TABLE weather_descriptions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    current_weather_id INT,
    weather_id INT,
    main VARCHAR(50),
    description VARCHAR(100),
    icon VARCHAR(10),
    FOREIGN KEY (current_weather_id) REFERENCES current_weather(id)
);
```

**Error Handling**
If the API request is not successful, the application prints an error message with the status code.


**Running the Program**

To run the program, navigate to the directory containing the Python script in your terminal and type the following command:

```bash
python weather.py
```

**Test Example**

```bash
Main Menu:
1. Get weather data for a location
2. Exit
Enter your choice: 1
Enter the latitude: 34
Enter the longitude: -118
Timezone: America/Los_Angeles
UVI: 9.15
Clouds: 0
Visibility: 10000
Main Menu:
1. Get weather data for a location
2. Exit
Enter your choice: 2
```