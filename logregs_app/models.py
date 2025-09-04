from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(name=name, email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password=None):
        user = self.create_user(name, email, phone, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

class Title(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_admin': True})
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.ForeignKey('CustomTitle', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.title.name} - ₹{self.amount}"


class CustomTitle(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_admin': True})
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

