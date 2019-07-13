from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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
    if request.method == 'POST':
        current_order = Order.objects.get(pk=request.session["current_order"])

        if item_type == "PlatterType":
            new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")
            new_item = eval(item_type[:-4] +
                            "(order=current_order, type=new_item_type, size=size)")
        elif item_type == "PastaType":
            new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")
            new_item = eval(item_type[:-4] +
                            "(order=current_order, type=new_item_type)")
        elif item_type == "SaladType":
            new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")
            new_item = eval(item_type[:-4] +
                            "(order=current_order, type=new_item_type)")
        elif item_type == "SubType":
            item_id = request.POST['sub-type']
            size = request.POST['sub-size']
            new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")
            new_item = eval(item_type[:-4] +
                            "(order=current_order, type=new_item_type, size=size)")
            new_item.save()
            selected_addons = request.POST.getlist('sub-toppings')
            for addon_id in selected_addons:
                new_addon = SubTopping.objects.get(pk=addon_id)
                new_item.toppings.add(new_addon)
                new_item.save()
        elif item_type == "PizzaType":
            item_id = request.POST['pizza-type']
            size = request.POST['pizza-size']
            new_item_type = eval(item_type + ".objects.get(pk=" + str(item_id) + ")")
            new_item = eval(item_type[:-4] +
                            "(order=current_order, type=new_item_type, size=size)")
            new_item.save()
            selected_toppings = request.POST.getlist('pizza-toppings')
            for topping_id in selected_toppings:
                new_topping = PizzaTopping.objects.get(pk=topping_id)
                new_item.toppings.add(new_topping)
                new_item.save()

        new_item.calculate_price()
        new_item.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete_item(request, item_type, item_id):
    if request.method == 'POST':
        current_order = Order.objects.get(pk=request.session["current_order"])
        item = eval(item_type + ".objects.get(order=current_order, pk=" + str(item_id) + ")")
        item.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete_order(request):
    if request.method == 'POST':
        current_order = Order.objects.get(pk=request.session["current_order"])
        items = current_order.get_items()
        for item in items:
            item.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def submit_order(request):
    user = User.objects.get(username=request.user.username)
    current_order = Order.objects.get(pk=request.session["current_order"])
    current_order.submitted = True
    current_order.save()
    new_order = Order(user=user)
    new_order.save()
    request.session["current_order"] = new_order.id
    return HttpResponseRedirect(reverse("index"))

@staff_member_required(login_url="login")
def orders(request):
    user = User.objects.get(username=request.user.username)
    context = {
        "username": user.username,
        "submitted_orders": Order.objects.all().filter(submitted=True)
    }
    return render(request, 'orders/orders.html', context)
