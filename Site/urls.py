from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('car/<int:Car_id>/', views.CarView, name="car"),
    path('car/<int:Car_id>/services/<int:Service_id>/', views.ServiceView, name="service"),
    path('car/<int:Car_id>/fuel/<int:Fuel_id>/', views.FuelView, name="fuel"),
    path('add_car/', views.CarEntry.as_view(), name="add_car"),
    path('car/<int:Car_id>/add_service', views.ServiceEntry.as_view(), name="add_service"),
    path('car/<int:Car_id>/add_fueling', views.FuelingEntry.as_view(), name="add_fueling"),
    path("car/<int:Car_id>/delete", views.DeleteCar.as_view(), name="delete_car"),
    path('car/<int:Car_id>/fuel/<int:Fuel_id>/delete', views.DeleteFueling.as_view(), name="delete_fueling"),
    path('car/<int:Car_id>/services/<int:Service_id>/delete', views.DeleteService.as_view(), name="delete_service"),
    path("car/<int:Car_id>/report", views.report, name="report"),
    path("car/<int:Car_id>/book.pdf", views.generate_pdf, name="pdf"),
]
