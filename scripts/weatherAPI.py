import requests
import pandas as pd
APIkey = '3b44ca87fb86045dc73d251817916e47'

dfCities = pd.read_csv('../data/worldcities.csv')
dfCities = dfCities.head(10)

successRequests = []
failedRequests = []


def getWeather(lat, lon, APIkey):

    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}&units=metric')
        r.raise_for_status()
        weatherData = r.json()

        weather = {
            "id": weatherData['id'],
            "city": weatherData['name'],
            "latitude": weatherData['coord']['lat'],
            "longitude": weatherData['coord']['lon'],
            "country": weatherData['sys']['country'],
            "description": weatherData['weather'][0]['description'],
            "temp": weatherData['main']['temp'],
            "temp_min": weatherData['main']['temp_min'],
            "temp_max": weatherData['main']['temp_max'],
            "feels_like": weatherData['main']['feels_like'],
            "humidity": weatherData['main']['humidity'],
            "wind_speed": weatherData['wind']['speed']
        }

        return(weather)

    except requests.exceptions.HTTPError as e:
        errorData = e.response.json()

        error = {
            'Error Code': errorData['cod'],
            'Error Message': errorData['message'],
            'latitute': lat,
            'longitude': lon
        }
        return (errorData, error)

latlonDict = [
    (42, 21.4333),
    (42,24),
    (41,41),
    (999, 53),
    (999,999),
    (41, -500)
]

for lat, lon in latlonDict:
    result = getWeather(lat, lon, APIkey)

    if isinstance(result, tuple):
        errorData = result[1]
        failedRequests.append(errorData)

    else:
        successRequests.append(result)



for index, row in dfCities.iterrows():
    lat = row['lat']
    lon = row['lng']

    weatherInfo = getWeather(lat, lon, APIkey)

    successRequests.append(weatherInfo)

df = pd.DataFrame(successRequests)
dfErrors = pd.DataFrame(failedRequests)


df.to_csv(f"../output/apiRequests.csv",index=False)
dfErrors.to_csv(f"../output/errorRequests.csv",index=False)


