from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *

# Create your views here.
@login_required
def index(request):
    user = User.objects.get(username=request.user.username)
    context = {
        "username": user.username,
        "order": Order.objects.get(pk=request.session["current_order"]),
        "pizzas": PizzaType.objects.all(),
        "pizza_toppings": PizzaTopping.objects.all(),
        "subs": SubType.objects.all(),
        "sub_toppings": SubTopping.objects.all(),
        "pastas": PastaType.objects.all(),
        "salads": SaladType.objects.all(),
        "platters": PlatterType.objects.all(),
    }
    print(context["order"])
    return render(request, "orders/index.html", context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            try:
                current_order = Order.objects.get(user=user, submitted=False)
            except ObjectDoesNotExist:
                current_order = Order(user=user)
                current_order.save()
            request.session["current_order"] = current_order.id
            return HttpResponseRedirect(reverse("index"))
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = UserCreationForm()
    context = {"form": form}
    return render(request, "authentication/register.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                current_order = Order.objects.get(user=user, submitted=False)
            except ObjectDoesNotExist:
                current_order = Order(user=user)
                current_order.save()
            request.session["current_order"] = current_order.id
            print(f"logged in as {username}")
            return HttpResponseRedirect(reverse("index"))
        else:
            print(f"Invalid credentials.")
            return render(request, "authentication/login.html", {"message": "Invalid credentials."})
    return render(request, "authentication/login.html", {"message": None})

@login_required
def logout_view(request):
    del request.session['current_order']
    logout(request)
    return redirect('login')

@login_required
def add(request, item_type, item_id, size):
    current_order = Order.objects.get(pk=request.session["current_order"])
    new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")

    if item_type == "PlatterType":
        new_item = eval(item_type[:-4] +
                        "(order=current_order, type=new_item_type, size=size)")
    elif item_type == "PastaType":
        new_item = eval(item_type[:-4] +
                        "(order=current_order, type=new_item_type)")
    elif item_type == "SaladType":
        new_item = eval(item_type[:-4] +
                        "(order=current_order, type=new_item_type)")
    elif item_type == "SubType":
        new_item = eval(item_type[:-4] +
                        "(order=current_order, type=new_item_type, size=size)")
        new_item.save()
    elif item_type == "PizzaType":
        new_item = eval(item_type[:-4] +
                        "(order=current_order, type=new_item_type, size=size)")
        new_item.save()

    new_item.calculate_price()
    new_item.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete_item(request, item_type, item_id):
    current_order = Order.objects.get(pk=request.session["current_order"])
    item = eval(item_type + ".objects.get(order=current_order, pk=" + str(item_id) + ")")
    item.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete_order(request):
    current_order = Order.objects.get(pk=request.session["current_order"])
    items = current_order.get_items()
    for item in items:
        item.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def submit_order(request):
    #TODO
    pass
