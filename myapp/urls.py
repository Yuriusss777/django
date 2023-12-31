from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_client, name='create_client'),
    path('create_client', views.create_client, name='create_client'),
    path('clients/<int:client_id>/update/', views.update_client, name='update_client'),
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    path('clients/', views.client_list, name='client_list'),

    # Пути для модели "Товар"
    path('create_product', views.create_product, name='create_product'),
    path('products/<int:product_id>/update/', views.update_product, name='update_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Пути для модели "Заказ"
    path('create_order', views.create_order, name='create_order'),
    path('orders/<int:order_id>/update/', views.update_order, name='update_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_products', views.OrderProductListView.as_view(), name='order_product_list'),

    path('clients/<int:client_id>/orders/', views.client_orders, name='client_orders'),
    path('order', views.orders, name='orders'),
    path('client/<int:client_id>/ordered-products/<str:period>/', views.client_ordered_products,
         name='client_ordered_products'),
]
