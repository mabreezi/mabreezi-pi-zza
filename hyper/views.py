
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .forms import PersonForm, ItemForm, TransactionForm, TradeForm, ShipmentForm
from .models import Person, Item, Shipment
from django.http import HttpResponse
from django.conf import settings
from account.forms import ActivateAccountForm
from django.contrib.auth.models import User

import requests
import os
import sys

def add_item(request):
	section_name = 'Item'
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
  			#r= requests.post('http://{}/api/Item'.format(settings.BLOCKCHAIN_URL), data=data, cookies =cookies)

  			#return HttpResponse('%s: Item added successfully' % r.status_code)

			cookies = request.COOKIES
			print 'First'
  			# Post the new Item to the blockchain network
			try:
  				r= requests.post('http://{}/api/Item'.format(settings.BLOCKCHAIN_URL), data=data, cookies=cookies)
				print r.status_code
				if r.status_code / 100 != 2:
					raise ValueError('Something went wrong')
			except ValueError as error:
				return HttpResponse(r.text)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				return HttpResponse("Unexpected error:", sys.exc_info()[0])
				raise


			print 'Second'
			try:
				r = requests.get('http://{}/api/Item'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
				print r.status_code
				if r.status_code / 100 != 2:
					raise ValueError('Something went wrong')
			except ValueError as error:
				return HttpResponse(r.text)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				return HttpResponse("Unexpected error:", sys.exc_info()[0])
				raise

			print 'Here'


			return render(request, 'hyper/add_item.html', {'form':form, 'section_name':section_name, 'items':r.json() } )


	else:
		form = ItemForm()
		section_name ="Add an Item"
		cookies = request.COOKIES

		try:
			r = requests.get('http://{}/api/Item'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
				return HttpResponse(r.text)
		except:
				print("Unexpected error:", sys.exc_info()[0])
				raise
		items = r.json()
			
		for b,a in enumerate(items):
			owner = a['owner'].split('#')[-1]
			items[b]['owner'] = owner
			# items[b]['owner'] = User.objects.get(pk=int(owner))
			print items[b]['owner']


		return render(request, 'hyper/add_item.html', {'form':form, 'section_name':section_name, 'items':items } )


def get_item_detail(request, item_id):
	cookies = request.COOKIES
	# item = requests.get('http://{}/api/Item'.format(settings.HYPER_SERVER), cookies=cookies)
	item = get_object_or_404(Item, id = item_id)

	return render(request, 'hyper/item_detail.html', {'item':item, 'section_name': 'Item Detail'} )


def add_shipment(request):
	section_name = 'Shipment'
	if request.method == 'POST':
		form = ShipmentForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			items = cd['items']
			start = cd['start_location']
			destination = cd['destination']

			shipment = Shipment()

			data = {
					"$class": "org.kibaati.Shipment",
					"shipmentId": str(shipment.shipment_id),
					"itemList": [items],
					"location": start,
					"locationReadings": [start],
					"destination": destination,
			}

			cookies = request.COOKIES

  			# Post the new Item to the blockchain network
			try:
  				r= requests.post('http://{}/api/Shipment'.format(settings.HYPER_SERVER), data=data, cookies=cookies)
				if r.status_code / 100 != 2:
					raise ValueError('Something went wrong')
			except ValueError as error:
				return HttpResponse(r.text)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				raise
				# return HttpResponse("Unexpected error:", sys.exc_info()[0])

			try:
				r = requests.get('http://{}/api/Item'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
				if r.status_code / 100 != 2:
					raise ValueError('Something went wrong')
			except ValueError as error:
				return HttpResponse(r.text)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				raise
				# return HttpResponse("Unexpected error:", sys.exc_info()[0])

			return render(request, 'hyper/add_shipment.html', {'form':form, 'section_name':section_name } )


	else:
		form = ShipmentForm()
		cookies = request.COOKIES

		try:
			r = requests.get('http://{}/api/Shipment'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
				return HttpResponse(r.text)
		except:
				print("Unexpected error:", sys.exc_info()[0])
				# return HttpResponse("Unexpected error:", sys.exc_info()[0])
				raise

		return render(request, 'hyper/add_shipment.html', {'form':form, 'section_name':section_name, 'shipmentd':r.json() } )
	

def get_shipment_detail(request, shipment_number):
	cookies = request.COOKIES
	# item = requests.get('http://{}/api/Item'.format(settings.HYPER_SERVER), cookies=cookies)
	shipment = get_object_or_404(Shipment, id = shipment_number)
	shipment_id = shipment.shipment_id

	shipment = requests.get('http://{}/api/Shipment/{}'.format(settings.HYPER_SERVER, shipment_id), cookies=cookies)
	shipment = shipment.json()	

	return render(request, 'hyper/shipment_detail.html', {'shipment':shipment, 'section_name': 'Shipment Detail'} )


#view that transfers money from one person to another
def submit_transaction(request):
	if request.method=='POST':
		form = TransactionForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			recipient = cd['recipient']
			amount = cd['amount']

			data = {
    			"$class": "org.kibaati.OrdinaryPayment",
    			"amount": amount,
    			"recipient": "resource:org.kibaati.Person#" + str(recipient),
    			}

		cookies = request.COOKIES

		try:
			r = requests.post('http://{}/api/OrdinaryPayment'.format(settings.BLOCKCHAIN_URL), data=data, cookies=cookies)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
			return HttpResponse(r.text)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			# return HttpResponse("Unexpected error:", sys.exc_info()[0])
			raise

    		return HttpResponse('%s: Payment submitted successfully' % r.status_code)

	else:
		form = TransactionForm()
		section_name ="Submit a Transaction"
		cookies = request.COOKIES
		try:
			r = requests.get('http://{}/api/OrdinaryPayment'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
			return HttpResponse(r.text)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			# return HttpResponse("Unexpected error:", sys.exc_info()[0])
			raise
		
		payments= r.json()

		return render(request, 'hyper/submit_transaction.html',{'form':form, 'section_name':section_name,'payments':payments })



#view that transfers an item from one person to another
def make_trade(request):
	if request.method=='POST':
		form = TradeForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			recipient = cd['recipient']
			item = cd['recipient']

			data = {
    			"$class": "org.kibaati.ItemTransfer",
    			"item": "resource:org.kibaati.Item#" + str(item),
    			"newOwner": "resource:org.kibaati.Person#" + str(recipient),
    			}
		cookies = request.COOKIES

		try:
			r= requests.post('http://{}/api/ItemTransfer'.format(settings.BLOCKCHAIN_URL),cookies =cookies, data=data)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
			return HttpResponse(r.text)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			# return HttpResponse("Unexpected error:", sys.exc_info()[0])
			raise

    		return HttpResponse('%s: Trade submitted successfully' % r.status_code)

	else:
		form = TradeForm()
		section_name = "Make a Trade"
		cookies= request.COOKIES
		try:
			r= requests.get('http://{}/api/ItemTransfer'.format(settings.BLOCKCHAIN_URL),cookies =cookies)
			if r.status_code / 100 != 2:
				raise ValueError('Something went wrong')
		except ValueError as error:
			return HttpResponse(r.text)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			# return HttpResponse("Unexpected error:", sys.exc_info()[0])
			raise
		
		transfers = r.json()

		return render(request, 'hyper/make_trade.html', {'form':form, 'section_name':section_name, 'transfers':transfers})




def dashboard(request):
	# required_cookies = ['access_token','connect.sid', 'user_id']
	cookies = request.COOKIES
	for (key, value) in cookies.items():
		request.session[key] = value
        print cookies.items(), request.session.items()

	try:
		r = requests.get('http://{}/api/wallet'.format(settings.HYPER_SERVER), cookies=cookies)
		if r.status_code / 100 != 2:
			raise ValueError('Something went wrong')
	except ValueError as error:
		return HttpResponse(r.text)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		# return HttpResponse("Unexpected error:", sys.exc_info()[0])
		raise

	wallet = r.json()

	if not wallet:
		return render(request, 'account/enter_token.html', {'section_name':'Import Token', 'form':ActivateAccountForm() } )
	
	return render(request, 'hyper/dashboard.html')
	# return HttpResponse(request.COOKIES.items())

def login_page(request):
	return render(request, 'account/kodhi_login.html')




