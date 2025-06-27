from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # password hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')
        return self.create_user(email, password, **extra_fields)

class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Station(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')  # ✅ নতুন ফিল্ড
    admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_users')  # ✅ এটা থাকতেই হবে

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    EMAIL_FIELD = 'email'  # ✅ এইটা add করুন

    def __str__(self):
        return f"{self.full_name} | {self.role} | {self.email}"

