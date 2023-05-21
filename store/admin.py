from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Company)
admin.site.register(Section)
admin.site.register(SubSection)
admin.site.register(Item)

admin.site.register(Prescription)
admin.site.register(Cart)
admin.site.register(OrderItems)

admin.site.register(Order)
admin.site.register(CartItems)
