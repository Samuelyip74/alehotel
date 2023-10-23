from django.db import models
from django.contrib.auth.models import User
import datetime
import random
import os
import math
from django.conf import settings
from django.urls import reverse
from product.models import Product

# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)    
    created_on = models.DateTimeField('Date created',auto_now_add=True, blank=True)
    start_date = models.DateField('Start date',blank=True)
    end_date = models.DateField('End date',blank=True)
    guest = models.IntegerField('Guest',blank=True, null=True)
    days = models.IntegerField('Days',blank=True,null=True)
    is_active = models.BooleanField('Active',blank=True, default=True)
    price = models.FloatField(blank=True,null=True,default=0.00) ## double DEFAULT NULL,
    room  = models.ForeignKey(Product,null=True, blank=True,on_delete=models.CASCADE,unique=False)
    code = models.CharField('Reservation Code',max_length=200,blank=True)

    def __str__(self):
        return self.user.email
