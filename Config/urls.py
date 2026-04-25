"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from products import views as product_views
from orders import views as orders_views
from order_items import views as order_items_views
from payments import views as payments_views
from stock_movements import views as stock_movements_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # USERS
    path('users/', user_views.get_users),
    path('users/<int:pk>/', user_views.get_user),
    path('users/create/', user_views.create_user),
    path('users/update/<int:pk>/', user_views.update_user),
    path('users/delete/<int:pk>/', user_views.delete_user), 

    # PRODUCTS get_products_by_seller
    path('products/', product_views.get_products),
    path('products/create/', product_views.create_product),
    path('products/update/<int:pk>/', product_views.update_product),
    path('products/delete/<int:pk>/', product_views.delete_product),

    # Orders
    path('orders/' , orders_views.get_data),
    path('orders/<int:pk>/' , orders_views.get_orders),
    path('orders/create/' , orders_views.create_order),
    path('orders/update/<int:pk>/' , orders_views.update_order),     
    path('orders/delete/<int:pk>/' , orders_views.delete_order),


    #Order_items
    path('order_items/' , order_items_views.get_order_items),
    path('order_items/<int:pk>/' , order_items_views.get_order_item),
    path('order_items/create/' , order_items_views.create_order_item),
    path('order_items/update/<int:pk>/' , order_items_views.update_order_item),
    path('order_items/delete/<int:pk>/' , order_items_views.delete_order_item),

    #Payments
    path('payments/' , payments_views.get_payments),    
    path('payments/<int:pk>/' , payments_views.get_payment),
    path('payments/create/' , payments_views.create_payment),
    path('payments/update/<int:pk>/' , payments_views.update_payment),
    path('payments/delete/<int:pk>/' , payments_views.delete_payment),


    #stock_movements
    path('stock_movements/' , stock_movements_views.get_stock_movements),
    path('stock_movements/<int:pk>/' , stock_movements_views.get_stock_movement),
    path('stock_movements/create/' , stock_movements_views.create_stock_movement),
    path('stock_movements/update/<int:pk>/' , stock_movements_views.update_stock_movement),
    path('stock_movements/delete/<int:pk>/' , stock_movements_views.delete_stock_movement), 
]