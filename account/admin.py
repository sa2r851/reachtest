from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Pharmacy)
admin.site.register(Customer)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Branch)