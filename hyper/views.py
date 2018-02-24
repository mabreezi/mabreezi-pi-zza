# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import PersonForm, ItemForm, TransactionForm, TradeForm
from .models import Person, Item
from django.http import HttpResponse

import requests
import os

# HYPER_SERVER = os.environ['HYPER_SERVER']
HYPER_SERVER='40.121.193.68'

#View that creates a new person.participant
def add_person(request):
	if request.method == 'POST':
		form = PersonForm(request.POST)

		if form.is_valid():
			new_person = form.save()
			data=  {
    			"$class": "org.kibaati.Person",
    			"personId": new_person.id,
    			"firstName": new_person.first_name,
    			"lastName": new_person.last_name,
    			"role": new_person.role,
    			"balance": 0
  				}

  			# Post the new person to the blockcahin network
  			r = requests.post('http://{}/api/Person'.format(HYPER_SERVER), data=data)

  			return HttpResponse('%s: Person added successfully' % r.status_code)

	else:
		form = PersonForm()
		section_name ="Add a Person"

	return render(request, 'hyper/add_person.html', {'form':form, 'section_name':section_name} ) 

# view that creates an item before it can be traded
def add_item(request):
	if request.method == 'POST':
		form = ItemForm(request.POST)

		if form.is_valid():
			new_item = form.save()

			data =   {
    			"$class": "org.kibaati.Item",
    			"itemName": new_item.name,
    			"itemId": new_item.id,
    			"description": new_item.description,
    			"quantity": new_item.quantity,
    			"owner": "resource:org.kibaati.Person#" + str(new_item.owner.id)
  				}
  			# Post the new Item to the blockchain network
  			r= requests.post('http://{}}/api/Item'.format(HYPER_SERVER), data=data)

  			return HttpResponse('%s: Item added successfully' % r.status_code)

	else:
		form = ItemForm()
		section_name ="Add an Item"

	return render(request, 'hyper/add_item.html', {'form':form, 'section_name':section_name} )

#view that transfers money from one person to another
def submit_transaction(request):
	if request.method=='POST':
		form = TransactionForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			sender = cd['sender']
			recipient = cd['recipient']
			amount = cd['amount']

			data = {
    			"$class": "org.kibaati.Payment",
    			"amount": amount,
    			"sender":"resource:org.kibaati.Person#" + str(sender),
    			"recipient": "resource:org.kibaati.Person#" + str(recipient),
    			}


    		r= requests.post('http://{}/api/Payment'.format(HYPER_SERVER), data=data)
    		
    		return HttpResponse('%s: Payment submitted successfully' % r.status_code)

	else:
		form = TransactionForm()
		section_name ="Submit a Transaction"

	return render(request, 'hyper/submit_transaction.html',{'form':form, 'section_name':section_name})

#view that transfers an item from one person to another
def make_trade(request):
	if request.method=='POST':
		form = TradeForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			sender = cd['sender']
			recipient = cd['recipient']
			item = cd['recipient']

			data = {
    			"$class": "org.kibaati.Payment",
    			"item": "resource:org.kibaati.Item#" + str(item),
    			"newOwner": "resource:org.kibaati.Person#" + str(recipient),
    			}

    		r= requests.post('http://{}/api/Payment'.format(HYPER_SERVER), data=data)
    		
    		return HttpResponse('%s: Trade submitted successfully' % r.status_code)

	else:
		form = TradeForm()
		section_name = "Make a Trade"

	return render(request, 'hyper/make_trade.html', {'form':form, 'section_name':section_name})


#View that crates a new person.participant
def participants(request):
	if request.method == 'POST':
		# form = PersonForm(request.POST)

		# if form.is_valid():
		# 	new_person = form.save()
		# 	data=  {
    	# 		"$class": "org.kibaati.Person",
    	# 		"personId": new_person.id,
    	# 		"firstName": new_person.first_name,
    	# 		"lastName": new_person.last_name,
    	# 		"role": new_person.role,
    	# 		"balance": 0
  		# 		}

  			# Post the new person to the blockcahin network
  			# r = requests.post('http://{}/api/Person'.format(HYPER_SERVER), data=data)

  			# return r.status_code
			return (request, 'hyper/particpants.html')

	else:
		form = PersonForm()
		section_name ="Participants"
		r = requests.get('http://{}/api/Person'.format(HYPER_SERVER))
		# people = Person.objects.all()
		people = r.json()

	return render(request, 'hyper/participants.html', {'form':form,'section_name':section_name, 'persons':people} )




