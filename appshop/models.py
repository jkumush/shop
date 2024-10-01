from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from django.db.models.signals import post_save
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver





class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='category', null=True)
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('category', args=[self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/def.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    GENDER_CHOICES = [
        ('men', "Men's"),
        ('women', "Women's"),
        ('baby', "Baby's"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='product')
    image1 = models.ImageField(upload_to='product', null=True)
    image2 = models.ImageField(upload_to='product', null=True)
    description = models.TextField()
    bigdescription = models.TextField(null=True)
    info = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sizes = models.ManyToManyField(Size, blank=True)
    color = models.CharField(max_length=50)
    color1 = models.CharField(max_length=50, null=True, blank=True)
    color2 = models.CharField(max_length=50, null=True, blank=True)
    color3 = models.CharField(max_length=50, null=True, blank=True)
    color4 = models.CharField(max_length=50, null=True, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', args=[self.slug])
    
    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])
    
    def decrease_stock(self, quantity):
        self.stock -= quantity
        self.save()

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()
    
    def delete_if_no_stock(self):
        if self.stock <= 0:
            self.delete()

            
@receiver(post_save, sender=Product)
def check_product_stock(sender, instance, **kwargs):
    instance.delete_if_no_stock()

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return self.product.name
    
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
@receiver(post_save, sender=Cart)
def check_product_stock(sender, instance, **kwargs):
    instance.product.delete_if_no_stock()

@receiver(post_delete, sender=Cart)
def check_product_stock_on_delete(sender, instance, **kwargs):
    instance.product.delete_if_no_stock()
    

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"