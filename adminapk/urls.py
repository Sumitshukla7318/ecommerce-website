from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.admin_panel),
    path('admin_signup',views.admin_signup,name='admin_signup'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('add_product/',views.add_product,name="add_product"),
    path('add_category/',views.add_category,name="add_category"),
    path('view_product/',views.view_product,name='view_product'),
   path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),
   path('editproductt/<int:id>/', views.editproduct, name='editproduct'),
   path('view_customer/',views.view_customer,name='view_customer'),
   path('forgot_password/',views.forgot_password,name="forgot_password"),
   path('reset_password/',views.reset_password,name="reset_password"),
] 
