# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import uuid
import os

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.conf import settings

from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from .models import Profile, Refugee, Merchant, PartnerUser, Trucker
from .forms import AddUserForm, ProfileForm, RefugeeForm, MerchantForm, PartnerUserForm

# Create your views here.
def create_user(request):
    if request.method == 'POST':
        return HttpResponse('Still in Dev')
        user_form = AddUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            email = user_cd['email']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            profile_cd =profile_form.cleaned_data
            role = profile_cd['role']
            company = profile_cd['company']

            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                email=email, password=get_random_string())

            new_user.save()
            profile = Profile.objects.create(user=new_user, role=role, company=company)

            profile.save()

            personId = uuid.uuid4()

            data=  {
                    "$class": "org.kibaati.Person",
                    "personId": personId,
                    "firstName": first_name,
                    "lastName": last_name,
                    "role": role,
                    "balance": 0
  				}
            
            access_token = 'X1tEvCbMZdrl9toBEPnlaB9WAzvZwijpclgyzD62LQUstuDYC3EpV2PM33MI2G4i'

            params={'access_token':access_token}

            r = requests.post('http://{}/api/Person'.format(settings.HYPER_SERVER), data=data, params=params)

            data = {
                    "participant": "org.kibaati.Person#{}".format(personId),
                    "userID": user_name
                    }
                    
            r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data,params=params)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            card = open(path, 'w')
            card.write(r.content)
            card.close()

            set_password_form = PasswordResetForm({'email':email})
            if set_password_form.is_valid():
                # print 'Reset Form is Valid'
                set_password_form.save(
                    request=request,
                    use_https=False,
                    from_email='bpmusisi@gmail.com',
                    email_template_name='account/activate_account.html'
                )

        return HttpResponse('Password Set Form Sent')

    else:
        user_form = AddUserForm()
        profile_form = ProfileForm()
        return render(request, 'account/add_user_form.html', {'user_form':user_form, 'profile_form':profile_form} )



def add_users(request):
    return render(request, 'account/add_all_users.html', {'section_name': 'Add Users'})



def add_refugee(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        refugee_form = RefugeeForm(request.POST)
        
        if user_form.is_valid() and refugee_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            refugee_cd = refugee_form.cleaned_data
            phone_number = refugee_cd['phone_number']
            age = refugee_cd['age']
            zone = refugee_cd['zone']
            village = refugee_cd['village']
            alternate = refugee_cd['alternate'] 


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                 password=get_random_string())
            
            refugee = Refugee.objects.create(user=new_user, phone_number = phone_number, age = age, zone = zone,
                                            village=village, alternate=alternate)
            refugee.save()

            ######### Send to Blockchain #############

            personId = uuid.uuid4()

            data=  {
                    "$class": "org.kibaati.Person",
                    "personId": personId,
                    "firstName": first_name,
                    "lastName": last_name,
                    "phoneNumber": phone_number,
                    "balance": 0
  				}
            
            access_token = 'X1tEvCbMZdrl9toBEPnlaB9WAzvZwijpclgyzD62LQUstuDYC3EpV2PM33MI2G4i'

            params={'access_token':access_token}

            r = requests.post('http://{}/api/Refugee'.format(settings.HYPER_SERVER), data=data, params=params)

            data = {
                    "participant": "org.kibaati.Refugee#{}".format(refugee),
                    "userID": user_name
                    }
                    
            r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data,params=params)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            card = open(path, 'w')
            card.write(r.content)
            card.close()

        return HttpResponse('Refugee created')
            

        #######################

            

    else:
        refugee_form = RefugeeForm()
        section_name = 'Add A Refugee'
        return render(request, 'account/add_refugee.html', {'section_name': section_name, 'form': refugee_form})


def add_merchant(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        merchant_form = MerchantForm(request.POST)
        
        if user_form.is_valid() and merchant_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            merchant_cd = merchant_form.cleaned_data
            phone_number = merchant_cd['phone_number']
            age = merchant_cd['age']
            zone = merchant_cd['zone']
            village = merchant_cd['village']
            account_number = merchant_cd['account_number'] 


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                 password=get_random_string())
                                                 
            merchant = Merchant.objects.create(user=new_user, phone_number = phone_number, age = age, zone = zone,
                                            village=village, account_number = account_number)
            
            merchant.save()
        
    else:
        merchant_form = MerchantForm()
        section_name = 'Add A Merchant'
        return render(request, 'account/add_merchant.html', {'section_name': section_name, 'form': merchant_form})



def add_partner_user(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        partner_user_form = PartnerUserForm(request.POST)
        
        if user_form.is_valid() and partner_user_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            partner_user_cd = partner_user_form.cleaned_data
            phone_number = partner_user_cd['phone_number']
            age = partner_user_cd['age']
            organization = partner_user_cd['organization']


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                 password=get_random_string())
                                                 
            partner_user = PartnerUser.objects.create(user=new_user, phone_number = phone_number, age = age, 
            										organization = organization)
            partner_user.save()

    else:
        partner_user_form = PartnerUserForm()
        section_name = 'Add A Partner User'
        return render(request, 'account/add_partner_user.html', {'section_name': section_name, 'form': partner_user_form })



####### Activate acount

def activate_account(request,uidb64, token):

    # def get(self, request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # user.profile.email_confirmed = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            # invalid link
            return render(request, 'registration/invalid.html')


def receive_cookies(request):
    return HttpResponse(request.COOKIES.items())






    