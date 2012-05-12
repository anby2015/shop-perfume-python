import datetime
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.urlresolvers import reverse

from django.db import models
from tagging.fields import TagField
from tagging.models import Tag

class Category(models.Model):
    """ The category """
    slug = models.SlugField(max_length=150)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list', kwargs={'slug': self.slug})

class Product(models.Model):
    """ The Product """
    slug = models.SlugField(max_length=150)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name="products")
    createdDate = models.DateTimeField(default=datetime.datetime.now())
    tags = TagField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

class Customer(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=300)
    phone = PhoneNumberField(blank=True)

class Order(models.Model):
    customer = models.ForeignKey(User, blank=True, null=True)
    status_code = models.ForeignKey('StatusCode')
    date_placed = models.DateTimeField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    comments = models.TextField(blank=True)
    products = models.ManyToManyField(Product, through='ProductInOrder')

class StatusCode(models.Model):
    """
    The StatusCode model represents the status of an order in the
    system.
    """
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=300)
    description = models.TextField()

class ProductInOrder(models.Model):
    """
    The ProductInOrder model represents information about a specific
    product ordered by a customer.
    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    comments = models.TextField(blank=True)