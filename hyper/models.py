# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid


from django.db import models

# Create your models here.
class Person(models.Model):
	ROLE_CHOICES = [
		('refugee','Refugee'), 
		('vendor','Vendor'), 
		('distributor','Distributor'),
		('implementor','Implementing Partner')]


	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name =models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	role = models.CharField(max_length=20, choices =ROLE_CHOICES)
	balance = models.IntegerField(default=0)
	
	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Item(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=300)
	quantity = models.DecimalField(max_digits=6, decimal_places=2)
	owner = models.ForeignKey('Person', on_delete=models.CASCADE)

	def __str__(self):
		return '%s#%s' %(self.name, self.id)
