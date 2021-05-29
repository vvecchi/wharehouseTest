from django.urls import path

from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('products', views.products, name='products'),
    path('product/<int:product_id>', views.product, name='product'),
    path('remove_product', views.remove_product, name='remove_product'),
    path('upload_inventory', views.upload_inventory, name='upload_inventory'),
    path('upload_inventory_file', views.upload_inventory_file, name='upload_inventory_file'),
    path('upload_products', views.upload_products, name='upload_products'),
    path('upload_products_file', views.upload_products_file, name='upload_products_file'),
]
