from django import forms
from django.contrib.auth.models import User

from .models import Profile, Refugee, Merchant, PartnerUser

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('role','company')

class RefugeeForm(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ('phone_number','age','zone', 'village','alternate')

class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields =('phone_number', 'age', 'zone','village','account_number')

class PartnerUserForm(forms.ModelForm):
    class Meta:
        model = PartnerUser
        fields = ('phone_number','age','organization')