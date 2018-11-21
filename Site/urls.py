from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('car/<int:Car_id>/', views.CarView, name="car"),
    path('serv/<int:Service_id>/', views.ServiceView, name="service"),
    path('fuel/<int:Fuel_id>/', views.FuelView, name="fuel"),
]