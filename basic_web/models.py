from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from django.utils.html import escape, mark_safe
from django.utils import timezone
from datetime import datetime
import math
    
# from .models import Customer, User, Temp_car

# 收费方案： 十元/h, 50/day
# 储值一千九折（0.9），三千7折（0.7）


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    email=models.CharField(max_length=100)
    class Meta:
        swappable = "AUTH_USER_MODEL"


class PLot(models.Model):
    total_space = models.IntegerField(default=10)
    used_space = models.IntegerField(default=0)
    # num_customer = models.IntegerField(default=0)
    def avai_space(self):
        return self.total_space - self.used_space

    # objects = models.Manager()
    def __str__(self):
        return self.used_space
    


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    plate = models.CharField(unique=True, max_length=100)
    balance = models.IntegerField(default=0)
    # 8 or 7, discount devide by 10 when using
    discount = models.IntegerField(default=10)
    # autogenerate by timesttamp
    card_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    reg_date = models.DateTimeField(null=False)
    comment = models.TextField(null=True, max_length=5000, blank=True)
    # objects = models.Manager()
    def __str__(self):
        return self.full_name


class Temp_car(models.Model):
    is_payed = models.BooleanField(default=False)
    plate = models.CharField(max_length=100,unique=True)
    # 在temp_car新建时插入
    # card = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    enter_time = models.DateTimeField(null=False)
    card_number=models.CharField(max_length=100,null=True)

    # objects = models.Manager()
    def __str__(self):
        return self.plate


class Temp_car_history(models.Model):

    is_payed = models.BooleanField(default=True)
    plate = models.CharField(max_length=100)
    # 在temp_car新建时插入
    # card = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    enter_time = models.DateTimeField(null=False)
    exit_time = models.DateTimeField(null=False)
    time_spent = models.IntegerField()
    total_cost = models.IntegerField()
    card_number=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.plate
    
class Slot(models.Model):
    idn = models.IntegerField(default=10)
    is_free = models.BooleanField(default=True)

    # def __str__(self):
    #     return str(self.idn)



