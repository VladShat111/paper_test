from django.urls import path
from .views import get_token, get_paper, get_person, get_car, get_car_licence, get_sprlics, get_vin

urlpatterns = [
    path('', get_token, name='get_token'),
    path('paper/<paper_pk>/', get_paper, name='get_paper'),
    path('person/<cltId>/', get_person, name='get_person'),
    path('car/<carId>/', get_car, name='get_car'),
    path('car_licence/', get_car_licence, name='car_licence'),
    path('sprlics/', get_sprlics, name='get_sprlics'),
    path('vin/<vin_number>/', get_vin, name='get_vin'),
]