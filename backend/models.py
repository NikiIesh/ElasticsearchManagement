from django.db import models


# Create your models here.
class url(models.Model):
    ip = models.CharField(max_length=500)
    port=models.CharField(max_length=500)
