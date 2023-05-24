# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import pytz
from django.utils import timezone


class Category(models.Model):
    category = models.TextField(blank=True, null=True, max_length=200)

    def __str__(self) -> str:
        return self.category

    class Meta:
        db_table = 'category'
        verbose_name_plural = "Kategorie"

class Price(models.Model):
    id = models.IntegerField(primary_key=True, default=None)
    price = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.price)

    class Meta:
        db_table = 'price'
        verbose_name_plural = "Cena"

class Products(models.Model):
    product = models.CharField(blank=True, null=True, max_length=200)
    composition = models.CharField(blank=True, null=True, max_length=500)
    allergens = models.CharField(blank=True, null=True, max_length=200)
    price = models.ForeignKey(Price, on_delete=models.SET_NULL,db_column='price', related_name='product_price', null=True, blank=True)
    id_category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column='id_category', blank=True, null=True)
    with_dressing = models.BooleanField(default=False)
    with_drink = models.BooleanField(default=False)
    with_side_dish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.price and not self.price.id:
            self.price.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product

    class Meta:
        db_table = 'products'
        verbose_name_plural = "Produkty"

class Dressing(models.Model):
    dressing = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self) -> str:
        return self.dressing

    class Meta:
        db_table = 'dressing'
        verbose_name_plural = "Dresinky"

class Drink(models.Model):
    drink = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self) -> str:
        return self.drink

    class Meta:
        db_table = 'drink'
        verbose_name_plural = "Nápoje"


class SideDish(models.Model):
    side_dish = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self) -> str:
        return self.side_dish

    class Meta:
        db_table = 'side_dish'
        verbose_name_plural = "Přílohy"


class Customer(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='customers', null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"

    class Meta:
        db_table = 'customer'
        verbose_name_plural = "Zákazníci"

class Delivery(models.Model):
    delivery = models.CharField(blank=True, null=True, max_length=200)
    delivery_price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.delivery

    class Meta:
        db_table = 'delivery'
        verbose_name_plural = "Doručení"

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATING', 'Creating'),
        ('NEW', 'New'),
        ('IN_PROCESS', 'In Process'),
        ('COMPLETED', 'Completed'),
        ('STORNO', 'Storno'),
    ]
    
    date_ordered = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATING')
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_price = models.IntegerField(null=True, blank=True)
    gdpr = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    customer_comment = models.CharField(max_length=1000, blank=True, null=True)
    order_number = models.CharField(max_length=6, null=True, blank=True)
    total_price_order = models.IntegerField(default=None, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.delivery and self.delivery.delivery_price:
            self.delivery_price = self.delivery.delivery_price.price
        if not self.delivery_price:
            self.delivery_price = 0
        super().save(*args, **kwargs)

    @property
    def get_delivery_price(self):
        return int(self.delivery_price) if self.delivery_price else 0    

    def get_local_time(self, *args, **kwargs):
        if not self.pk:
            self.date_ordered = timezone.now().astimezone(pytz.timezone('Europe/Prague')).strftime("%Y-%m-%d %H:%M:%S")
        super().save(*args, **kwargs)

    def set_order_number(self) -> str:
        last_order = Order.objects.all().order_by('order_number').last()
        if last_order is not None:
            last_order_number = last_order.order_number
            if last_order_number is not None:
                last_order_number = int(last_order_number)
                next_order_number = last_order_number + 1
            else:
                next_order_number = 1
        else:
            next_order_number = 1
        self.order_number = str(next_order_number).zfill(6)
        return self.order_number
    
    def __str__(self) -> str:
        return str(self.id)

    @property
    def get_cart_price_total(self):
        cart_items = self.cartitem_set.all()
        total_price = sum([item.get_product_price for item in cart_items])
        return total_price
    
    @property
    def get_cart_price_total_with_delivery(self):
        cart_items = self.cartitem_set.all() 
        delivery_price = self.get_delivery_price
        total_price = sum([item.get_product_price for item in cart_items]) + delivery_price
        return total_price



    @property
    def get_cart_items_total(self):
        cart_items = self.cartitem_set.all()
        total_items = cart_items.count()
        return total_items

    class Meta:
        db_table = 'order'
        verbose_name_plural = "Objednávky"

class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    drink =  models.ForeignKey(Drink, on_delete=models.SET_NULL, db_column='drink', blank=True, null=True)
    side_dish =  models.ForeignKey(SideDish, on_delete=models.SET_NULL, db_column='side_dish', blank=True, null=True)
    dressing =  models.ForeignKey(Dressing, on_delete=models.SET_NULL, db_column='dressing', blank=True, null=True)
    price = models.IntegerField(default=None)  

    def save(self, *args, **kwargs):
        if not self.id:  
            self.price = self.product.price.price 
        super().save(*args, **kwargs)

    @property
    def get_product_price(self):
        return self.price 

    class Meta:
        db_table = 'cart_item'
        verbose_name_plural = "Košík"

class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='delivery_addresses')
    street = models.CharField(max_length=80, null=False, blank=True)
    city = models.CharField(max_length=50, null=False, blank=True)
    zipcode = models.CharField(max_length=6, null=False, blank=True)

    def __str__(self) -> str:
        return f"Ulice: {self.street} - Město: {self.city} - PSČ: {self.zipcode}"

    class Meta:
        db_table = 'delivery_address'
        verbose_name_plural = "Doručovací adresa"