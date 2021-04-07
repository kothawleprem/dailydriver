from django.db import models

# Create your models here.
class Location(models.Model):
    text = models.CharField(max_length = 45)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'cities'
