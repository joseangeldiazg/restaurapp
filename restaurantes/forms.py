from django import forms
from mongoengine import *
from requests import *
import datetime
from .models import *

def parseDireccion(json):
    final = {}
    if json['results']:
        data = json['results'][0]
        for item in data['address_components']:
            for category in item['types']:
                data[category] = {}
                data[category] = item['long_name']
        final['number'] = data.get("street_number", None)
        final['street'] = data.get("route", None)
        final['city'] = data.get("locality", None)
        final['postal_code'] = data.get("postal_code", None)
        final['latitude'] = data.get("geometry", {}).get("location", {}).get("lat", None)
        final['longitude'] = data.get("geometry", {}).get("location", {}).get("lng", None)
    return final

class AddRestaurant(forms.Form):

    name    = forms.CharField(required=True, label='Nombre')
    city    = forms.CharField(required=True, label='Ciudad')
    cuisine = forms.CharField(required=True, label='Cocina')
    borough = forms.CharField(required=True, label='Zona')
    image   = forms.FileField(required=True, label='Imagen')


    def save(self, commit=True):
        url = 'http://maps.googleapis.com/maps/api/geocode/json?address='
        url = url+self.cleaned_data['name']+self.cleaned_data['city']
        response = get(url)
        data = parseDireccion(response.json());
        dir = addr(building = data['number'] , street=data['street'], city=data['city'], zipcode=data['postal_code'], coord=[data['latitude'], data['longitude']])


        r = restaurants()

        r.name = self.cleaned_data['name']
        r.restaurant_id = restaurants.objects.count() + 1
        r.cuisine = self.cleaned_data['cuisine']
        r.borough = self.cleaned_data['borough']
        r.address = dir

        restaurant_image = open('static/img/restaurants/' + str(restaurants.objects.count() + 1) + '.jpg', 'rb')
        r.image.put(restaurant_image, content_type = 'image/jpeg')

        if commit:
            r.save()

        return r
