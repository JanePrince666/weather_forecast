from django.db import models


# Create your models here.
class CitySearch(models.Model):
    user_ip = models.CharField(max_length=255)  # Убедитесь, что это поле есть
    city_name = models.CharField(max_length=255)
    search_count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_ip', 'city_name')
        db_table = 'city_searches'

    def __str__(self):
        return self.city_name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name
