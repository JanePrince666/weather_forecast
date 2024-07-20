from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from .forms import CityForm
from .utils import WeatherForecast
from .manage_database import get_all_cities, add_city, update_search_count, get_search_history
from .models import SearchHistory


# Класс для отображения погоды
class WeatherView(TemplateView):
    template_name = 'home_page.html'

    def get_initial(self):
        return {'city': '', 'weather_data': None}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CityForm(initial=self.get_initial())
        context['cities'] = get_all_cities()

        if 'last_city' in self.request.session:
            context['last_city'] = self.request.session['last_city']
            weather_forecast = WeatherForecast(context['last_city'])
            weather_forecast.fetch_weather_data()
            context['weather_data'] = weather_forecast.get_forecast_data()

        return context

    def post(self, request, *args, **kwargs):
        city = request.POST.get('city')
        weather_forecast = WeatherForecast(city)
        weather_forecast.fetch_weather_data()
        weather_data = weather_forecast.get_forecast_data()

        request.session['last_city'] = city
        user_ip = request.META.get('REMOTE_ADDR')

        # Обновление счетчика поисков в базе данных
        update_search_count(city, user_ip)

        coordinates = weather_forecast.coordinates
        if coordinates:
            add_city(city, coordinates['latitude'], coordinates['longitude'])

        context = {
            'form': CityForm(initial={'city': city}),
            'weather_data': weather_data,
            'cities': get_all_cities()
        }

        if weather_data:
            return render(self.request, self.template_name, context)
        else:
            context['error_message'] = "Город не найден. Пожалуйста, попробуйте снова."
            return render(self.request, self.template_name, context)


# Класс для отображения истории поиска
class SearchHistoryView(View):
    def get(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        history = get_search_history(user_ip)
        return JsonResponse(history, safe=False, json_dumps_params={'ensure_ascii': False})
