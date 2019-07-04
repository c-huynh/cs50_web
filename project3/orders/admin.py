from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(Pasta)
admin.site.register(PastaType)
admin.site.register(Pizza)
admin.site.register(PizzaTopping)
admin.site.register(PizzaType)
admin.site.register(Platter)
admin.site.register(PlatterType)
admin.site.register(Salad)
admin.site.register(SaladType)
admin.site.register(Sub)
admin.site.register(SubTopping)
admin.site.register(SubType)
