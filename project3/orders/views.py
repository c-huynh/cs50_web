from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required
def index(request):
    context = {
        "username": request.user.username,
        "pizza_types": PizzaType.objects.all(),
        "pizza_toppings": PizzaTopping.objects.all(),
        "sub_types": SubType.objects.all(),
        "sub_toppings": SubTopping.objects.all(),
        "pastas": PastaType.objects.all(),
        "salads": SaladType.objects.all(),
        "platters": PlatterType.objects.all(),
        "sub": Sub.objects.first()
    }
    return render(request, "orders/index.html", context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('index')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = UserCreationForm()
    context = {"form": form}
    return render(request, "authentication/register.html", context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"logged in as {username}")
                return redirect('index')
            else:
                print(f"invalid username and/or password")
        else:
            print(f"invalid username and/or password")
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "authentication/login.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
