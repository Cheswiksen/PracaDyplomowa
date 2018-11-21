from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Service(models.Model):
    mileage_number = models.DecimalField(max_digits=8, decimal_places=0)
    cash_float = models.DecimalField(max_digits=6, decimal_places=2)
    note_text = models.CharField(max_length=256, null=True)
    title_text = models.CharField(max_length=32)
    created_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title_text}"


class Fueling(models.Model):
    mileage_number = models.DecimalField(max_digits=8, decimal_places=0)
    cash_float = models.DecimalField(max_digits=6, decimal_places=2)
    liters_float = models.DecimalField(max_digits=6, decimal_places=2)
    created_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.cash_float} zł"


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark_text = models.CharField(max_length=32, null=False, default='mark')
    model_text = models.CharField(max_length=32, null=False, default='model')
    services = models.ManyToManyField(Service)
    refueling = models.ManyToManyField(Fueling)

    def __str__(self):
        return f"{self.mark_text} {self.model_text}"
