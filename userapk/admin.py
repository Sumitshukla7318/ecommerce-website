from django.contrib import admin
from . models import Customer,Cart


class CustomerAdmin(admin.ModelAdmin):
    list_display=('fname','lname','father','email','pass1','Phone','image')

admin.site.register(Customer,CustomerAdmin)

class cartadmin(admin.ModelAdmin):
    list_display=('id','customer','product','quantity')
admin.site.register(Cart,cartadmin)

# Register your models here.
