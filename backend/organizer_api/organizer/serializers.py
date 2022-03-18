from rest_framework import serializers
from .models import Scrap

class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        # name = serializers.FileField()
        # csv = serializers.FileField()
        fields = ('id', 'name', 'author', 'csv')
        
        