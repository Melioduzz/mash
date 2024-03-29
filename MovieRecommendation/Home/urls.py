from django.contrib import admin
from django.urls import path, include
from Home import *
from Home import views
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path("base", views.base, name='base'),
    path("home", views.home, name='home'),
    path("shop", views.shop, name='shop'),
    path("admin_home", views.admin_home, name='admin_home'),

    path("cat_add", views.cat_add, name='cat_add'),
    path("cat_del<int:id>", views.cat_del, name='cat_del'),
    path("all_product_view", views.all_product_view, name='all_product_view'),
    path("user_view", views.user_view, name='user_view'),
    path("user_delete/<int:id>", views.user_delete, name='user_delete'),

    path("shop_filter", views.shop_filter, name='shop_filter'),
    path('product_details_slug/<slug:slug>/', views.product_details, name='product_details'),
    path("product_details/<int:id>", views.product_details, name='product_details'),
    path("user_account", views.user_account, name='user_account'),
    path("user_validate/<username>/<field>", views.user_validate, name='user_validate'),
    path("user_registration", views.user_registration, name='user_registration'),
    path("LogIn", views.LogIn, name='LogIn'),
    path("LogOut", views.LogOut, name='LogOut'),
    path("", views.index, name='index'),
    path("review", views.review, name='review'),
    path("replies<int:id>", views.replies, name='replies'),
    path('profile/', views.profile, name='profile'),
    path('changepass/', views.changepass, name='changepass'),
    path('rating', views.rating, name='rating'),
    path('search', views.search, name='search'),
    path('filter-category', views.filter_category, name='filter_category'),
    # path('admin', views.admin, name='admin'),
    path('favorites', views.favorites, name='favorites'),
    path('fav_view', views.fav_view, name='fav_view'),
    path('delete-favorite/', views.delete_favorite, name='delete_favorite'),
    path('create_product', views.create_product, name='create_product'),
    path('my_product_view', views.my_product_view, name='my_product_view'),
    path('delete_product', views.delete_product, name='delete_product'),
    path('delete_product_all', views.delete_product_all, name='delete_product_all'),
    path('ckeditor/upload/', ckeditor_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),

]
