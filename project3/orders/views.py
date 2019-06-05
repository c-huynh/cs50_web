from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        "pizza_types": PizzaType.objects.all(),
        "pizza_toppings": PizzaTopping.objects.all(),
        "sub_types": SubType.objects.all(),
        "sub_toppings": SubTopping.objects.all(),
        "pastas": PastaType.objects.all(),
        "salads": SaladType.objects.all(),
        "platters": PlatterType.objects.all()
    }
    return render(request, "orders/index.html", context)
