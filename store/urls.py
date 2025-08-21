from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    OrderListCreateView,
    OrderDetailView,
    product_list_view,
    product_detail_view,
    cart_view,
    add_to_cart,
    remove_from_cart,
    checkout,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    # Frontend product views
    path('browse/', product_list_view, name='product-list-view'),
    path('browse/<int:pk>/', product_detail_view, name='product-detail-view'),
    # Cart and checkout
    path('cart/', cart_view, name='cart-view'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout, name='checkout'),
]
