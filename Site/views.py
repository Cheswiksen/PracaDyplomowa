from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.views.generic.base import View
from .models import Car, Service, Fueling
from django.contrib.auth.models import User


# from main_app.tasks import add


def index(request):
    context = {
        "Cars": Car.objects.all(),
        "Services": Service.objects.all()
    }
    return render(request, 'Site/index.html', context)


def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form' : form}
    return render(request, 'registration/register.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def CarView(request, Car_id):
    try:
        car = Car.objects.get(pk=Car_id)
    except Car.DoesNotExist:
        raise Http404("no car!")
    context = {
        "car": car,
        #"Services": Car.services()
    }
    return render(request, "Site/car.html", context)


def ServiceView(request, Service_id):
    try:
        service = Service.objects.get(pk=Service_id)
    except Service.DoesNotExist:
        raise Http404("no service!")
    context = {
        "Service": service,
    }
    return render(request, "Site/service.html", context)

def FuelView(request, Fuel_id):
    try:
        fuel = Fueling.objects.get(pk=Fuel_id)
    except Service.DoesNotExist:
        raise Http404("no service!")
    context = {
        "Fuel": fuel,
    }
    return render(request, "Site/fuel.html", context)


def car(request):
        context = {
            "Services": Service.objects.all()
        }
        return render(request, 'Site/car.html', context)


