from django.contrib import admin
from . models import Admin_register,Category,Product


admin.site.register(Admin_register)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name','des')

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','price','category','des','image')

admin.site.register(Product,ProductAdmin)