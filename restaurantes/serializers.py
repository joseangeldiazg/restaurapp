from rest_framework_mongoengine import serializers
from rest_framework_mongoengine import viewsets
from rest_framework import filters

from requests import *

from .models import restaurants

class restaurantsSerializer(serializers.DocumentSerializer):

    class Meta:
        model = restaurants
        fields = ('name', 'cuisine', 'borough', 'address', 'image')


class restaurantsViewSet(viewsets.ModelViewSet):
    serializer_class = restaurantsSerializer
    queryset= restaurants.objects.all()

    def get_queryset(self):
        queryset= restaurants.objects.all()
        cuisine = self.request.query_params.get('cuisine', None)
        if cuisine is not None:
            queryset = queryset.filter(cuisine=cuisine)

        return queryset
