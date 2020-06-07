from django.urls import path
from .views import get_token, search_doc

urlpatterns = [
    path('', get_token, name='get_token'),
    path('search/', search_doc, name='search'),
    # path('paper/<paper_pk>/', get_paper, name='get_paper'),
    # path('person/<cltId>/', get_person, name='get_person'),
    # path('car/<carId>/', get_car, name='get_car'),
    # path('car_licence/', get_car_licence, name='car_licence'),
    # path('sprlics/', get_sprlics, name='get_sprlics'),
    # path('vin/<vin_number>/', get_vin, name='get_vin'),
]