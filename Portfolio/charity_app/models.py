from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Institution(models.Model):
    INSTITUTION_CHOICES = [
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
]

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_CHOICES, default=1)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateTimeField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
