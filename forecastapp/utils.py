import requests
from .manage_database import add_city, get_city_coordinates


class WeatherForecast:
    def __init__(self, city_name):
        self.city_name = city_name
        self.coordinates = self.get_coordinates(city_name)
        self.weather_data = None

    def get_coordinates(self, city_name):
        """
        Получение координат города из базы данных или  сиспользованием Nominatim.
        """
        # Проверка наличия города в базе данных
        coordinates = get_city_coordinates(city_name)
        if coordinates:
            return {'latitude': coordinates[0], 'longitude': coordinates[1]}
        url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&addressdetails=1'
        headers = {
            'User-Agent': 'forecast/1.0 (zhenyazav6666@gmail.com)'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                # Сохранение города в базе данных
                add_city(city_name, latitude, longitude)
                return {'latitude': latitude, 'longitude': longitude}
        return None

    def fetch_weather_data(self):
        """
        Получение данных о погоде с использованием Open-Meteo API.
        """
        if not self.coordinates:
            return None

        url = (f'https://api.open-meteo.com/v1/forecast?'
               f'latitude={self.coordinates["latitude"]}&'
               f'longitude={self.coordinates["longitude"]}&'
               f'current_weather=true&'
               f'hourly=temperature_2m,precipitation,rain,snowfall,surface_pressure,cloud_cover,wind_speed_10m&'
               f'forecast_hours=1'
               )
        response = requests.get(url)
        if response.status_code == 200:
            self.weather_data = response.json()
            return self.weather_data
        else:
            print(f"Ошибка запроса к API Open-Meteo: {response.status_code}")
            return None

    def get_forecast_data(self):
        """
        Формирование данных о погоде для отображения.
        """
        if not self.weather_data:
            return None

        current_weather = self.weather_data.get("current_weather", {})
        hourly_forecast = self.weather_data.get("hourly", {})

        forecast = {
            'city': self.city_name,
            'current_temperature': current_weather.get('temperature', 'N/A'),
            'windspeed': current_weather.get('windspeed', 'N/A'),
            'forecast': []
        }

        # Давление и облачность
        keys = ['temperature_2m', 'wind_speed_10m', 'surface_pressure', 'cloud_cover']
        forecast_keys = ['temperature', 'windspeed', 'pressure', 'cloud_cover']
        # Извлечение данных и создание словаря с прогнозом
        forecast_data = {forecast_key: hourly_forecast.get(key, [None])[-1] for key, forecast_key in
                         zip(keys, forecast_keys)}
        # Добавление данных в прогноз
        forecast['forecast'].append(forecast_data)

        # Проверка осадков
        precipitation = hourly_forecast.get('precipitation', [0])[-1]
        rain = hourly_forecast.get('rain', [0])[-1]
        snowfall = hourly_forecast.get('snowfall', [0])[-1]

        if precipitation > 0:
            if rain > 0:
                forecast['precipitation'] = "Ожидается дождь."
            if snowfall > 0:
                forecast['snowfall'] = "Ожидается снег."

        return forecast
