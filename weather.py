import requests
import json
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker

def get_weather_data(latitude, longitude, api_key):
    base_url = "https://api.openweathermap.org/data/3.0/onecall?"
    exclude = "hourly,daily" 
    complete_url = base_url + "lat=" + latitude + "&lon=" + longitude + "&exclude=" + exclude + "&appid=" + api_key
    response = requests.get(complete_url)
    return response.json()

def store_weather_data(data, engine):
    metadata = MetaData()

    locations = Table('locations', metadata,
        Column('id', Integer, primary_key=True),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('timezone', String(50)),
        Column('timezone_offset', Integer)
    )

    current_weather = Table('current_weather', metadata,
        Column('id', Integer, primary_key=True),
        Column('location_id', Integer, ForeignKey('locations.id')),
        Column('dt', BigInteger),
        Column('sunrise', BigInteger),
        Column('sunset', BigInteger),
        Column('temp', Float),
        Column('feels_like', Float),
        Column('pressure', Integer),
        Column('humidity', Integer),
        Column('dew_point', Float),
        Column('uvi', Float),
        Column('clouds', Integer),
        Column('visibility', Integer),
        Column('wind_speed', Float),
        Column('wind_deg', Integer),
        Column('wind_gust', Float)
    )

    rain = Table('rain', metadata,
        Column('id', Integer, primary_key=True),
        Column('current_weather_id', Integer, ForeignKey('current_weather.id')),
        Column('rain_1h', Float)
    )

    weather_descriptions = Table('weather_descriptions', metadata,
        Column('id', Integer, primary_key=True),
        Column('current_weather_id', Integer, ForeignKey('current_weather.id')),
        Column('weather_id', Integer),
        Column('main', String(50)),
        Column('description', String(100)),
        Column('icon', String(10))
    )

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Insert location information into the table
        insert_stmt = locations.insert().values(latitude=data['lat'], longitude=data['lon'], timezone=data['timezone'], timezone_offset=data['timezone_offset'])
        result = session.execute(insert_stmt)
        location_id = result.inserted_primary_key[0]

        # Insert current weather information into the table
        insert_stmt = current_weather.insert().values(location_id=location_id, dt=data['current']['dt'], sunrise=data['current']['sunrise'], sunset=data['current']['sunset'],
                                                      temp=data['current']['temp'], feels_like=data['current']['feels_like'], pressure=data['current']['pressure'],
                                                      humidity=data['current']['humidity'], dew_point=data['current']['dew_point'], uvi=data['current']['uvi'],
                                                      clouds=data['current']['clouds'], visibility=data['current']['visibility'], wind_speed=data['current']['wind_speed'],
                                                      wind_deg=data['current'].get('wind_deg', None), wind_gust=data['current'].get('wind_gust', None))
        result = session.execute(insert_stmt)
        current_weather_id = result.inserted_primary_key[0]

        # Insert rain information into the table
        if 'rain' in data['current']:
            insert_stmt = rain.insert().values(current_weather_id=current_weather_id, rain_1h=data['current']['rain']['1h'])
            session.execute(insert_stmt)

        # Insert weather descriptions into the table
        for weather in data['current']['weather']:
            insert_stmt = weather_descriptions.insert().values(current_weather_id=current_weather_id, weather_id=weather['id'], main=weather['main'],
                                                              description=weather['description'], icon=weather['icon'])
            session.execute(insert_stmt)

        session.commit()

    except KeyError as e:
        print(f"Error: {e}")
        session.rollback()

    finally:
        session.close()

def print_main_info(data):
    print("Timezone:", data['timezone'])
    print("UVI:", data['current']['uvi'])
    print("Clouds:", data['current']['clouds'])
    print("Visibility:", data['current']['visibility'])

def main():
    api_key = "[YOUR_API_KEY]"
    # This string conection is using windows authentication 
    engine = create_engine('mssql+pyodbc://[SERVER_NAME]/STG?driver=ODBC+Driver+17+for+SQL+Server')

    while True:
        print("Main Menu:")
        print("1. Get weather data for a location")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            latitude = input("Enter the latitude: ")
            longitude = input("Enter the longitude: ")
            data = get_weather_data(latitude, longitude, api_key)
            store_weather_data(data, engine)
            print_main_info(data)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()