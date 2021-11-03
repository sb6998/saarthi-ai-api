from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class api(models.Model):
    name = models.CharField(max_length = 200)
    isbn = models.CharField(max_length = 100)
    authors = ArrayField(models.CharField(max_length =100))
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    release_date = models.DateField()
    def __str__(self):
        return self.name