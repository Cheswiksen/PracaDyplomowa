from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.views.generic.base import View
from .models import Car, Service, Fueling
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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


def ServiceView(request, Service_id, Car_id):
    try:
        service = Service.objects.get(pk=Service_id)
    except Service.DoesNotExist:
        raise Http404("no service!")
    context = {
        "Service": service,
    }
    return render(request, "Site/service.html", context)


def FuelView(request, Fuel_id, Car_id):
    try:
        fuel = Fueling.objects.get(pk=Fuel_id)
    except Service.DoesNotExist:
        raise Http404("no fueling!")
    context = {
        "Fuel": fuel,
    }
    return render(request, "Site/fuel.html", context)


class DeleteFueling(DeleteView):
    model = Fueling
    success_url = "/"

    def form_valid(self, form):
        serv = Service.objects.get(pk=self.kwargs['Service_id'])
        serv.delete()
        return redirect(self.success_url)


def DeleteCar(request, pk):
    template = 'Site/service_confirm_delete.html'
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return render(template)

def car(request):
        context = {
            "Services": Service.objects.all(),
            "Cars": Car.objects.all(),
        }
        return render(request, 'Site/car.html', context)


class CarEntry(CreateView):
    model = Car
    success_url = "/"
    template_name = "Site/add_car.html"
    fields = [
        'mark_text',
        'model_text',
        'services',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CarEntry, self).form_valid(form)


class ServiceEntry(CreateView):
    model = Service
    success_url = "/"
    template_name = "Site/add_service.html"
    fields = [
        'mileage_number',
        'cash_float',
        'note_text',
        'title_text',
        'created_date',
    ]

    def form_valid(self, form):
        service = form.save()
        car = Car.objects.get(pk=self.kwargs['Car_id'])
        service.car_set.add(car)
        return redirect(self.success_url)


class FuelingEntry(CreateView):
    model = Fueling
    success_url = "/"
    template_name = "Site/add_fueling.html"
    fields = [
        'mileage_number',
        'cash_float',
        'liters_float',
        'created_date',
    ]

    def form_valid(self, form):
        fuel = form.save()
        car = Car.objects.get(pk=self.kwargs['Car_id'])
        fuel.car_set.add(car)
        return redirect(self.success_url)
