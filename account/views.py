# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import uuid
import os

from django.shortcuts import render, redirect
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
from .forms import AddUserForm, ProfileForm, RefugeeForm,TruckerForm, MerchantForm, PartnerUserForm, ActivateAccountForm, CreatePasswordForm



# Create your views here.
def create_user(request):
    if request.method == 'POST':
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

            set_password_form = PasswordResetForm({'email':email})
            if set_password_form.is_valid():
                # print 'Reset Form is Valid'
                set_password_form.save(
                    request=request,
                    use_https=False,
                    from_email='bpmusisi@gmail.com',
                    email_template_name='account/activate_account.html'
                )

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

            #Using cookies to connect
            required_cookies = ['access_token','connect.sid', 'user_id']
            cookies = {key: request.session[key] for key in required_cookies}
            r = requests.post('http://{}/api/Person'.format(settings.HYPER_SERVER), data=data, cookies=cookies)

            # r = requests.post('http://{}/api/Person'.format(settings.HYPER_SERVER2), data=data, params=params)

            data = {
                    "participant": "org.kibaati.Person#{}".format(personId),
                    "userID": user_name
                    }

            # r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER2),data=data,params=params)

            #Using cookies
            r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data,cookies=cookies)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            card = open(path, 'w')
            card.write(r.content)
            card.close()

            # set_password_form = PasswordResetForm({'email':email})
            # if set_password_form.is_valid():
            #     # print 'Reset Form is Valid'
            #     set_password_form.save(
            #         request=request,
            #         use_https=False,
            #         from_email='bpmusisi@gmail.com',
            #         email_template_name='account:account/activate_account.html'
            #     )

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
            family = refugee_cd['family']
            alternate = refugee_cd['alternate']


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                 password=get_random_string())

            refugee = Refugee.objects.create(user=new_user, phone_number = phone_number, age = age, zone = zone,
                                            village=village, alternate=alternate)
            refugee.save()

            ######### Send to Blockchain #############

            personId = uuid.uuid4()


            data ={
                    "$class": "org.kibaati.Refugee",
                    "refugeeId": str(personId),
                    "phoneNumber": phone_number,
                    "age": age,
                    "zone": zone,
                    "village": village,
                    "alternate": str(alternate),
                    "family": "resource:org.kibaati.Family#%s" % family,
                    "personId": str(personId),
                    "firstName": first_name,
                    "lastName": last_name,
                    "balance": 0
                    }

            access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

            params={'access_token':access_token}

            required_cookies = ['access_token','connect.sid']
            cookies = {key: request.session[key] for key in required_cookies}

           # r = requests.post('http://{}/api/Refugee'.format(settings.HYPER_SERVER), data=data, cookies=cookies)

            try:
                r = requests.post('http://{}/api/Refugee'.format(settings.HYPER_SERVER), data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except ValueError:
                return HttpResponse(r.text)


            data = {
                    "participant": "org.kibaati.Refugee#{}".format(personId),
                    "userID": user_name
                    }

           # r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)

            #path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            #card = open(path, 'w')
            #card.write(r.content)
            #card.close()


            try:
                r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except:
                return HttpResponse(r.text)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            try:
                card = open(path, 'w')
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)

            card.write(r.content)
            card.close()

        return HttpResponse('Refugee created')


        #######################



    else:
        refugee_form = RefugeeForm()
        user_form = AddUserForm()
        section_name = 'Refugee'

       # access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

       # params={'access_token':access_token}


        required_cookies = ['access_token','connect.sid']
        cookies = {key: request.session[key] for key in required_cookies}

        print cookies

       # r = requests.get('http://{}/api/Refugee'.format(settings.BLOCKCHAIN_URL), cookies=cookies)


        try:
            r = requests.get('http://{}/api/Refugee'.format(settings.BLOCKCHAIN_URL), cookies=cookies)

	    print r.status_code
            if r.status_code / 100 != 2:
                raise ValueError(r.text)
        except ValueError:
            return HttpResponse (r.text)


        people = r.json()
        return render(request, 'account/add_refugee.html', {'section_name': section_name, 'refugee_form': refugee_form,
        'user_form':user_form, 'persons':people })


def add_merchant(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        merchant_form = MerchantForm(request.POST)
        if user_form.is_valid() and merchant_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            email = user_cd['email']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            merchant_cd = merchant_form.cleaned_data
            account_number = merchant_cd['account_number']
            phone_number = merchant_cd['phone_number']
            age = merchant_cd['age']
            zone = merchant_cd['zone']
            village = merchant_cd['village']



            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,
                                                 password=get_random_string())
            new_user.save()

            merchant = Merchant.objects.create(user=new_user, phone_number = phone_number, age = age, zone = zone,
                                            village=village, account_number = account_number)

            merchant.save()

            person_Id = uuid.uuid4()

            data = {
                "$class": "org.kibaati.Merchant",
                "merchantId": person_Id,
                "zone": zone,
                "email": email,
                "phoneNumber": phone_number,
                "accountNumber": account_number,
                "personId": person_Id,
                "firstName": first_name,
                "lastName": last_name,
                "balance": 0
                }

            access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

            params={'access_token':access_token}

            cookies= request.COOKIES

           # r = requests.post('http://{}/api/Merchant'.format(settings.HYPER_SERVER), data=data, cookies=cookies)


            try:
                r = requests.post('http://{}/api/Merchant'.format(settings.HYPER_SERVER), data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except ValueError:
                return HttpResponse(r.text)

            data = {
                    "participant": "org.kibaati.Merchant#{}".format(person_Id),
                    "userID": user_name
                    }

           # r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)

            #path = os.path.join(settings.BASE_DIR, 'account/cards/Merchants/%s.card' % user_name)

            #card = open(path, 'w')
            #card.write(r.content)
            #card.close()


            try:
                r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except:
                return HttpResponse(r.text)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            try:
                card = open(path, 'w')
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)

            card.write(r.content)
            card.close()

            return HttpResponse('Merchant has been created')
        else:
            return HttpResponse('Merchant has not been created')

    else:
        user_form = AddUserForm()
        merchant_form = MerchantForm()
        section_name = 'Merchants'

        #access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

        #params={'access_token':access_token}

        #Using cookies to connect
        # required_cookies = ['access_token','connect.sid']
        # cookies = {key: request.session[key] for key in required_cookies}

        cookies = request.COOKIES
        print cookies.items()

        #r = requests.get('http://{}/api/Merchant'.format(settings.BLOCKCHAIN_URL), cookies=cookies)

        try:
            r = requests.get('http://{}/api/Merchant'.format(settings.BLOCKCHAIN_URL), cookies=cookies)
            if r.status_code / 100 != 2:
                raise ValueError(r.text)
        except ValueError:
            return HttpResponse (r.text)

        people = r.json()

        return render(request, 'account/add_merchant.html', {'section_name': section_name, 
        'user_form':user_form, 'merchant_form': merchant_form, 
        'persons':people})



def add_partner_user(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        partner_user_form = PartnerUserForm(request.POST)
        print user_form.is_valid(), partner_user_form.is_valid()
        print user_form.errors
        print partner_user_form.errors
        if user_form.is_valid() and partner_user_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']
            email = user_cd['email']

            partner_user_cd = partner_user_form.cleaned_data
            phone_number = partner_user_cd['phone_number']
            organization = partner_user_cd['organization']


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, email=email,
                                                 password=get_random_string())
            new_user.save()

            partner_user = PartnerUser.objects.create(user=new_user, phone_number = phone_number,
            										organization = organization)
            partner_user.save()

            person_Id = uuid.uuid4()

            data = {
                    "$class": "org.kibaati.PartnerUser",
                    "email": email,
                    "phoneNumber": phone_number,
                    "organization": organization,
                    "personId": person_Id,
                    "firstName": first_name,
                    "lastName": last_name,
                    "balance": 0
                    }


            # access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

            # params={'access_token':access_token}

            # cookies = request.COOKIES

            required_cookies = ['access_token','connect.sid']
            cookies = {key: request.session[key] for key in required_cookies}

            try:
                r = requests.post('http://{}/api/PartnerUser'.format(settings.HYPER_SERVER), data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except ValueError:
                return HttpResponse(r.text)


            data = {
                    "participant": "org.kibaati.PartnerUser#{}".format(person_Id),
                    "userID": user_name
                    }

            try:
                r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except:
                return HttpResponse(r.text)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            try:
                card = open(path, 'w')
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)

            card.write(r.content)
            card.close()

            set_password_form = PasswordResetForm({'email':email})
            print set_password_form.is_valid(), set_password_form
            if set_password_form.is_valid():
                print 'Reset Form is Valid'
                set_password_form.save(
                    request=request,
                    use_https=False,
                    from_email='bpmusisi@gmail.com',
                    email_template_name='account/activate_account.html'
                )
            print set_password_form
            new_user.is_active = False

            return HttpResponse('PartnerUser has been created')

    else:
        partner_user_form = PartnerUserForm()
        user_form = AddUserForm()
        section_name = 'Partner User'

        # access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

        # params={'access_token':access_token}

        required_cookies = ['access_token','connect.sid']
        cookies = {key: request.session[key] for key in required_cookies}
        print cookies.items()
        # cookies = request.COOKIES

        try:
            r = requests.get('http://{}/api/PartnerUser'.format(settings.HYPER_SERVER), cookies=cookies)
            if r.status_code / 100 != 2:
                raise ValueError(r.text)
        except ValueError:
            return HttpResponse (r.text)

        people = r.json()

        return render(request, 'account/add_partner_user.html', {'section_name': section_name, 
        'partner_form': partner_user_form, 'user_form':user_form, 'persons':people })



####### Activate account

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
            return render(request, 'account/enter_token.html',{'section_name':'Import Token', 'form':ActivateAccountForm()})
            # login(request, user)
            # return redirect('profile')

        else:
            # invalid link
            # return render(request, 'registration/invalid.html')
            return HttpResponse('Your link is invalid')

    else:
        token_form = ActivateAccountForm(request.POST)

        if token_form.is_valid():
            token_cd = token_form.cleaned_data
            file_name = token_cd['token']

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % file_name)

            files = {'card': open(path, 'rb')}
            # access_token = 'X1tEvCbMZdrl9toBEPnlaB9WAzvZwijpclgyzD62LQUstuDYC3EpV2PM33MI2G4i'
            # params={'access_token':access_token}

            required_cookies = ['access_token','connect.sid']
            cookies = {key: request.session[key] for key in required_cookies}

            try:
                r = requests.post('http://{}/api/wallet/import'.format(settings.HYPER_SERVER),files=files, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)
                return HttpResponse("I/O error(%s): %s" % (errno, strerror))
            except ValueError:
                return HttpResponse(r.text)

            return render(request, 'hyper/dashboard.html',{'section_name':'Dashboard'})

def add_trucker(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        trucker_form = TruckerForm(request.POST)
        print user_form.is_valid(), trucker_form.is_valid()
        if user_form.is_valid() and trucker_form.is_valid():
            user_cd = user_form.cleaned_data
            user_name = user_cd['username']
            first_name = user_cd['first_name']
            last_name = user_cd['last_name']

            trucker_cd = trucker_form.cleaned_data
            phone_number = trucker_cd['phone_number']


            new_user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, email=email,
                                                 password=get_random_string())
            new_user.save()

            trucker = Trucker.objects.create(user=new_user, phone_number = phone_number,
            										organization = organization)
            trucker.save()

            person_Id = uuid.uuid4()

            data = 	{
  				"$class": "org.kibaati.Trucker",
 				"truckId": "",
				"phoneNumber": 0,
  				"personId": "string",
  				"firstName": "string",
  				"lastName": "string",
  				"balance": 0
				}



            required_cookies = ['access_token','connect.sid']
            cookies = {key: request.session[key] for key in required_cookies}

            try:
                r = requests.post('http://{}/api/Trucker'.format(settings.HYPER_SERVER), data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except ValueError:
                return HttpResponse(r.text)


            data = {
                    "participant": "org.kibaati.Trucker#{}".format(person_Id),
                    "userID": user_name
                    }

            try:
                r = requests.post('http://{}/api/system/identities/issue'.format(settings.HYPER_SERVER),data=data, cookies=cookies)
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except:
                return HttpResponse(r.text)

            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % user_name)

            try:
                card = open(path, 'w')
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)

            card.write(r.content)
            card.close()

            set_password_form = PasswordResetForm({'email':email})
            print set_password_form.is_valid(), set_password_form
            if set_password_form.is_valid():
                print 'Reset Form is Valid'
                set_password_form.save(
                    request=request,
                    use_https=False,
                    from_email='bpmusisi@gmail.com',
                    email_template_name='account/activate_account.html'
                )
            print set_password_form
            new_user.is_active = False

            try:
            	r = requests.get('http://{}/api/Trucker'.format(settings.HYPER_SERVER), cookies=cookies)
            	if r.status_code / 100 != 2:
                	raise ValueError(r.text)
            except ValueError:
            	return HttpResponse (r.text)

        	people = r.json()

        	return render(request, 'account/add_trucker.html', {'section_name': section_name, 
        	'trucker_form': trucker_form, 'user_form':user_form, 'persons':people })

    else:
        trucker_form = TruckerForm()
        user_form = AddUserForm()
        section_name = 'Trucker User'

        # access_token = '6Ks7RDiFxTTIIq6F9PtFs65w3padbW67lYE66tYXRkL4AsCGCa8Z1TXD4XbGvR2c'

        # params={'access_token':access_token}

        required_cookies = ['access_token','connect.sid']
        cookies = {key: request.session[key] for key in required_cookies}
        print cookies.items()
        # cookies = request.COOKIES

        try:
            r = requests.get('http://{}/api/Trucker'.format(settings.HYPER_SERVER), cookies=cookies)
            if r.status_code / 100 != 2:
                raise ValueError(r.text)
        except ValueError:
            return HttpResponse (r.text)

        people = r.json()

        return render(request, 'account/add_trucker.html', {'section_name': section_name, 
        'trucker_form': trucker_form, 'user_form':user_form, 'persons':people })


def enter_token(request):
    if request.method == 'POST':
        token_form = ActivateAccountForm(request.POST)
        print token_form.is_valid() 
        if token_form.is_valid():
            token_cd = token_form.cleaned_data
            file_name = token_cd['token']

            print file_name
            path = os.path.join(settings.BASE_DIR, 'account/cards/%s.card' % file_name)

            print
            print path

            files = {'card': open(path, 'rb')}
            # access_token = 'X1tEvCbMZdrl9toBEPnlaB9WAzvZwijpclgyzD62LQUstuDYC3EpV2PM33MI2G4i'
            # params={'access_token':access_token}

            required_cookies = ['access_token','connect.sid']
            cookies = {key: request.session[key] for key in required_cookies}

            print cookies

            try:
                r = requests.post('http://{}/api/wallet/import'.format(settings.HYPER_SERVER),files=files, cookies=cookies)
                r= requests.post('http://{}/api/wallet/{}@mabreezi/setDefault'.format(settings.HYPER_SERVER, file_name) , cookies=cookies)
                print r.status_code
                if r.status_code / 100 != 2:
                    raise ValueError(r.text)
            except IOError, (errno, strerror):
                print "I/O error(%s): %s" % (errno, strerror)
                return HttpResponse("I/O error(%s): %s" % (errno, strerror))
            except ValueError:
                return HttpResponse(r.text)

            return render(request, 'hyper/dashboard.html',{'section_name':'Dashboard'})

    else:
        form = ActivateAccountForm()
        return render(request, 'account/enter_token.html', {'form': form , 'section_name' : 'Enter Token' })

def password_create(request):
    if request.method == 'POST':
        password_create_form = CreatePasswordForm(request.POST)

        if password_create_form.is_valid():
            password_cd = password_create_form.cleaned_data
            password = password_cd['password']
            confirm_password = password['confirm_password']

            if password == confirm_password:
                return HttpResponse('Password Successfully Created')

    else:
        password_create_form = CreatePasswordForm()

        return render(request, 'account/password_create.html', {'form':password_create_form} )


def kodhi_login(request):
    return redirect('http://hyper.brianmusisi.com/auth/github')
