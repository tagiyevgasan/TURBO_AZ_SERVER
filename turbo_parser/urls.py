from django.urls import path
from . import views

app_name = 'turbo_parser'

urlpatterns = [
    path('orders/', views.orders, name='orders'),
    path('orders/id=<int:id>/', views.order_details, name='order_details'),
    path('orders/add_order/', views.add_order, name='add_order'),
    path('orders/delete=<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/edit=<int:order_id>/', views.edit_order, name='edit_order'),
    path('profile/', views.profile, name='profile'),

]