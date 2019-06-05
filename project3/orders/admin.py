from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(PizzaType)
admin.site.register(PizzaTopping)
admin.site.register(Pizza)
admin.site.register(SubTopping)
admin.site.register(SubType)
admin.site.register(PastaType)
admin.site.register(SaladType)
admin.site.register(PlatterType)
