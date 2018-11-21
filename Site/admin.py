from django.contrib import admin
from .models import Fueling, Service, Car

# Register your models here.
admin.site.register(Fueling)
admin.site.register(Service)
admin.site.register(Car)
