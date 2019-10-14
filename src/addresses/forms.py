from django import forms
from .models import Address
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.forms import ModelForm

class AddressRegisterForm(forms.ModelForm):
    #class meta renders the the form as exactly is displayed in admin django web page
     
    class Meta:
        model = Address
        fields = ['address_type', 'address_line_1',
                  'address_line_2', 'city', 'state', 'zip_code', 'country']


class AddressUpdateForm(forms.ModelForm):
     email = forms.EmailField()

     class Meta:
        model = Address
        fields = ['address_line_1',
                  'address_line_2', 'city', 'state', 'zip_code']
     def __init__(self, *args, **kwargs):
        super(AddressUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Field('address_line_1'),
            Field('address_line_2'),
            Field('city'),
            Field('state'))
           
