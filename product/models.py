from django.db import models
import datetime
import random
import os
import math
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField('Name',max_length=200,blank=True)
    description = models.CharField('Description',max_length=10000,blank=True)
    image_url = models.FileField ('Image URL',max_length=200,blank=True,null=True)
    created_on = models.DateTimeField('Date created',auto_now_add=True, blank=True)
    is_active = models.BooleanField('Active',blank=True, default=True)
    price = models.FloatField(blank=True,null=True,default=0.00) ## double DEFAULT NULL,


    def __str__(self):
        return self.name

    # def get_image_url(self):
    #     if self.product_image_url.name:
    #         return self.product_image_url.url
    #     else:
    #         return "/media/placeholder.png" 