from django import forms
from django.contrib.auth.models import User

from .models import Profile, Refugee, Merchant, PartnerUser, Trucker

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
        widgets ={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('role','company')
        widgets = {
            'role': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s role'}),
            'company': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s company name'}),
        }

class RefugeeForm(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ('phone_number','age','zone','village','family', 'alternate')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'age': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Company Number'}),
            'zone': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Refugee Zone'}),
            'village': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Village Number'}),
            'family': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Family Number'}),
            'alternate': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Alternate Recipient'})
        }

class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields =('phone_number', 'age', 'zone','village','account_number')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'age': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Company Number'}),
            'zone': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Merchant\'s Zone'}),
            'village': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Village Number'}),
            'account_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Account Number'})
        }

class PartnerUserForm(forms.ModelForm):
    class Meta:
        model = PartnerUser
        fields = ('phone_number','organization')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'organization': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Organization'})
        }

class TruckerForm(forms.ModelForm):
    class Meta:
        model =Trucker
        fields =('phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
        }

class ActivateAccountForm(forms.Form):
    token = forms.CharField(max_length=10, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Token'}))


class CreatePasswordForm(forms.Form):
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()


