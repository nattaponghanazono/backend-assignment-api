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


urlpatterns = [
    path('admin/', admin.site.urls),

    # USERS
    path('users/', user_views.get_users),
    path('users/<int:pk>/', user_views.get_user),
    path('users/create/', user_views.create_user),

    # PRODUCTS get_products_by_seller
    path('products/', product_views.get_products),
    path('serch/products/<int:pk>', product_views.get_products_by_seller),
]