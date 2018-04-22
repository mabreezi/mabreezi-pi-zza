# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import qrcode
import StringIO

from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

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
	# item_id = models.UUIDField(default=uuid.uuid4, editable=False)
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=300)
	quantity = models.DecimalField(max_digits=6, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

	def get_absolute_url(self):
		return reverse('hyper:item_detail', args=[str(self.id)])

	def generate_qrcode(self):
		qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=6,border=0,)
		qr.add_data(self.get_absolute_url())
		qr.make(fit=True)
		img = qr.make_image()
		file_name = 'item_{}.png'.format(self.id)
		buffer = StringIO.StringIO()
		img.save(buffer)
		file_buffer = InMemoryUploadedFile(buffer, None, file_name, 'image/png', buffer.len, None)
		self.qrcode.save(file_name, file_buffer)


	def __str__(self):
		return '%s#%s' %(self.name, self.id)


class Shipment(models.Model):
	shipment_id = models.UUIDField(default=uuid.uuid4, editable=False)

	def get_absolute_url(self):
		return reverse('hyper:shipment_details', args=[str(self.id)])

	def __str__(self):
		return 'Shipment-{}'.format(self.id)
