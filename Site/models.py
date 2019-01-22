from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Service(models.Model):
    mileage_number = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Przebieg")
    cash_float = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Kwota")
    note_text = models.CharField(max_length=256, blank=True, null=True, verbose_name="Notatka")
    title_text = models.CharField(max_length=32, verbose_name="Tytuł")
    created_date = models.DateField(default=timezone.now, verbose_name="Data")

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title_text} - {self.cash_float} zł"


class Fueling(models.Model):
    mileage_number = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="Przebieg")
    cash_float = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Kwota")
    liters_float = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Litry")
    created_date = models.DateField(default=timezone.now, verbose_name="Data")

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.created_date} - {self.cash_float} zł"


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark_text = models.CharField(max_length=32, null=False, default='', verbose_name="Marka")
    model_text = models.CharField(max_length=32, null=False, default='', verbose_name="Model")
    vin_text = models.CharField(max_length=17, null=True, verbose_name="Numer VIN")
    plate_text = models.CharField(max_length=10, null=True, verbose_name="Rejestracja")
    engine_float = models.DecimalField(max_digits=8, decimal_places=0, null=True, verbose_name="Poj. silnika")
    services = models.ManyToManyField(Service)
    refueling = models.ManyToManyField(Fueling)
    created_date = models.DateField(default=timezone.now, verbose_name="Data")

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.mark_text} {self.model_text}"
