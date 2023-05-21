from django.urls import path
from . import api
app_name='account'
urlpatterns = [
    #create account
    path('register_ph/', api.PharmacyRegistration.as_view(), name='Register-Pharmacy'),
    path('register_customer/', api.CustomerRegistration.as_view(), name='Register-Customer'),
    path("branch_cities/<int:branch>",api.branch_cities,name='cities of branch'),
    path("branch_staff/",api.branch_staff,name='staff branch'),
    path("allcities/",api.Cities,name='all cities'),
    path("allcities/<int:city>",api.city_customer,name='Customers of city'),
]
