from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('profile/', views.profile, name='profile'),
    path('update_product/<int:pid>/', views.update_product, name='update_product'),
    path('forgot/', views.forgot_cutomer_password, name='forgot_customer_password'),
    path('reset_password/', views.reset_customer_password, name='reset_password'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('address_management/', views.address_management, name='address_management'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/', views.delete_address, name="delete_address"),
    path('order-summary/',views.order_summary_view, name='order_summary'),
    path('select-address/', views.select_address_view, name='select_address'),
    path('payment/', views.payment_view, name='payment'),
    path('place-order/',views.place_order_view, name='place_order'),
    path('buy-now/', views.buy_now, name='buy_now'),
   path('order/<int:order_id>/', views.order_detail_view, name='order_detail_view'),
    path('confirm-order/<int:order_id>/',views.confirm_order_view, name='confirm_order_view'),
    path('cancel-order/<int:order_id>/', views.cancel_order_view, name='cancel_order_view'),
]
