from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Consumer(AbstractUser):
	username		= models.CharField(max_length=30,unique=True)
	password		= models.CharField(max_length=100)
	email			= models.EmailField(unique=True)
	first_name 		= models.CharField(max_length=30)
	last_name 		= models.CharField(max_length=30)
	date_of_birth 	= models.DateField(null=True,blank=True)

	

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class Category(models.Model) :
	name			= models.CharField(max_length=30,unique=True)
	
	class Meta:
		verbose_name = _("category")
		verbose_name_plural = _("categories")

	def __str__(self):
		return self.name




class Product(models.Model) :
	name			= models.CharField(max_length=30)
	price			= models.FloatField(default=0)
	description		= models.CharField(max_length=255)
	category		= models.ForeignKey(Category,on_delete=models.CASCADE)
	digital			= models.BooleanField(default=False,null=True,blank=False)
	image			= models.ImageField(null=True,blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''

		return url
	

class Order(models.Model) :
	consumer		= models.ForeignKey(Consumer,on_delete=models.SET_NULL,blank=True,null=True)
	date_ordered	= models.DateTimeField(auto_now_add=True)
	complete		= models.BooleanField(default=False,null=True,blank=False)
	transaction_id	= models.CharField(max_length=200,null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		cart_items = self.orderitem_set.all() 
		total = sum([item.get_total for item in cart_items])
		return total

	@property
	def get_cart_items(self):
		cart_items = self.orderitem_set.all() 
		total = sum([item.quantity for item in cart_items])
		return total


class OrderItem(models.Model) :
	product		= models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
	order 		= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
	quantity 	= models.IntegerField(default=0)
	date_added 	= models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	


class ShippingAddress(models.Model) :
	consumer 	= models.ForeignKey(Consumer,on_delete=models.SET_NULL,blank=True,null=True)
	order 		= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
	address 	= models.CharField(max_length=255,null=True)
	city 		= models.CharField(max_length=255)
	state 		= models.CharField(max_length=255)
	country		= models.CharField(default='India',max_length=25)
	zipcode		= models.IntegerField(null=True)
	date_added 	= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.address + ', ' + self.city + ', ' + self.state + ', ' + self.country+ ', '+ str(self.zipcode)+'.'

class orderSuccess(models.Model) :
	name 		= models.CharField(max_length=255,null=True)
	email 		= models.EmailField(blank=True,null=True)
	consumer 	= models.ForeignKey(Consumer,on_delete=models.SET_NULL,blank=True,null=True)
	order 		= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
	address 	= models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,blank=True,null=True)
	date_added 	= models.DateTimeField(auto_now_add=True)




	def __str__(self):
		return self.name
























