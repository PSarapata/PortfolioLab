from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import tree
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Institution(models.Model):
    INSTITUTION_CHOICES = [
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
]
    name = models.CharField(max_length=64)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_CHOICES, default=1)

    class Meta:
        def __str__(self) -> str:
            return f"Name: {self.name} <> Categories: {self.categories} <> Description: {self.description} <> Type: {self.type}"


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    """Charity App's custom User model."""
    username = None
    email = models.EmailField(_('email address'), unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Donation(models.Model):
    quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=256, null=True)
    phone_number = models.IntegerField(null=True)
    city = models.CharField(max_length=128, null=True)
    zip_code = models.CharField(max_length=64, null=True)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, on_delete=models.CASCADE)
