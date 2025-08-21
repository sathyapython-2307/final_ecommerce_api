from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	image = models.ImageField(upload_to='products/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	)
	user = models.ForeignKey(get_user_model(), related_name='orders', on_delete=models.CASCADE)
	products = models.ManyToManyField(Product, through='OrderItem')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"
