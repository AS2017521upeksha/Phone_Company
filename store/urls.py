from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('',views.storehome, name='storehome'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('reviews',views.reviews, name='reviews'),
    path('shop',views.shop, name='shop'),
    path('shop/<str:category>/', views.shop, name='shop'),

    path('add_category/', views.create_category, name='create_category'),
    path('categories/', views.get_categories, name='get_categories'),
    path('category/<int:category_id>/', views.get_category, name='get_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),

    path('products/', views.products, name='products'),
    path('add_product/', views.create_product, name='create_products'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), 
    path('view_cart/update-purchase/', views.update_purchase, name='update_purchase'),

    path('create_order/', views.create_order, name='create_order'),
    path('create_order/<int:orderid>/', views.create_order, name='create_order_with_id'),
    
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order_list', views.order_list, name='order_list'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),




]
urlpatterns += staticfiles_urlpatterns()
 