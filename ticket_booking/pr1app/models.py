from django.db import models


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()

    def __str__(self):
        return self.name

class Packages(models.Model):
    Packages_date=models.CharField(max_length=250)
    Packages_name=models.CharField(max_length=250)
    Packages_price=models.CharField(max_length=250)
    Packages_desc=models.TextField()
    Packages_img=models.ImageField(upload_to='pics')

    def __str__(self):
        return self.Packages_name