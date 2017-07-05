from django.conf.urls import url, include
from rest_framework_mongoengine import routers

from . import views
from . import serializers

router = routers.DefaultRouter()

   # register REST API endpoints with DRF router
router.register(r'restaurants', serializers.restaurantsViewSet, r"restaurants")

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^listar/$', views.listar, name='listar'),
  url(r'^listar/introducir/$', views.introducir, name='introducir'),
  url(r'^introducir/$', views.introducir, name='introducir'),
  url(r'^buscar/$', views.buscar, name='buscar'),
  url(r'^restaurant/(?P<id>[0-9]+)$', views.restaurant, name='restaurant'),
  url(r'^addrestaurant/$', views.add, name="addrestaurant"),
  url(r'^api/', include(router.urls, namespace='api')),
]
