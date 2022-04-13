from rest_framework import serializers
from . import models

class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Api
        fields=('apiId','urlreq')
