from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Banner_area(models.Model):
    title = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to="bannertop")
    rating = models.FloatField(default="")
    link = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('Home:products_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    title = models.CharField(max_length=250, default="", null=True)
    poster = models.ImageField(upload_to='product_image')
    description = RichTextField()
    release_date = models.CharField(max_length=20, default="")
    actors = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    youtube = models.CharField(max_length=250, default="", null=True)
    download = models.CharField(max_length=250, default="", null=True)
    tags = models.CharField(max_length=250, default="", null=True)
    slug = models.CharField(max_length=555, default="", null=True, unique=True, blank=True)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=0.0)
    creator = models.IntegerField(max_length=30,blank=True, null=True)



    class Meta:
        ordering = ('title',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('Home:prodCatDetail', args=[self.categories.first().slug, self.slug])

    def __str__(self):
        return '{}'.format(self.title)
class Additional_image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=1000, null=True, blank=True)

from django.utils.text import slugify


@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        counter = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = unique_slug





class Review(models.Model):
    name = models.CharField(max_length=250, default="")
    prod_parent = models.IntegerField(max_length=100, default="")
    review = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.CharField(max_length=250, default="")
    prod_parent = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.user


class Reply(models.Model):
    name = models.CharField(max_length=250, default="")
    review_parent = models.ForeignKey(Review, on_delete=models.CASCADE)
    reply = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.IntegerField(max_length=30,blank=True, null=True)
    product = models.IntegerField(max_length=30, blank=True, null=True)


