from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from django.views import View

app_name= 'shop'

urlpatterns=[
    # path('', views.product_list, name='product_list'),
    # path('search/', views.post_search, name='post_search'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]