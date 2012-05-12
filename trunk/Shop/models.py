import datetime
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

