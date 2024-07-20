from django.db import models


# Create your models here.
class CitySearch(models.Model):
    city_name = models.CharField(max_length=255)
    search_count = models.IntegerField(default=0)
    search_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'city_searches'  # Убедитесь, что имя таблицы указано правильно

    def __str__(self):
        return self.city_name
