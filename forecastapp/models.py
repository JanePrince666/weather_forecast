from django.db import models


# Create your models here.
class SearchHistory(models.Model):
    city_name = models.CharField(max_length=255)
    user_ip = models.CharField(max_length=45)  # Достаточно для хранения IPv6
    search_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.city_name} - {self.search_count} раз"
