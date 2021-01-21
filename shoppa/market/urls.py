from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('api/category/', views.category_api, name='category-api'),
    path('cart/', views.cart, name='cart'),
    path('api/cart/', views.cart_api, name='cart-api'),
    path('payment/', views.payment, name='payment'),
    path('api/pay/', views.pay_api, name='pay-api'),
    path('api/search/', views.search_api, name='search-api'),
    path('search/', views.search, name='search'),
    path('account/', views.account, name='account'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('product/<int:product_id>', views.product, name='product'),
    path('api/product/', views.product_api, name='product-api'),
    path('api/register/', views.register_api, name='register-api'),
    path('api/index/', views.index_api, name='index-api'),
    #path('api/index/<int:product_id>', views.index_api, name='index-api-extra'),
    path('login/', views.go_login, name='login'),
    path('logout/', views.go_logout, name='logout'),
]
