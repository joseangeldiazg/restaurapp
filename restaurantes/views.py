from django.shortcuts import render, HttpResponse, redirect
from .models import restaurants
from django.contrib.auth.decorators import login_required
from .forms import AddRestaurant
import logging
import datetime
logger = logging.getLogger(__name__)

# Create your views here.

def handle_uploaded_file(n, f):
    with open('static/img/restaurants/' + str(n) + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    context = {
            "resta": restaurants.objects,
            "menu": "menu-inicio"
         }
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha accedido al inicio. ")
    return render (request, 'restaurantes/listar.html', context)

def listar(request):
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha accedido a listar. ")
    context = {
            "resta": restaurants.objects,
            "menu": "menu-inicio"
         }
    return render (request, 'restaurantes/listar.html', context)

def introducir(request):
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha accedido a introducir busqueda por zona. ")
    context = {
            "menu": "menu-buscar"
         }
    return render (request, 'restaurantes/introducir.html', context)

@login_required
def add(request):
    if request.method == "POST":
        form = AddRestaurant(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) != 0:
                handle_uploaded_file(restaurants.objects.count() + 1, request.FILES['image'])
            r = form.save()
            return redirect('listar')
    else:
        form = AddRestaurant();
    # GET o error
    context = {
        "form": form,
        "menu": "menu-add"
    }
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha añadido un nuevo restaurante. ")
    return render(request, 'restaurantes/addrestaurant.html', context)

def restaurant(request, id):
    restaurante = restaurants.objects(restaurant_id=id)[0]
    context = {
            "resta": restaurante,
            "imagen": str(restaurante.restaurant_id)
    }
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha accedido a la ficha de un restaurante. ")
    return render (request, 'restaurantes/restaurant.html', context)

def buscar(request):
    parametro=request.GET.get('zona')
    context={
        "resta":restaurants.objects(borough=parametro),
        "menu":"menu-resultados"
    }
    logger.info(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - se ha buscado en la zona ")
    return render (request, 'restaurantes/listar.html', context)
