# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):

    ROLE_CHOICES = [
		('refugee','Refugee'), 
		('vendor','Vendor'), 
		('distributor','Distributor'),
		('implementor','Implementing Partner')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # first_name =models.CharField(max_length=200)
    # last_name =models.CharField(max_length=200)
    role =models.CharField(max_length=20, choices =ROLE_CHOICES)
    balance = models.IntegerField(default=0)
    company = models.CharField(max_length=70)


class Refugee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  family = models.CharField(max_length=20, blank=True, default='')
  phone_number = models.CharField(max_length=11, blank=True)
  age = models.IntegerField()
  zone = models.IntegerField()
  village = models.IntegerField()
  alternate = models.CharField(max_length=20, blank=True, default=True)


class Merchant(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=11)
  age = models.IntegerField()
  zone = models.IntegerField(blank=True)
  village = models.IntegerField(blank=True)
  account_number = models.IntegerField(blank=True)

class PartnerUser(models.Model):
  user= models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=11)
  age = models.IntegerField()
  organization = models.CharField(max_length=20)

class Trucker(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=11)





