from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.views.generic.base import View
from .models import Car, Service, Fueling
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from main_app.tasks import add
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import render_to_pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings

from weasyprint import HTML, CSS


@csrf_exempt
def index(request):
    context = {
        "Cars": Car.objects.all(),
        "Services": Service.objects.all()
    }
    return render(request, 'Site/index.html', context)


@csrf_exempt
def register(request):
    if request.method == 'POST':
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
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


@csrf_exempt
def CarView(request, Car_id):
    try:
        car = Car.objects.get(pk=Car_id)
    except Car.DoesNotExist:
        raise Http404("no car!")
    context = {
        "car": car,
        # "Services": Car.services()
    }
    return render(request, "Site/car.html", context)


@csrf_exempt
def ServiceView(request, Service_id, Car_id):
    try:
        service = Service.objects.get(pk=Service_id)
        car = Car.objects.get(pk=Car_id)
    except Service.DoesNotExist:
        raise Http404("no service!")
    context = {
        "Service": service,
        "Car": car,
    }
    return render(request, "Site/service.html", context)


@csrf_exempt
def FuelView(request, Fuel_id, Car_id):
    try:
        fuel = Fueling.objects.get(pk=Fuel_id)
        car = Car.objects.get(pk=Car_id)
    except Service.DoesNotExist:
        raise Http404("no fueling!")
    context = {
        "Fuel": fuel,
        "Car": car,
    }
    return render(request, "Site/fuel.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteCar(DeleteView):
    template_name = 'Site/car_confirm_delete.html'
    success_url = "/"

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("Car_id")
        return get_object_or_404(Car, id=id_)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFueling(DeleteView):
    template_name = 'Site/fueling_confirm_delete.html'
    success_url = "/"

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("Fuel_id")
        return get_object_or_404(Fueling, id=id_)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteService(DeleteView):
    template_name = 'Site/service_confirm_delete.html'
    success_url = "/"

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("Service_id")
        return get_object_or_404(Service, id=id_)


@csrf_exempt
def car(request):
    context = {
        "Services": Service.objects.all(),
        "Cars": Car.objects.all(),
    }
    return render(request, 'Site/car.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class CarEntry(CreateView):
    model = Car
    success_url = "/"
    template_name = "Site/add_car.html"
    fields = [
        'mark_text',
        'model_text',
        'vin_text',
        'plate_text',
        'engine_float',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CarEntry, self).form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
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

    def get_form(self):
        form = super().get_form()
        form.fields['created_date'].widget = DatePickerInput(format='%Y-%m-%d')
        return form

    def form_valid(self, form):
        service = form.save()
        car = Car.objects.get(pk=self.kwargs['Car_id'])
        service.car_set.add(car)
        return redirect(self.success_url)


@method_decorator(csrf_exempt, name='dispatch')
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

    def get_form(self):
        form = super().get_form()
        form.fields['created_date'].widget = DatePickerInput(format='%Y-%m-%d')
        return form

    def form_valid(self, form):
        fuel = form.save()
        car = Car.objects.get(pk=self.kwargs['Car_id'])
        fuel.car_set.add(car)
        return redirect(self.success_url)


def generate_pdf(request, Car_id):
    """Generate pdf."""
    # Model data
    car = Car.objects.get(pk=Car_id)
    services = car.services.all()
    context = {
        "car": car,
        "services": services,
    }
    # Rendered
    html_string = render_to_string('PDFreport.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


@csrf_exempt
def report(request, Car_id):
    try:
        procentT = 0
        procentS = 0
        i = 0
        q = 0
        srednia_spalania = 0
        srednia_cena = 0
        suma = 0
        sumaT = 0
        sumaS = 0
        litry = 0
        car = Car.objects.get(pk=Car_id)
        for n in car.services.iterator():
            suma = suma + n.cash_float
        sumaS = suma
        for n in car.refueling.iterator():
            q = q + 1
            if i == 0:
                przebieg1 = n.mileage_number
                i = i + 1
            przebieg2 = n.mileage_number
            litry = litry + n.liters_float
            suma = suma + n.cash_float
            srednia_cena = srednia_cena + (n.cash_float / n.liters_float)
        if q != 0:
            srednia_cena = srednia_cena / q
            srednia_cena = round(srednia_cena, 2)
            if (przebieg1 - przebieg2) != 0:
                srednia_spalania = (litry / (przebieg1 - przebieg2)) * 100
                srednia_spalania = round(srednia_spalania, 2)
        sumaT = suma - sumaS
        procentT = sumaT
        procentS = sumaS
    except Car.DoesNotExist:
        raise Http404("no car!")
    context = {
        "car": car,
        "suma": suma,
        "tankowania": sumaT,
        "serwisy": sumaS,
        "srednia": srednia_spalania,
        "procentT": procentT,
        "procentS": procentS,
        "cena": srednia_cena,
    }
    return render(request, 'Site/report.html', context)
