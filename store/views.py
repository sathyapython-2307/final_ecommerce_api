# ...existing imports...
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import OrderItem
# ...existing code...

# Cart logic using session
def get_cart(request):
	return request.session.setdefault('cart', {})

@login_required
def cart_view(request):
	cart = get_cart(request)
	cart_items = []
	grand_total = 0
	for product_id, quantity in cart.items():
		try:
			product = Product.objects.get(id=product_id)
			total = product.price * quantity
			cart_items.append({'product': product, 'quantity': quantity, 'total': total})
			grand_total += total
		except Product.DoesNotExist:
			continue
	return render(request, 'store/cart.html', {'cart_items': cart_items, 'grand_total': grand_total})

@require_POST
@login_required
def add_to_cart(request, pk):
	cart = get_cart(request)
	cart[str(pk)] = cart.get(str(pk), 0) + 1
	request.session.modified = True
	return redirect('cart-view')

@require_POST
@login_required
def remove_from_cart(request, pk):
	cart = get_cart(request)
	if str(pk) in cart:
		del cart[str(pk)]
		request.session.modified = True
	return redirect('cart-view')

@require_POST
@login_required
def checkout(request):
	cart = get_cart(request)
	if not cart:
		return redirect('cart-view')
	order = Order.objects.create(user=request.user, status='pending', total_price=0)
	total_price = 0
	for product_id, quantity in cart.items():
		product = Product.objects.get(id=product_id)
		item_total = product.price * quantity
		OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
		total_price += item_total
		product.stock = max(product.stock - quantity, 0)
		product.save()
	order.total_price = total_price
	order.save()
	request.session['cart'] = {}
	return redirect('product-list-view')
from django.shortcuts import render, get_object_or_404, redirect
# ...existing code...

# Frontend product list view
def product_list_view(request):
	products = Product.objects.all()
	return render(request, 'store/product_list.html', {'products': products})

# Frontend product detail view
def product_detail_view(request, pk):
	product = get_object_or_404(Product, pk=pk)
	return render(request, 'store/product_detail.html', {'product': product})
from rest_framework import generics, permissions, filters
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filter_backends = [filters.SearchFilter]
	search_fields = ['name']

class ProductListCreateView(generics.ListCreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name', 'description']
	ordering_fields = ['price', 'created_at']

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderListCreateView(generics.ListCreateAPIView):
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user)
