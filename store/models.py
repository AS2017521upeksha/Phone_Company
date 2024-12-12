
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=10)

	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'categories'


# Profile model to store extra details of Customers
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)
	image = models.ImageField(upload_to='uploads/profiles/' , default='uploads/profiles/avatar1.png')

	def __str__(self):
		return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)


# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	# description = models.CharField(max_length=250, default='', blank=True, null=True)
	# more_info = models.TextField(max_length=1000, default='', blank=True, null=True)
	# # Add Sale Stuff
	# is_sale = models.BooleanField(default=False)
	# sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	
	def __str__(self):
		return self.name


# Customer Orders
class Order(models.Model):
	product = models.ManyToManyField(Product, through='OrderProduct')
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.CharField(
    max_length=20, 
    choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('delivered', 'delivered'),('deleted','Deleted')],
    default='unpaid'
	)
	total = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	pay_refrence = models.CharField(max_length=50, default='', blank=True)
	dilivery_ref = models.CharField(max_length=50, default='', blank=True)

	def __str__(self):
		return str(self.id)

# OrderProdct 
class OrderProduct(models.Model):
	product= models.ForeignKey(Product,on_delete=models.CASCADE)
	order= models.ForeignKey(Order,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	soldprice= models.DecimalField(default=0, decimal_places=2, max_digits=6)
	
	def __str__(self):
		return "{}_{}".format(self.order.__str__(), self.product.__str__())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    purchase= models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

