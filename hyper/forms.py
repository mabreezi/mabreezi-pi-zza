from django import forms

from .models import Person, Item

#Model Form for the diferent persons
class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'role')
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s first name'}),
			'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s last name'}),
			'role':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s role'})
		}



#Model Form for the Items to be transferred
class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields =('name', 'description', 'quantity', 'owner')
		widgets = {
			'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of the item'}),
			'description':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Describe the item'}),
			'quantity':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Amount of the item'}),
			'owner':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Person\'s ID'})
		}

#Form for making a transaction
class TransactionForm(forms.Form):
	sender = forms.CharField(max_length=40, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sender ID'})) #takes the sender id
	recipient = forms.CharField(max_length=40, widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Recipient ID'})) # takes the recipient id
	amount = forms.IntegerField(widget= forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Amount to transfer'}))

class TradeForm(forms.Form):
	sender = forms.CharField(max_length=40, widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Sender ID'})) #takes the sedner id
	item = forms.CharField(max_length=40, widget= forms.NumberInput(attrs={'class':'form-control','placeholder':'Item ID'})) #takes the item id
	recipient = forms.CharField(max_length=40, widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Recipient ID'})) #takes the recipient id


