from django.db import models
from django.contrib.auth.models import User
import datetime
import random
import os
import math
from django.conf import settings
from django.urls import reverse
from reservation.models import Reservation
from product.models import Product

# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)    
    created_on = models.DateTimeField('Date created',auto_now_add=True, blank=True)
    number = models.IntegerField('Number',blank=True)
    is_active = models.BooleanField('Active',blank=True, default=False)
    room_type  = models.ForeignKey(Product,null=True, blank=True,on_delete=models.CASCADE,unique=False)

    def __str__(self):
        return str(self.number)
