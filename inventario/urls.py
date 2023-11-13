"""
URL configuration for inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from login import views as views_login
from articulos import views as views_articulos
from categorias import views as views_categorias


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views_login.login_page, name="login"),
    path('home/', views_login.home_page, name="home"),
    path('logout/', views_login.logout_view, name="logout"),
    path("__reload__/", include("django_browser_reload.urls")),
    path('products/', views_articulos.products_page, name="products"),
    path('addProduct/', views_articulos.productsEntry_page,
         name="addProduct"),
    path('users/', views_login.users_view, name="users"),
    path('delete_user/<str:user_rut>',
         views_login.deleteUser, name='deleteUser'),
    path('delete_product/<str:idarticulo>',
         views_articulos.deleteProduct, name='deleteProduct'),
    path('addUser/', views_login.usersEntry_page, name="addUser"),
    path('updateUser/<str:user_rut>',
         views_login.updateUser, name="updateUser"),
    path('updateProduct/<str:idarticulo>',
         views_articulos.updateProduct, name='updateProduct'),
    path('searchProducts/',
         views_articulos.searchProduct, name="searchProduct"),
    path('categories/', views_categorias.categories, name="categories"),
    path('addCategory/', views_categorias.addCategory, name="addCategory"),
    path('deleteCategory/<str:idcategoria>',
         views_categorias.deleteCategory, name="deleteCategory"),
    path('updateCategory/<str:idcategoria>',
         views_categorias.updateCategory, name="updateCategory"),

]
